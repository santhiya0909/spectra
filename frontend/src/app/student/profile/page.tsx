"use client";

import React from "react";
import { useAuth } from "@/lib/auth";
import { RoleLayout } from "@/components/layout/RoleLayout";
import { Badge } from "@/components/common/Badge";
import { User, Mail, School, BookOpen, Sparkles, Shield } from "lucide-react";

export default function StudentProfilePage() {
  const { user } = useAuth();

  return (
    <RoleLayout allowedRoles={["STUDENT", "ADMIN"]}>
      <div className="mx-auto max-w-3xl space-y-6">
        <div>
          <h1 className="text-2xl font-bold tracking-tight text-slate-900 dark:text-slate-100">Student Profile</h1>
          <p className="mt-1 text-sm text-slate-500 dark:text-slate-400">
            Academic enrollment details, learning preferences, and credentials.
          </p>
        </div>

        {user && (
          <div className="rounded-3xl border border-slate-200 dark:border-white/[0.08] bg-white dark:bg-[#0B1124]/85 dark:backdrop-blur-xl p-6 sm:p-8 shadow-sm space-y-6">
            <div className="flex items-center gap-4 border-b border-slate-100 dark:border-white/[0.08] pb-6">
              <div className="flex h-16 w-16 items-center justify-center rounded-2xl bg-brand-50 dark:bg-brand-500/10 text-2xl font-black text-brand-600 border border-brand-200 dark:border-brand-500/30">
                {user.name.charAt(0).toUpperCase()}
              </div>
              <div>
                <h2 className="text-xl font-bold text-slate-900 dark:text-slate-100">{user.name}</h2>
                <p className="text-xs text-slate-500 dark:text-slate-400">{user.email}</p>
                <div className="mt-2">
                  <Badge variant="cyan" size="sm">
                    {user.role} ACCOUNT
                  </Badge>
                </div>
              </div>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 text-xs">
              <div className="rounded-2xl border border-slate-100 dark:border-white/[0.08] bg-slate-50/70 dark:bg-white/[0.03] p-4">
                <span className="block text-[11px] font-bold uppercase tracking-wider text-slate-400 dark:text-slate-500 mb-1">
                  Student Registration ID
                </span>
                <span className="text-sm font-bold text-slate-900 dark:text-slate-100">
                  {user.student_profile?.student_id || `STU-${user.id}`}
                </span>
              </div>

              <div className="rounded-2xl border border-slate-100 dark:border-white/[0.08] bg-slate-50/70 dark:bg-white/[0.03] p-4">
                <span className="block text-[11px] font-bold uppercase tracking-wider text-slate-400 dark:text-slate-500 mb-1">
                  Department / Program
                </span>
                <span className="text-sm font-bold text-slate-900 dark:text-slate-100">
                  {user.student_profile?.department || "Computer Science & Engineering"}
                </span>
              </div>

              <div className="rounded-2xl border border-slate-100 dark:border-white/[0.08] bg-slate-50/70 dark:bg-white/[0.03] p-4">
                <span className="block text-[11px] font-bold uppercase tracking-wider text-slate-400 dark:text-slate-500 mb-1">
                  Current Semester
                </span>
                <span className="text-sm font-bold text-slate-900 dark:text-slate-100">
                  Semester {user.student_profile?.semester || 4}
                </span>
              </div>

              <div className="rounded-2xl border border-slate-100 dark:border-white/[0.08] bg-slate-50/70 dark:bg-white/[0.03] p-4">
                <span className="block text-[11px] font-bold uppercase tracking-wider text-slate-400 dark:text-slate-500 mb-1">
                  Personalization Model
                </span>
                <span className="text-sm font-bold text-slate-900 dark:text-slate-100">
                  SPECTRA Adaptive Cognitive Path
                </span>
              </div>
            </div>

            <div className="rounded-2xl border border-brand-100 dark:border-brand-500/20 bg-brand-50/50 dark:bg-brand-500/[0.08] p-4">
              <div className="flex items-center gap-2 mb-1">
                <Sparkles className="h-4 w-4 text-brand-600" />
                <h4 className="text-xs font-bold text-brand-900 dark:text-brand-300">Continuous Assessment Loop</h4>
              </div>
              <p className="text-xs text-slate-600 dark:text-slate-300 leading-relaxed">
                Your performance profile dynamically recalculates topic weights after every quiz submission.
                Weak areas trigger targeted review recommendations automatically.
              </p>
            </div>
          </div>
        )}
      </div>
    </RoleLayout>
  );
}
