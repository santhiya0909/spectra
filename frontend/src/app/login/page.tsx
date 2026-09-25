"use client";

import React, { useState, useEffect, Suspense } from "react";
import Link from "next/link";
import { useSearchParams } from "next/navigation";
import { useAuth } from "@/lib/auth";
import { Sparkles, Loader2, AlertCircle } from "lucide-react";

function LoginForm() {
  const { login, isLoading } = useAuth();
  const searchParams = useSearchParams();
  const roleParam = searchParams.get("role");

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);

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
        <div className="inline-flex h-12 w-12 items-center justify-center rounded-2xl bg-gradient-to-tr from-brand-600 via-secondary-500 to-accent-500 text-white shadow-lg shadow-brand-500/20 mb-3">
          <Sparkles className="h-6 w-6" />
        </div>
        <h1 className="text-2xl font-bold tracking-tight text-slate-900">Sign in to SPECTRA</h1>
        <p className="mt-1 text-sm text-slate-500">Access your personalized learning environment</p>
      </div>

      {/* Demo Credential Quick Fill */}
      <div className="mb-6 rounded-2xl border border-slate-200 bg-white p-4 shadow-sm">
        <p className="text-xs font-bold uppercase tracking-wider text-slate-400 mb-2">
          One-Click Demo Accounts
        </p>
        <div className="grid grid-cols-3 gap-2">
          <button
            type="button"
            onClick={() => setDemoCredentials("student")}
            className={`rounded-lg border px-2.5 py-2 text-xs font-semibold transition-all ${
              email === "student@example.com"
                ? "border-accent-500 bg-accent-50 text-accent-700 shadow-sm"
                : "border-slate-200 bg-slate-50 hover:bg-slate-100 text-slate-700"
            }`}
          >
            🎓 Student
          </button>
          <button
            type="button"
            onClick={() => setDemoCredentials("teacher")}
            className={`rounded-lg border px-2.5 py-2 text-xs font-semibold transition-all ${
              email === "teacher@example.com"
                ? "border-secondary-500 bg-secondary-50 text-secondary-700 shadow-sm"
                : "border-slate-200 bg-slate-50 hover:bg-slate-100 text-slate-700"
            }`}
          >
            👩‍🏫 Teacher
          </button>
          <button
            type="button"
            onClick={() => setDemoCredentials("admin")}
            className={`rounded-lg border px-2.5 py-2 text-xs font-semibold transition-all ${
              email === "admin@example.com"
                ? "border-emerald-500 bg-emerald-50 text-emerald-700 shadow-sm"
                : "border-slate-200 bg-slate-50 hover:bg-slate-100 text-slate-700"
            }`}
          >
            🛡️ Admin
          </button>
        </div>
      </div>

      {/* Form Container */}
      <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
        {error && (
          <div className="mb-4 flex items-center gap-2 rounded-xl border border-rose-200 bg-rose-50 p-3 text-xs font-medium text-rose-700">
            <AlertCircle className="h-4 w-4 shrink-0 text-rose-600" />
            <span>{error}</span>
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-xs font-semibold text-slate-700 mb-1">Email Address</label>
            <input
              type="email"
              required
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="name@example.com"
              className="w-full rounded-xl border border-slate-200 bg-white px-3.5 py-2.5 text-sm text-slate-900 outline-none transition focus:border-brand-500 focus:ring-2 focus:ring-brand-500/20"
            />
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-700 mb-1">Password</label>
            <input
              type="password"
              required
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="••••••••"
              className="w-full rounded-xl border border-slate-200 bg-white px-3.5 py-2.5 text-sm text-slate-900 outline-none transition focus:border-brand-500 focus:ring-2 focus:ring-brand-500/20"
            />
          </div>

          <button
            type="submit"
            disabled={isSubmitting || isLoading}
            className="flex w-full items-center justify-center gap-2 rounded-xl bg-brand-600 px-4 py-2.5 text-sm font-semibold text-white shadow-sm transition hover:bg-brand-700 focus:outline-none focus:ring-2 focus:ring-brand-500/20 disabled:opacity-50"
          >
            {isSubmitting ? (
              <>
                <Loader2 className="h-4 w-4 animate-spin" />
                <span>Authenticating...</span>
              </>
            ) : (
              <span>Sign In</span>
            )}
          </button>
        </form>

        <div className="mt-5 text-center text-xs text-slate-500">
          Don&apos;t have an account?{" "}
          <Link href="/register" className="font-semibold text-brand-600 hover:text-brand-700">
            Create an account
          </Link>
        </div>
      </div>
    </div>
  );
}

export default function LoginPage() {
  return (
    <div className="flex min-h-screen items-center justify-center bg-slate-50 px-4 py-12">
      <Suspense fallback={<div className="text-center p-8 text-slate-400">Loading SPECTRA Login...</div>}>
        <LoginForm />
      </Suspense>
    </div>
  );
}
