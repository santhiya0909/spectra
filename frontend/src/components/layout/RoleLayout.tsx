"use client";

import React, { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { useAuth } from "@/lib/auth";
import { Navbar } from "./Navbar";
import { Sidebar } from "./Sidebar";
import { Loader2, Sparkles } from "lucide-react";

interface RoleLayoutProps {
  allowedRoles: Array<"STUDENT" | "TEACHER" | "ADMIN">;
  children: React.ReactNode;
}

export const RoleLayout: React.FC<RoleLayoutProps> = ({ allowedRoles, children }) => {
  const { user, isLoading } = useAuth();
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const router = useRouter();

  useEffect(() => {
    if (!isLoading) {
      if (!user) {
        router.push("/login");
      } else if (!allowedRoles.includes(user.role)) {
        if (user.role === "STUDENT") router.push("/student/dashboard");
        else if (user.role === "TEACHER") router.push("/teacher/dashboard");
        else router.push("/admin/dashboard");
      }
    }
  }, [user, isLoading, allowedRoles, router]);

  if (isLoading || !user) {
    return (
      <div className="relative flex h-screen w-screen flex-col items-center justify-center bg-[#F8FAFC] dark:bg-[#060913] text-slate-900 dark:text-white overflow-hidden transition-colors">
        {/* Ambient lighting */}
        <div className="absolute top-1/4 left-1/3 w-96 h-96 bg-cyan-500/10 rounded-full blur-[120px] pointer-events-none" />
        <div className="absolute bottom-1/4 right-1/3 w-96 h-96 bg-purple-500/10 rounded-full blur-[120px] pointer-events-none" />
        
        <div className="relative z-10 flex flex-col items-center gap-4 text-center">
          <div className="flex h-14 w-14 items-center justify-center rounded-2xl bg-gradient-to-tr from-indigo-600 via-purple-600 to-cyan-400 text-white shadow-[0_0_35px_rgba(6,182,212,0.4)] animate-pulse">
            <Sparkles className="h-7 w-7" />
          </div>
          <div className="space-y-1">
            <h2 className="text-xl font-bold tracking-tight text-slate-900 dark:text-white">SPECTRA AI</h2>
            <p className="text-xs text-slate-500 dark:text-slate-400 font-medium">Initializing adaptive cognitive environment...</p>
          </div>
          <Loader2 className="h-5 w-5 animate-spin text-cyan-600 dark:text-cyan-400 mt-2" />
        </div>
      </div>
    );
  }

  return (
    <div className="relative flex min-h-screen flex-col bg-[#F8FAFC] dark:bg-[#060913] bg-cosmic-grid text-slate-900 dark:text-slate-100 selection:bg-cyan-500 selection:text-black transition-colors duration-300">
      {/* Subtle ambient lighting orbs */}
      <div className="fixed -top-40 -left-40 w-[500px] h-[500px] bg-cyan-500/[0.05] dark:bg-cyan-500/[0.07] rounded-full blur-[140px] pointer-events-none" />
      <div className="fixed top-1/3 -right-40 w-[500px] h-[500px] bg-purple-500/[0.04] dark:bg-purple-500/[0.06] rounded-full blur-[140px] pointer-events-none" />
      <div className="fixed -bottom-40 left-1/3 w-[600px] h-[500px] bg-indigo-500/[0.04] dark:bg-indigo-500/[0.05] rounded-full blur-[160px] pointer-events-none" />

      <Navbar onToggleSidebar={() => setSidebarOpen((prev) => !prev)} />
      
      <div className="relative z-10 flex flex-1">
        <Sidebar isOpen={sidebarOpen} onClose={() => setSidebarOpen(false)} />
        <main className="flex-1 overflow-x-hidden p-4 sm:p-6 lg:p-8">
          <div className="mx-auto max-w-7xl">{children}</div>
        </main>
      </div>
    </div>
  );
};
