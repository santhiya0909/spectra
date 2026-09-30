"use client";

/**
 * useSocialAuth
 * ─────────────
 * Provides `loginWithGoogle()` and `loginWithFacebook()`.
 *
 * HOW IT WORKS (no heavy SDKs required)
 * ──────────────────────────────────────
 * 1. Open a small popup window pointing at the OAuth provider's consent page
 * 2. The provider redirects to our callback page (/auth/callback/google|facebook)
 *    with the token in the URL hash fragment
 * 3. The callback page reads the token and posts it back via postMessage
 * 4. We receive the message, send the token to our backend for server-side
 *    verification, receive a SPECTRA JWT, persist it, and redirect
 *
 * WHY THIS APPROACH
 * ──────────────────
 * - Google One Tap is blocked by modern browsers (third-party cookie
 *   restrictions, FedCM not yet universally available)
 * - The popup/postMessage pattern works in all browsers, requires no SDK,
 *   and is the most reliable cross-browser OAuth UX pattern
 *
 * ENV VARS REQUIRED
 * ──────────────────
 * NEXT_PUBLIC_GOOGLE_CLIENT_ID   → frontend/.env.local
 * NEXT_PUBLIC_FACEBOOK_APP_ID    → frontend/.env.local
 * GOOGLE_CLIENT_ID               → backend/.env  (same value)
 * FACEBOOK_APP_ID                → backend/.env
 * FACEBOOK_APP_SECRET            → backend/.env  (NEVER in frontend)
 */

import { useCallback } from "react";
import { useRouter } from "next/navigation";

// ── Constants read from env ──────────────────────────────────────────────────

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000";

/** Public Google OAuth client ID — safe in browser, issued per-app */
const GOOGLE_CLIENT_ID = process.env.NEXT_PUBLIC_GOOGLE_CLIENT_ID ?? "";

/** Public Facebook App ID — safe in browser, issued per-app */
const FACEBOOK_APP_ID = process.env.NEXT_PUBLIC_FACEBOOK_APP_ID ?? "";

/** Popup window dimensions */
const POPUP_W = 520;
const POPUP_H = 620;

/** How long to wait for the user to complete the OAuth flow (2 min) */
const POPUP_TIMEOUT_MS = 120_000;

// ── Types ────────────────────────────────────────────────────────────────────

interface SpectraToken {
  access_token: string;
  token_type: string;
  role: "STUDENT" | "TEACHER" | "ADMIN";
  user_id: number;
  name: string;
  email: string;
}

// ── Helpers ──────────────────────────────────────────────────────────────────

/** Open an OAuth popup, centred on the screen */
function openPopup(url: string, title: string): Window | null {
  const left = window.screenX + (window.outerWidth - POPUP_W) / 2;
  const top = window.screenY + (window.outerHeight - POPUP_H) / 2;
  return window.open(
    url,
    title,
    [
      `width=${POPUP_W}`,
      `height=${POPUP_H}`,
      `left=${left}`,
      `top=${top}`,
      "toolbar=no",
      "menubar=no",
      "location=no",
      "status=no",
      "scrollbars=yes",
      "resizable=yes",
    ].join(",")
  );
}

/** Exchange a Google ID token with our backend and receive a SPECTRA JWT */
async function exchangeGoogleToken(idToken: string): Promise<SpectraToken> {
  const res = await fetch(`${API_URL}/api/auth/social/google`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ id_token: idToken }),
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || "Google sign-in failed. Please try again.");
  }
  return res.json();
}

/** Exchange a Facebook access token with our backend and receive a SPECTRA JWT */
async function exchangeFacebookToken(accessToken: string): Promise<SpectraToken> {
  const res = await fetch(`${API_URL}/api/auth/social/facebook`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ access_token: accessToken }),
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || "Facebook sign-in failed. Please try again.");
  }
  return res.json();
}

/** Persist the SPECTRA session so the AuthContext picks it up on next render */
function persistSession(token: SpectraToken): void {
  localStorage.setItem("spectra_token", token.access_token);
  localStorage.setItem(
    "spectra_user",
    JSON.stringify({
      id: token.user_id,
      name: token.name,
      email: token.email,
      role: token.role,
    })
  );
}

/** Redirect to the correct dashboard based on role */
function redirectByRole(role: string, router: ReturnType<typeof useRouter>): void {
  if (role === "STUDENT") router.push("/student/dashboard");
  else if (role === "TEACHER") router.push("/teacher/dashboard");
  else if (role === "ADMIN") router.push("/admin/dashboard");
  else router.push("/login");
}

/**
 * Wait for a postMessage from our callback page, with timeout and
 * popup-closed detection.
 *
 * Resolves with the raw token value string.
 * Rejects on cancellation, timeout, or auth error.
 */
function waitForPopupToken(
  popup: Window,
  successType: string,
  errorType: string,
  tokenKey: string
): Promise<string> {
  return new Promise<string>((resolve, reject) => {
    const origin = window.location.origin;

    // Timeout guard
    const timeoutId = setTimeout(() => {
      cleanup();
      reject(
        new Error("Sign-in timed out. Please try again.")
      );
    }, POPUP_TIMEOUT_MS);

    // Poll for popup closure (user closed it manually)
    const pollId = setInterval(() => {
      if (popup.closed) {
        cleanup();
        reject(new Error("Sign-in was cancelled."));
      }
    }, 500);

    function onMessage(event: MessageEvent) {
      // Only accept messages from our own origin
      if (event.origin !== origin) return;

      const { type, error_description } = event.data ?? {};

      if (type === successType) {
        const tokenValue = event.data[tokenKey] as string;
        cleanup();
        if (tokenValue) {
          resolve(tokenValue);
        } else {
          reject(new Error("Authentication succeeded but no token was returned."));
        }
        return;
      }

      if (type === errorType) {
        cleanup();
        reject(
          new Error(
            error_description ||
              event.data?.error ||
              "Authentication failed."
          )
        );
      }
    }

    window.addEventListener("message", onMessage);

    function cleanup() {
      clearTimeout(timeoutId);
      clearInterval(pollId);
      window.removeEventListener("message", onMessage);
      // Close popup if still open
      try {
        if (!popup.closed) popup.close();
      } catch {
        /* cross-origin guard — safe to ignore */
      }
    }
  });
}

// ── Hook ──────────────────────────────────────────────────────────────────────

export function useSocialAuth() {
  const router = useRouter();

  // ── Google ────────────────────────────────────────────────────────────────

  const loginWithGoogle = useCallback(async (): Promise<void> => {
    // Guard: credentials must be configured before the flow starts
    if (!GOOGLE_CLIENT_ID || GOOGLE_CLIENT_ID === "YOUR_GOOGLE_CLIENT_ID_HERE") {
      throw new Error(
        "Google Sign-In is not configured yet.\n" +
          "Add your NEXT_PUBLIC_GOOGLE_CLIENT_ID to frontend/.env.local and restart the dev server.\n" +
          "Get a Client ID at: https://console.cloud.google.com/apis/credentials"
      );
    }

    // Build the Google OAuth 2.0 implicit flow URL
    // response_type=id_token delivers the signed JWT directly to the callback
    const callbackUrl = `${window.location.origin}/auth/callback/google`;
    // Nonce prevents replay attacks — we generate a random one per request
    const nonce = Array.from(crypto.getRandomValues(new Uint8Array(16)))
      .map((b) => b.toString(16).padStart(2, "0"))
      .join("");

    const params = new URLSearchParams({
      client_id: GOOGLE_CLIENT_ID,
      redirect_uri: callbackUrl,
      response_type: "id_token",
      scope: "openid email profile",
      nonce,
      prompt: "select_account", // always show account chooser
    });

    const oauthUrl = `https://accounts.google.com/o/oauth2/v2/auth?${params}`;

    const popup = openPopup(oauthUrl, "Sign in with Google");
    if (!popup) {
      throw new Error(
        "A pop-up blocker prevented the Google sign-in window from opening. " +
          "Please allow pop-ups for this site and try again."
      );
    }

    // Wait for the callback page to post the id_token back
    const idToken = await waitForPopupToken(
      popup,
      "SPECTRA_GOOGLE_AUTH_SUCCESS",
      "SPECTRA_GOOGLE_AUTH_ERROR",
      "id_token"
    );

    // Exchange the id_token for a SPECTRA JWT (server-side verification)
    const spectraToken = await exchangeGoogleToken(idToken);
    persistSession(spectraToken);
    redirectByRole(spectraToken.role, router);
  }, [router]);

  // ── Facebook ──────────────────────────────────────────────────────────────

  const loginWithFacebook = useCallback(async (): Promise<void> => {
    if (!FACEBOOK_APP_ID || FACEBOOK_APP_ID === "YOUR_FACEBOOK_APP_ID_HERE") {
      throw new Error(
        "Facebook Login is not configured yet.\n" +
          "Add your NEXT_PUBLIC_FACEBOOK_APP_ID to frontend/.env.local and restart the dev server.\n" +
          "Get an App ID at: https://developers.facebook.com/apps"
      );
    }

    // Facebook OAuth dialog — implicit flow returns access_token in hash
    const callbackUrl = `${window.location.origin}/auth/callback/facebook`;

    const params = new URLSearchParams({
      client_id: FACEBOOK_APP_ID,
      redirect_uri: callbackUrl,
      response_type: "token",
      scope: "email,public_profile",
      // display=popup keeps the UI compact inside the popup window
      display: "popup",
    });

    const oauthUrl = `https://www.facebook.com/v21.0/dialog/oauth?${params}`;

    const popup = openPopup(oauthUrl, "Sign in with Facebook");
    if (!popup) {
      throw new Error(
        "A pop-up blocker prevented the Facebook sign-in window from opening. " +
          "Please allow pop-ups for this site and try again."
      );
    }

    // Wait for the callback page to post the access_token back
    const accessToken = await waitForPopupToken(
      popup,
      "SPECTRA_FACEBOOK_AUTH_SUCCESS",
      "SPECTRA_FACEBOOK_AUTH_ERROR",
      "access_token"
    );

    // Exchange the access_token for a SPECTRA JWT (server-side verification)
    const spectraToken = await exchangeFacebookToken(accessToken);
    persistSession(spectraToken);
    redirectByRole(spectraToken.role, router);
  }, [router]);

  return { loginWithGoogle, loginWithFacebook };
}
