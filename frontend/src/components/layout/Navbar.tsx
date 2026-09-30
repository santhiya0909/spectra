"use client";

import React from "react";
import Link from "next/link";
import { useAuth } from "@/lib/auth";
import { ThemeToggle } from "@/components/theme/ThemeToggle";
import { LogOut, Sparkles, Bell, Shield, Zap } from "lucide-react";

interface NavbarProps {
  onToggleSidebar?: () => void;
}

export const Navbar: React.FC<NavbarProps> = ({ onToggleSidebar }) => {
  const { user, logout } = useAuth();

  return (
    <header className="sticky top-0 z-30 flex h-16 w-full items-center justify-between border-b border-slate-200/80 dark:border-white/[0.08] bg-white/80 dark:bg-[#070A14]/85 px-4 backdrop-blur-2xl md:px-6 transition-colors">
      <div className="flex items-center gap-3">
        <button
          onClick={onToggleSidebar}
          aria-label="Toggle navigation menu"
          className="flex h-10 w-10 items-center justify-center rounded-xl text-slate-600 dark:text-slate-400 hover:bg-slate-100 dark:hover:bg-white/5 hover:text-slate-900 dark:hover:text-white md:hidden transition"
        >
          <svg className="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
          </svg>
        </button>

        <Link href="/" className="flex items-center gap-3 group">
          <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-gradient-to-tr from-cyan-500 via-indigo-600 to-purple-600 text-white shadow-[0_0_20px_rgba(6,182,212,0.4)] transition-transform group-hover:scale-105">
            <Sparkles className="h-5 w-5" />
          </div>
          <div className="flex items-center gap-2">
            <span className="text-xl font-black tracking-tight text-slate-900 dark:text-white group-hover:text-cyan-600 dark:group-hover:text-cyan-400 transition-colors">
              SPECTRA
            </span>
            <span className="hidden sm:inline-flex items-center gap-1.5 px-2 py-0.5 rounded-full text-[10px] font-bold uppercase tracking-wider bg-cyan-500/10 text-cyan-700 dark:text-cyan-300 border border-cyan-500/25 shadow-sm dark:shadow-[0_0_10px_rgba(6,182,212,0.2)]">
              <span className="w-1.5 h-1.5 rounded-full bg-cyan-500 dark:bg-cyan-400 animate-pulse" />
              AI Cognitive
            </span>
          </div>
        </Link>
      </div>

      {/* Middle/Center status highlight */}
      <div className="hidden lg:flex items-center gap-2 px-3.5 py-1 rounded-full bg-slate-100/80 dark:bg-white/[0.03] border border-slate-200/80 dark:border-white/[0.06] text-xs font-medium text-slate-600 dark:text-slate-400">
        <Zap className="w-3.5 h-3.5 text-cyan-600 dark:text-cyan-400" />
        <span>Adaptive Neural Guidance:</span>
        <span className="text-emerald-600 dark:text-emerald-400 font-semibold">Active &bull; Round 2 Ready</span>
      </div>

      <div className="flex items-center gap-2 sm:gap-3 md:gap-4">
        {/* Dark Mode / Light Mode Toggle Button */}
        <ThemeToggle />

        {user ? (
          <>
            <div className="hidden text-right sm:block">
              <p className="text-xs font-bold text-slate-900 dark:text-white tracking-wide">{user.name}</p>
              <div className="flex items-center justify-end gap-1.5">
                <span
                  className={`inline-block h-1.5 w-1.5 rounded-full ${
                    user.role === "STUDENT"
                      ? "bg-cyan-500 dark:bg-cyan-400 shadow-[0_0_8px_#22d3ee]"
                      : user.role === "TEACHER"
                      ? "bg-purple-500 dark:bg-purple-400 shadow-[0_0_8px_#c084fc]"
                      : "bg-emerald-500 dark:bg-emerald-400 shadow-[0_0_8px_#34d399]"
                  }`}
                />
                <p className="text-[10px] font-semibold text-slate-500 dark:text-slate-400 uppercase tracking-wider">
                  {user.role}
                </p>
              </div>
            </div>

            <div className="flex items-center gap-2">
              <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-gradient-to-br from-indigo-500/20 to-purple-500/20 text-cyan-700 dark:text-cyan-300 font-bold text-xs border border-slate-200 dark:border-white/10 shadow-inner">
                {user.name.charAt(0).toUpperCase()}
              </div>

              <button
                onClick={logout}
                title="Sign Out"
                className="flex h-9 w-9 items-center justify-center rounded-xl text-slate-500 dark:text-slate-400 hover:bg-rose-500/10 hover:text-rose-600 dark:hover:text-rose-400 border border-transparent hover:border-rose-500/20 transition-all"
              >
                <LogOut className="h-4 w-4" />
              </button>
            </div>
          </>
        ) : (
          <div className="flex items-center gap-2.5">
            <Link
              href="/login"
              className="rounded-xl px-4 py-2 text-xs font-semibold text-slate-600 dark:text-slate-300 hover:text-slate-900 dark:hover:text-white hover:bg-slate-100 dark:hover:bg-white/5 transition"
            >
              Sign In
            </Link>
            <Link
              href="/register"
              className="rounded-xl bg-gradient-to-r from-cyan-500 to-indigo-600 px-4 py-2 text-xs font-bold text-white shadow-[0_0_20px_rgba(6,182,212,0.3)] hover:brightness-110 transition"
            >
              Get Started
            </Link>
          </div>
        )}
      </div>
    </header>
  );
};
