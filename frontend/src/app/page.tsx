
"use client";

import React, { useEffect } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { useAuth } from "@/lib/auth";
import {
  Sparkles,
  BrainCircuit,
  GraduationCap,
  BarChart3,
  Users,
} from "lucide-react";

export default function HomePage() {
  const { user, isLoading } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (!isLoading && user) {
      const role = user.role?.toUpperCase();

      if (role === "STUDENT") {
        router.replace("/student/dashboard");
      } else if (role === "TEACHER") {
        router.replace("/teacher/dashboard");
      } else if (role === "ADMIN") {
        router.replace("/admin/dashboard");
      }
    }
  }, [user, isLoading, router]);

  if (isLoading || user) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-slate-50">
        <p className="text-slate-600">Loading SPECTRA...</p>
      </div>
    );
  }

  return (
    <div className="flex min-h-screen flex-col bg-slate-50">
      {/* Top Bar */}
      <header className="flex h-16 items-center justify-between border-b border-slate-200 bg-white/90 px-6 backdrop-blur">
        <div className="flex items-center gap-2.5">
          <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-gradient-to-tr from-brand-600 via-secondary-500 to-accent-500 text-white shadow-md shadow-brand-500/20">
            <Sparkles className="h-5 w-5" />
          </div>
          <span className="text-xl font-bold tracking-tight text-slate-900">
            SPECTRA
          </span>
        </div>

        <div className="flex items-center gap-3">
          <Link
            href="/login"
            className="rounded-lg px-4 py-2 text-sm font-semibold text-slate-700 hover:bg-slate-100"
          >
            Sign In
          </Link>

          <Link
            href="/register"
            className="rounded-lg bg-brand-600 px-4 py-2 text-sm font-semibold text-white shadow hover:bg-brand-700"
          >
            Register
          </Link>
        </div>
      </header>

      {/* Hero Section */}
      <main className="mx-auto flex w-full max-w-5xl flex-1 flex-col items-center justify-center px-4 py-16 text-center">
        <div className="mb-6 inline-flex items-center gap-2 rounded-full border border-brand-200 bg-brand-50 px-3 py-1 text-xs font-semibold text-brand-700">
          <BrainCircuit className="h-4 w-4" />
          Next-Generation Adaptive Learning Engine
        </div>

        <h1 className="text-4xl font-extrabold leading-tight tracking-tight text-slate-900 sm:text-6xl">
          Intelligent Education with
          <br />
          <span className="bg-gradient-to-r from-brand-600 via-secondary-600 to-accent-600 bg-clip-text text-transparent">
            Continuous Personalization
          </span>
        </h1>

        <p className="mt-6 max-w-2xl text-lg leading-relaxed text-slate-600">
          SPECTRA analyzes student assessment responses, pinpoints
          individual knowledge gaps, and continuously recommends
          targeted practice to drive rapid topic mastery.
        </p>

        {/* Demo Login Cards */}
        <div className="mt-10 grid w-full max-w-3xl grid-cols-1 gap-4 text-left sm:grid-cols-3">
          {/* Student */}
          <Link
            href="/login?role=student"
            className="group rounded-2xl border border-slate-200 bg-white p-5 shadow-sm transition-all hover:border-brand-300 hover:shadow-md"
          >
            <div className="mb-3 flex h-10 w-10 items-center justify-center rounded-xl bg-accent-50 text-accent-600 transition-transform group-hover:scale-105">
              <GraduationCap className="h-5 w-5" />
            </div>
            <h3 className="font-bold text-slate-900">Student Portal</h3>
            <p className="mt-1 text-xs text-slate-500">
              student@example.com
            </p>
            <div className="mt-3 flex items-center text-xs font-semibold text-brand-600 transition-transform group-hover:translate-x-1">
              Launch Dashboard →
            </div>
          </Link>

          {/* Teacher */}
          <Link
            href="/login?role=teacher"
            className="group rounded-2xl border border-slate-200 bg-white p-5 shadow-sm transition-all hover:border-secondary-300 hover:shadow-md"
          >
            <div className="mb-3 flex h-10 w-10 items-center justify-center rounded-xl bg-secondary-50 text-secondary-600 transition-transform group-hover:scale-105">
              <Users className="h-5 w-5" />
            </div>
            <h3 className="font-bold text-slate-900">Teacher Portal</h3>
            <p className="mt-1 text-xs text-slate-500">
              teacher@example.com
            </p>
            <div className="mt-3 flex items-center text-xs font-semibold text-secondary-600 transition-transform group-hover:translate-x-1">
              Class Analytics →
            </div>
          </Link>

          {/* Admin */}
          <Link
            href="/login?role=admin"
            className="group rounded-2xl border border-slate-200 bg-white p-5 shadow-sm transition-all hover:border-emerald-300 hover:shadow-md"
          >
            <div className="mb-3 flex h-10 w-10 items-center justify-center rounded-xl bg-emerald-50 text-emerald-600 transition-transform group-hover:scale-105">
              <BarChart3 className="h-5 w-5" />
            </div>
            <h3 className="font-bold text-slate-900">Admin Console</h3>
            <p className="mt-1 text-xs text-slate-500">
              admin@example.com
            </p>
            <div className="mt-3 flex items-center text-xs font-semibold text-emerald-600 transition-transform group-hover:translate-x-1">
              System Console →
            </div>
          </Link>
        </div>

        {/* Learning Cycle */}
        <div className="mt-16 w-full rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
          <h2 className="mb-4 text-sm font-bold uppercase tracking-wider text-slate-400">
            The SPECTRA Closed-Loop Learning Cycle
          </h2>

          <div className="grid grid-cols-2 gap-2 text-xs font-semibold text-slate-700 md:grid-cols-6">
            <div className="rounded-xl border border-slate-200 bg-slate-50 p-3">
              1. ASSESS
            </div>
            <div className="rounded-xl border border-slate-200 bg-slate-50 p-3">
              2. ANALYZE
            </div>
            <div className="rounded-xl border border-brand-200 bg-brand-50 p-3 text-brand-700">
              3. PERSONALIZE
            </div>
            <div className="rounded-xl border border-slate-200 bg-slate-50 p-3">
              4. IMPROVE
            </div>
            <div className="rounded-xl border border-slate-200 bg-slate-50 p-3">
              5. REASSESS
            </div>
            <div className="rounded-xl border border-emerald-200 bg-emerald-50 p-3 text-emerald-700">
              6. UPDATE PATH
            </div>
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="border-t border-slate-200 bg-white py-6 text-center text-xs text-slate-500">
        SPECTRA – Intelligent Educational System
        {" "}• Production Full-Stack Architecture
      </footer>
    </div>
  );
}