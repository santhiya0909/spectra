"use client";

/**
 * Google OAuth 2.0 Callback Page
 * ─────────────────────────────
 * Google redirects here after the user authorises the app.
 * The id_token arrives in the URL fragment (hash), e.g.:
 *   /auth/callback/google#id_token=eyJ...&token_type=bearer&...
 *
 * This page:
 *  1. Reads the id_token (or error) from window.location.hash
 *  2. Posts it back to the opener window via postMessage
 *  3. Closes itself
 *
 * It NEVER touches the network — token exchange happens in useSocialAuth.ts
 * so the id_token is always verified server-side before any session is set.
 *
 * Registered Redirect URI (add this in Google Cloud Console):
 *   http://localhost:3001/auth/callback/google
 */

import { useEffect } from "react";

export default function GoogleCallbackPage() {
  useEffect(() => {
    // Google puts the id_token in the URL hash fragment (implicit flow)
    const hash = window.location.hash.startsWith("#")
      ? window.location.hash.slice(1)
      : window.location.hash;

    const params = new URLSearchParams(hash);
    const id_token = params.get("id_token");
    const error = params.get("error");
    const error_description = params.get("error_description");

    const origin = window.location.origin;

    if (window.opener && typeof window.opener.postMessage === "function") {
      if (id_token) {
        window.opener.postMessage(
          { type: "SPECTRA_GOOGLE_AUTH_SUCCESS", id_token },
          origin
        );
      } else {
        window.opener.postMessage(
          {
            type: "SPECTRA_GOOGLE_AUTH_ERROR",
            error: error || "unknown_error",
            error_description: error_description || "Google authentication failed.",
          },
          origin
        );
      }
    }

    // Close the popup — a small delay lets postMessage be delivered first
    const timer = setTimeout(() => window.close(), 300);
    return () => clearTimeout(timer);
  }, []);

  return (
    <div
      style={{
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        justifyContent: "center",
        minHeight: "100vh",
        fontFamily: "system-ui, sans-serif",
        background: "#060913",
        color: "#94a3b8",
        gap: "12px",
      }}
    >
      <div
        style={{
          width: 32,
          height: 32,
          border: "3px solid #22d3ee",
          borderTopColor: "transparent",
          borderRadius: "50%",
          animation: "spin 0.8s linear infinite",
        }}
      />
      <p style={{ margin: 0, fontSize: 14 }}>Completing Google sign-in&hellip;</p>
      <style>{`@keyframes spin { to { transform: rotate(360deg); } }`}</style>
    </div>
  );
}
