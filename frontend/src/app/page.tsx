"use client";

import React, { useEffect } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { useAuth } from "@/lib/auth";
import {
  Sparkles,
  ArrowRight,
  BrainCircuit,
  Compass,
  GraduationCap,
  Target,
  BarChart3,
  CheckCircle2,
  Users
} from "lucide-react";

export default function HomePage() {
  const { user, isLoading } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (!isLoading && user) {
      if (user.role === "STUDENT") router.push("/student/dashboard");
      else if (user.role === "TEACHER") router.push("/teacher/dashboard");
      else if (user.role === "ADMIN") router.push("/admin/dashboard");
    }
  }, [user, isLoading, router]);

  return (
    <div className="min-h-screen bg-slate-50 flex flex-col">
      {/* Top Bar */}
      <header className="flex h-16 items-center justify-between border-b border-slate-200 bg-white/90 px-6 backdrop-blur">
        <div className="flex items-center gap-2.5">
          <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-gradient-to-tr from-brand-600 via-secondary-500 to-accent-500 text-white shadow-md shadow-brand-500/20">
            <Sparkles className="h-5 w-5" />
          </div>
          <span className="text-xl font-bold tracking-tight text-slate-900">SPECTRA</span>
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
      <main className="flex-1 flex flex-col items-center justify-center px-4 py-16 text-center max-w-5xl mx-auto">
        <div className="inline-flex items-center gap-2 rounded-full border border-brand-200 bg-brand-50 px-3 py-1 text-xs font-semibold text-brand-700 mb-6">
          <BrainCircuit className="h-4 w-4" /> Next-Generation Adaptive Learning Engine
        </div>

        <h1 className="text-4xl sm:text-6xl font-extrabold tracking-tight text-slate-900 leading-tight">
          Intelligent Education with <br />
          <span className="bg-gradient-to-r from-brand-600 via-secondary-600 to-accent-600 bg-clip-text text-transparent">
            Continuous Personalization
          </span>
        </h1>

        <p className="mt-6 max-w-2xl text-lg text-slate-600 leading-relaxed">
          SPECTRA analyzes student assessment responses, pinpoints individual knowledge gaps,
          and continuously recommends targeted practice to drive rapid topic mastery.
        </p>

        {/* Demo Fast Login Cards */}
        <div className="mt-10 grid grid-cols-1 sm:grid-cols-3 gap-4 w-full max-w-3xl text-left">
          <Link
            href="/login?role=student"
            className="group rounded-2xl border border-slate-200 bg-white p-5 shadow-sm hover:border-brand-300 hover:shadow-md transition-all"
          >
            <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-accent-50 text-accent-600 mb-3 group-hover:scale-105 transition-transform">
              <GraduationCap className="h-5 w-5" />
            </div>
            <h3 className="font-bold text-slate-900">Student Portal</h3>
            <p className="text-xs text-slate-500 mt-1">student@example.com</p>
            <div className="mt-3 flex items-center text-xs font-semibold text-brand-600 group-hover:translate-x-1 transition-transform">
              Launch Dashboard →
            </div>
          </Link>

          <Link
            href="/login?role=teacher"
            className="group rounded-2xl border border-slate-200 bg-white p-5 shadow-sm hover:border-secondary-300 hover:shadow-md transition-all"
          >
            <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-secondary-50 text-secondary-600 mb-3 group-hover:scale-105 transition-transform">
              <Users className="h-5 w-5" />
            </div>
            <h3 className="font-bold text-slate-900">Teacher Portal</h3>
            <p className="text-xs text-slate-500 mt-1">teacher@example.com</p>
            <div className="mt-3 flex items-center text-xs font-semibold text-secondary-600 group-hover:translate-x-1 transition-transform">
              Class Analytics →
            </div>
          </Link>

          <Link
            href="/login?role=admin"
            className="group rounded-2xl border border-slate-200 bg-white p-5 shadow-sm hover:border-emerald-300 hover:shadow-md transition-all"
          >
            <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-emerald-50 text-emerald-600 mb-3 group-hover:scale-105 transition-transform">
              <BarChart3 className="h-5 w-5" />
            </div>
            <h3 className="font-bold text-slate-900">Admin Console</h3>
            <p className="text-xs text-slate-500 mt-1">admin@example.com</p>
            <div className="mt-3 flex items-center text-xs font-semibold text-emerald-600 group-hover:translate-x-1 transition-transform">
              System Console →
            </div>
          </Link>
        </div>

        {/* The Closed Loop Flow Diagram */}
        <div className="mt-16 w-full rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
          <h2 className="text-sm font-bold uppercase tracking-wider text-slate-400 mb-4">
            The SPECTRA Closed-Loop Learning Cycle
          </h2>
          <div className="grid grid-cols-2 md:grid-cols-6 gap-2 text-xs font-semibold text-slate-700">
            <div className="p-3 rounded-xl bg-slate-50 border border-slate-200">1. ASSESS</div>
            <div className="p-3 rounded-xl bg-slate-50 border border-slate-200">2. ANALYZE</div>
            <div className="p-3 rounded-xl bg-brand-50 border border-brand-200 text-brand-700">3. PERSONALIZE</div>
            <div className="p-3 rounded-xl bg-slate-50 border border-slate-200">4. IMPROVE</div>
            <div className="p-3 rounded-xl bg-slate-50 border border-slate-200">5. REASSESS</div>
            <div className="p-3 rounded-xl bg-emerald-50 border border-emerald-200 text-emerald-700">6. UPDATE PATH</div>
          </div>
        </div>
      </main>

      <footer className="border-t border-slate-200 py-6 text-center text-xs text-slate-500 bg-white">
        SPECTRA – Intelligent Educational System &bull; Production Full-Stack Architecture
      </footer>
    </div>
  );
}
