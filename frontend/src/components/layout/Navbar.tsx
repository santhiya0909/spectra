"use client";

import React from "react";
import Link from "next/link";
import { useAuth } from "@/lib/auth";
import { LogOut, User as UserIcon, Bell, Sparkles, BookOpen } from "lucide-react";

interface NavbarProps {
  onToggleSidebar?: () => void;
}

export const Navbar: React.FC<NavbarProps> = ({ onToggleSidebar }) => {
  const { user, logout } = useAuth();

  return (
    <header className="sticky top-0 z-30 flex h-16 w-full items-center justify-between border-b border-slate-200 bg-white/95 px-4 backdrop-blur md:px-6">
      <div className="flex items-center gap-3">
        <button
          onClick={onToggleSidebar}
          aria-label="Toggle navigation menu"
          className="flex h-10 w-10 items-center justify-center rounded-lg text-slate-600 hover:bg-slate-100 md:hidden"
        >
          <svg className="h-6 w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
          </svg>
        </button>

        <Link href="/" className="flex items-center gap-2.5">
          <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-gradient-to-tr from-brand-600 via-secondary-500 to-accent-500 text-white shadow-md shadow-brand-500/20">
            <Sparkles className="h-5 w-5" />
          </div>
          <div>
            <span className="text-xl font-bold tracking-tight text-slate-900">
              SPECTRA
            </span>
            <span className="hidden text-xs font-semibold uppercase tracking-wider text-brand-600 sm:inline ml-2 px-1.5 py-0.5 rounded bg-brand-50 border border-brand-100">
              EdTech AI
            </span>
          </div>
        </Link>
      </div>

      <div className="flex items-center gap-3 md:gap-4">
        {user ? (
          <>
            <div className="hidden text-right sm:block">
              <p className="text-sm font-semibold text-slate-900">{user.name}</p>
              <div className="flex items-center justify-end gap-1.5">
                <span className={`inline-block h-2 w-2 rounded-full ${
                  user.role === "STUDENT" ? "bg-accent-500" : user.role === "TEACHER" ? "bg-secondary-500" : "bg-emerald-500"
                }`} />
                <p className="text-xs font-medium text-slate-500 capitalize">{user.role.toLowerCase()}</p>
              </div>
            </div>

            <div className="flex items-center gap-2">
              <div className="flex h-9 w-9 items-center justify-center rounded-full bg-slate-100 text-slate-700 font-semibold border border-slate-200">
                {user.name.charAt(0).toUpperCase()}
              </div>

              <button
                onClick={logout}
                title="Sign Out"
                className="flex h-9 w-9 items-center justify-center rounded-lg text-slate-500 hover:bg-rose-50 hover:text-rose-600 transition-colors"
              >
                <LogOut className="h-4 w-4" />
              </button>
            </div>
          </>
        ) : (
          <div className="flex items-center gap-2">
            <Link
              href="/login"
              className="rounded-lg px-3.5 py-2 text-sm font-medium text-slate-700 hover:bg-slate-100"
            >
              Sign In
            </Link>
            <Link
              href="/register"
              className="rounded-lg bg-brand-600 px-3.5 py-2 text-sm font-medium text-white shadow hover:bg-brand-700"
            >
              Get Started
            </Link>
          </div>
        )}
      </div>
    </header>
  );
};
