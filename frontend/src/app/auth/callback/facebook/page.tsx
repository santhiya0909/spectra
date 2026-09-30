"use client";

/**
 * Facebook OAuth 2.0 Callback Page
 * ──────────────────────────────────
 * Facebook redirects here after the user authorises the app.
 * The access_token arrives in the URL fragment (hash), e.g.:
 *   /auth/callback/facebook#access_token=EAA...&token_type=bearer&...
 *
 * This page:
 *  1. Reads the access_token (or error) from window.location.hash
 *  2. Posts it back to the opener window via postMessage
 *  3. Closes itself
 *
 * Token validation happens server-side in the backend via
 * Facebook's /debug_token Graph API endpoint.
 *
 * Registered Redirect URI (add this in Facebook Developer Console):
 *   http://localhost:3001/auth/callback/facebook
 */

import { useEffect } from "react";

export default function FacebookCallbackPage() {
  useEffect(() => {
    // Facebook puts the access_token in the URL hash fragment (implicit flow)
    const hash = window.location.hash.startsWith("#")
      ? window.location.hash.slice(1)
      : window.location.hash;

    const params = new URLSearchParams(hash);
    const access_token = params.get("access_token");

    // Facebook may also return error in the query string
    const searchParams = new URLSearchParams(window.location.search);
    const error = searchParams.get("error") || params.get("error");
    const error_description =
      searchParams.get("error_description") ||
      params.get("error_description") ||
      "Facebook authentication failed.";

    const origin = window.location.origin;

    if (window.opener && typeof window.opener.postMessage === "function") {
      if (access_token) {
        window.opener.postMessage(
          { type: "SPECTRA_FACEBOOK_AUTH_SUCCESS", access_token },
          origin
        );
      } else {
        window.opener.postMessage(
          {
            type: "SPECTRA_FACEBOOK_AUTH_ERROR",
            error: error || "unknown_error",
            error_description,
          },
          origin
        );
      }
    }

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
          border: "3px solid #1877F2",
          borderTopColor: "transparent",
          borderRadius: "50%",
          animation: "spin 0.8s linear infinite",
        }}
      />
      <p style={{ margin: 0, fontSize: 14 }}>Completing Facebook sign-in&hellip;</p>
      <style>{`@keyframes spin { to { transform: rotate(360deg); } }`}</style>
    </div>
  );
}
