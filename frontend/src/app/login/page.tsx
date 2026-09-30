"use client";

import React, { useState, useEffect, Suspense } from "react";
import Link from "next/link";
import { useSearchParams } from "next/navigation";
import { useAuth } from "@/lib/auth";
import { useSocialAuth } from "@/lib/useSocialAuth";
import { Sparkles, Loader2, AlertCircle } from "lucide-react";
import { GlassCard } from "@/components/common/GlassCard";
import { ThemeToggle } from "@/components/theme/ThemeToggle";

// ── Google SVG icon ─────────────────────────────────────────────────────────
function GoogleIcon({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" aria-hidden="true">
      <path
        fill="#4285F4"
        d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"
      />
      <path
        fill="#34A853"
        d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"
      />
      <path
        fill="#FBBC05"
        d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l3.66-2.84z"
      />
      <path
        fill="#EA4335"
        d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"
      />
    </svg>
  );
}

// ── Facebook SVG icon ────────────────────────────────────────────────────────
function FacebookIcon({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" aria-hidden="true" fill="#1877F2">
      <path d="M24 12.073C24 5.405 18.627 0 12 0S0 5.405 0 12.073C0 18.1 4.388 23.094 10.125 24v-8.437H7.078v-3.49h3.047V9.41c0-3.025 1.792-4.697 4.533-4.697 1.312 0 2.686.235 2.686.235v2.97h-1.513c-1.491 0-1.956.93-1.956 1.874v2.25h3.328l-.532 3.49h-2.796V24C19.612 23.094 24 18.1 24 12.073z" />
    </svg>
  );
}

// ── OR divider ───────────────────────────────────────────────────────────────
function OrDivider() {
  return (
    <div className="flex items-center gap-3 my-5">
      <div className="flex-1 h-px bg-slate-200 dark:bg-white/10" />
      <span className="text-[10px] font-bold uppercase tracking-widest text-slate-400 dark:text-slate-500 select-none">
        or
      </span>
      <div className="flex-1 h-px bg-slate-200 dark:bg-white/10" />
    </div>
  );
}

// ── Social button ─────────────────────────────────────────────────────────────
interface SocialButtonProps {
  icon: React.ReactNode;
  label: string;
  loadingLabel: string;
  isLoading: boolean;
  disabled: boolean;
  onClick: () => void;
  bgClass: string;
  hoverBgClass: string;
  textClass: string;
  borderClass: string;
  ringClass: string;
}

function SocialButton({
  icon,
  label,
  loadingLabel,
  isLoading,
  disabled,
  onClick,
  bgClass,
  hoverBgClass,
  textClass,
  borderClass,
  ringClass,
}: SocialButtonProps) {
  return (
    <button
      type="button"
      onClick={onClick}
      disabled={disabled}
      className={`
        relative flex w-full items-center justify-center gap-3
        rounded-xl border px-4 py-2.5
        text-xs font-bold transition-all duration-200
        focus:outline-none focus-visible:ring-2
        disabled:cursor-not-allowed disabled:opacity-50
        active:scale-[0.98]
        ${bgClass} ${hoverBgClass} ${textClass} ${borderClass} ${ringClass}
      `}
    >
      {isLoading ? (
        <>
          <Loader2 className="h-4 w-4 animate-spin shrink-0" />
          <span>{loadingLabel}</span>
        </>
      ) : (
        <>
          {icon}
          <span>{label}</span>
        </>
      )}
    </button>
  );
}

// ── Main login form ───────────────────────────────────────────────────────────
function LoginForm() {
  const { login, isLoading } = useAuth();
  const { loginWithGoogle, loginWithFacebook } = useSocialAuth();
  const searchParams = useSearchParams();
  const roleParam = searchParams.get("role");

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [googleLoading, setGoogleLoading] = useState(false);
  const [facebookLoading, setFacebookLoading] = useState(false);

  const anySocialLoading = googleLoading || facebookLoading;
  const anyLoading = isSubmitting || isLoading || anySocialLoading;

  useEffect(() => {
    if (roleParam === "student") {
      setEmail("student@example.com");
      setPassword("student123");
    } else if (roleParam === "teacher") {
      setEmail("teacher@example.com");
      setPassword("teacher123");
    } else if (roleParam === "admin") {
      setEmail("admin@example.com");
      setPassword("admin123");
    }
  }, [roleParam]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setIsSubmitting(true);
    try {
      await login(email, password);
    } catch (err: any) {
      setError(err.message || "Failed to sign in. Please verify your credentials.");
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleGoogleLogin = async () => {
    setError(null);
    setGoogleLoading(true);
    try {
      await loginWithGoogle();
    } catch (err: any) {
      setError(err.message || "Google sign-in failed. Please try again.");
    } finally {
      setGoogleLoading(false);
    }
  };

  const handleFacebookLogin = async () => {
    setError(null);
    setFacebookLoading(true);
    try {
      await loginWithFacebook();
    } catch (err: any) {
      setError(err.message || "Facebook sign-in failed. Please try again.");
    } finally {
      setFacebookLoading(false);
    }
  };

  const setDemoCredentials = (role: "student" | "teacher" | "admin") => {
    setError(null);
    if (role === "student") {
      setEmail("student@example.com");
      setPassword("student123");
    } else if (role === "teacher") {
      setEmail("teacher@example.com");
      setPassword("teacher123");
    } else {
      setEmail("admin@example.com");
      setPassword("admin123");
    }
  };

  return (
    <div className="w-full max-w-md">
      <div className="text-center mb-8">
        <div className="inline-flex h-14 w-14 items-center justify-center rounded-2xl bg-gradient-to-tr from-cyan-400 via-indigo-600 to-purple-600 text-white shadow-[0_0_30px_rgba(6,182,212,0.4)] mb-3">
          <Sparkles className="h-7 w-7" />
        </div>
        <h1 className="text-3xl font-black tracking-tight text-slate-900 dark:text-white">Sign in to SPECTRA</h1>
        <p className="mt-1 text-xs text-slate-500 dark:text-slate-400">Access your adaptive neural learning environment</p>
      </div>

      {/* Demo Credential Quick Fill */}
      <div className="mb-6 rounded-3xl border border-slate-200/90 dark:border-white/10 bg-white/90 dark:bg-[#0B1124]/90 p-4 backdrop-blur-2xl shadow-sm dark:shadow-lg">
        <p className="text-[10px] font-extrabold uppercase tracking-widest text-cyan-600 dark:text-cyan-300 mb-2">
          One-Click Demo Accounts
        </p>
        <div className="grid grid-cols-3 gap-2">
          <button
            type="button"
            onClick={() => setDemoCredentials("student")}
            className={`rounded-xl border px-2.5 py-2 text-xs font-bold transition-all ${
              email === "student@example.com"
                ? "border-cyan-500 bg-cyan-500/15 text-cyan-700 dark:text-cyan-300 shadow-sm"
                : "border-slate-200 dark:border-white/10 bg-slate-50 dark:bg-white/[0.03] hover:bg-slate-100 dark:hover:bg-white/[0.08] text-slate-700 dark:text-slate-300"
            }`}
          >
            🎓 Student
          </button>
          <button
            type="button"
            onClick={() => setDemoCredentials("teacher")}
            className={`rounded-xl border px-2.5 py-2 text-xs font-bold transition-all ${
              email === "teacher@example.com"
                ? "border-purple-500 bg-purple-500/15 text-purple-700 dark:text-purple-300 shadow-sm"
                : "border-slate-200 dark:border-white/10 bg-slate-50 dark:bg-white/[0.03] hover:bg-slate-100 dark:hover:bg-white/[0.08] text-slate-700 dark:text-slate-300"
            }`}
          >
            👩‍🏫 Teacher
          </button>
          <button
            type="button"
            onClick={() => setDemoCredentials("admin")}
            className={`rounded-xl border px-2.5 py-2 text-xs font-bold transition-all ${
              email === "admin@example.com"
                ? "border-emerald-500 bg-emerald-500/15 text-emerald-700 dark:text-emerald-300 shadow-sm"
                : "border-slate-200 dark:border-white/10 bg-slate-50 dark:bg-white/[0.03] hover:bg-slate-100 dark:hover:bg-white/[0.08] text-slate-700 dark:text-slate-300"
            }`}
          >
            🛡️ Admin
          </button>
        </div>
      </div>

      {/* Form Container */}
      <GlassCard className="p-6 sm:p-7 shadow-xl dark:shadow-2xl">
        {/* Error banner */}
        {error && (
          <div className="mb-4 flex items-center gap-2 rounded-xl border border-rose-500/30 bg-rose-50 dark:bg-rose-950/30 p-3 text-xs font-medium text-rose-700 dark:text-rose-300">
            <AlertCircle className="h-4 w-4 shrink-0 text-rose-500 dark:text-rose-400" />
            <span>{error}</span>
          </div>
        )}

        {/* ── Email / Password form ──────────────────────────────────────── */}
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-xs font-bold uppercase tracking-wider text-slate-600 dark:text-slate-400 mb-1.5">
              Email Address
            </label>
            <input
              type="email"
              required
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="name@university.edu"
              className="w-full rounded-xl border border-slate-300 dark:border-white/10 bg-slate-50 dark:bg-[#060913] px-3.5 py-2.5 text-sm text-slate-900 dark:text-white placeholder:text-slate-400 dark:placeholder:text-slate-500 outline-none transition focus:border-cyan-500 focus:ring-2 focus:ring-cyan-500/20"
            />
          </div>

          <div>
            <label className="block text-xs font-bold uppercase tracking-wider text-slate-600 dark:text-slate-400 mb-1.5">
              Password
            </label>
            <input
              type="password"
              required
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="••••••••"
              className="w-full rounded-xl border border-slate-300 dark:border-white/10 bg-slate-50 dark:bg-[#060913] px-3.5 py-2.5 text-sm text-slate-900 dark:text-white placeholder:text-slate-400 dark:placeholder:text-slate-500 outline-none transition focus:border-cyan-500 focus:ring-2 focus:ring-cyan-500/20"
            />
          </div>

          <button
            type="submit"
            disabled={anyLoading}
            className="flex w-full items-center justify-center gap-2 rounded-xl bg-gradient-to-r from-cyan-500 to-indigo-600 hover:from-cyan-400 hover:to-indigo-500 px-4 py-3 text-xs font-black uppercase tracking-wider text-black shadow-md transition disabled:opacity-50 mt-2"
          >
            {isSubmitting ? (
              <>
                <Loader2 className="h-4 w-4 animate-spin text-black" />
                <span>Authenticating...</span>
              </>
            ) : (
              <span>Sign In &rarr;</span>
            )}
          </button>
        </form>

        {/* ── OR divider ─────────────────────────────────────────────────── */}
        <OrDivider />

        {/* ── Social login buttons ────────────────────────────────────────── */}
        <div className="space-y-3">
          {/* Google */}
          <SocialButton
            icon={<GoogleIcon className="h-4 w-4 shrink-0" />}
            label="Continue with Google"
            loadingLabel="Connecting to Google..."
            isLoading={googleLoading}
            disabled={anyLoading}
            onClick={handleGoogleLogin}
            bgClass="bg-white dark:bg-white/[0.04]"
            hoverBgClass="hover:bg-slate-50 dark:hover:bg-white/[0.09]"
            textClass="text-slate-800 dark:text-slate-100"
            borderClass="border-slate-300 dark:border-white/10"
            ringClass="focus-visible:ring-blue-500/40"
          />

          {/* Facebook */}
          <SocialButton
            icon={<FacebookIcon className="h-4 w-4 shrink-0" />}
            label="Continue with Facebook"
            loadingLabel="Connecting to Facebook..."
            isLoading={facebookLoading}
            disabled={anyLoading}
            onClick={handleFacebookLogin}
            bgClass="bg-[#1877F2]/10 dark:bg-[#1877F2]/[0.12]"
            hoverBgClass="hover:bg-[#1877F2]/[0.18] dark:hover:bg-[#1877F2]/[0.22]"
            textClass="text-[#1877F2] dark:text-[#6FA8FF]"
            borderClass="border-[#1877F2]/30 dark:border-[#1877F2]/25"
            ringClass="focus-visible:ring-[#1877F2]/40"
          />
        </div>

        {/* Register link */}
        <div className="mt-5 text-center text-xs text-slate-500 dark:text-slate-400">
          Don&apos;t have an account?{" "}
          <Link href="/register" className="font-bold text-cyan-600 dark:text-cyan-400 hover:underline">
            Create an account
          </Link>
        </div>
      </GlassCard>
    </div>
  );
}

export default function LoginPage() {
  return (
    <div className="relative flex min-h-screen items-center justify-center bg-[#F8FAFC] dark:bg-[#060913] bg-cosmic-grid px-4 py-12 overflow-hidden transition-colors">
      {/* Top right Theme Toggle button */}
      <div className="absolute top-5 right-5 z-20">
        <ThemeToggle />
      </div>

      {/* Ambient glowing orbs */}
      <div className="fixed -top-40 -left-40 w-[500px] h-[500px] bg-cyan-500/[0.05] dark:bg-cyan-500/[0.1] rounded-full blur-[140px] pointer-events-none" />
      <div className="fixed -bottom-40 -right-40 w-[500px] h-[500px] bg-purple-500/[0.05] dark:bg-purple-500/[0.1] rounded-full blur-[140px] pointer-events-none" />

      <div className="relative z-10 w-full max-w-md">
        <Suspense fallback={<div className="text-center p-8 text-slate-400">Loading SPECTRA Environment...</div>}>
          <LoginForm />
        </Suspense>
      </div>
    </div>
  );
}
