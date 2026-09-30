"use client";

import React from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { useAuth } from "@/lib/auth";
import {
  LayoutDashboard,
  BookOpen,
  HelpCircle,
  TrendingUp,
  Compass,
  Bot,
  UserCheck,
  Users,
  AlertTriangle,
  FolderKanban,
  FileQuestion,
  Shield,
  Layers,
  Dna,
  Puzzle,
  Gamepad2,
  Sparkles,
} from "lucide-react";
import type { LucideIcon } from "lucide-react";

interface SidebarProps {
  isOpen: boolean;
  onClose: () => void;
}

interface SidebarLink {
  label: string;
  href: string;
  icon: LucideIcon;
  badge?: string;
}

export const Sidebar: React.FC<SidebarProps> = ({ isOpen, onClose }) => {
  const pathname = usePathname();
  const { user } = useAuth();

  if (!user) return null;

  const role = user.role?.toUpperCase() ?? "";

  const studentLinks: SidebarLink[] = [
    { label: "Overview", href: "/student/dashboard", icon: LayoutDashboard },
    { label: "Knowledge DNA", href: "/student/knowledge-dna", icon: Dna, badge: "AI" },
    { label: "Learn & Subjects", href: "/student/subjects", icon: BookOpen },
    { label: "My Learning Path", href: "/student/learning-plan", icon: Compass },
    { label: "Adaptive Quizzes", href: "/student/quizzes", icon: HelpCircle },
    { label: "Puzzle Lab", href: "/student/puzzles", icon: Gamepad2, badge: "Play" },
    { label: "AI Socratic Tutor", href: "/student/ai-tutor", icon: Bot },
    { label: "Achievements & Profile", href: "/student/profile", icon: UserCheck },
  ];

  const teacherLinks: SidebarLink[] = [
    { label: "Class Overview", href: "/teacher/dashboard", icon: LayoutDashboard },
    { label: "Students Roster", href: "/teacher/students", icon: Users },
    { label: "Topic Gap Analytics", href: "/teacher/analytics", icon: Layers },
    { label: "Intervention Alerts", href: "/teacher/alerts", icon: AlertTriangle },
  ];

  const adminLinks: SidebarLink[] = [
    { label: "Admin Console", href: "/admin/dashboard", icon: Shield },
    { label: "User Management", href: "/admin/users", icon: Users },
    { label: "Curriculum Subjects", href: "/admin/subjects", icon: BookOpen },
    { label: "Topics Management", href: "/admin/topics", icon: Layers },
    { label: "Question Bank", href: "/admin/questions", icon: FileQuestion },
    { label: "Quiz Catalog", href: "/admin/quizzes", icon: FolderKanban },
  ];

  const navLinks: SidebarLink[] =
    role === "STUDENT"
      ? studentLinks
      : role === "TEACHER"
      ? teacherLinks
      : role === "ADMIN"
      ? adminLinks
      : [];

  const sectionTitle =
    role === "STUDENT"
      ? "Learning Matrix"
      : role === "TEACHER"
      ? "Instructor Console"
      : role === "ADMIN"
      ? "System Control"
      : "Navigation";

  return (
    <>
      {/* Mobile Backdrop */}
      {isOpen && (
        <div
          onClick={onClose}
          className="fixed inset-0 z-40 bg-black/70 backdrop-blur-md md:hidden"
        />
      )}

      {/* Sidebar Panel */}
      <aside
        className={`fixed inset-y-0 left-0 z-40 flex w-64 flex-col border-r border-slate-200/80 dark:border-white/[0.08] bg-white/95 dark:bg-[#070A14]/90 backdrop-blur-2xl pt-16 transition-transform duration-300 ease-in-out md:static md:translate-x-0 ${
          isOpen ? "translate-x-0" : "-translate-x-full"
        }`}
      >
        <div className="flex flex-1 flex-col gap-1 overflow-y-auto px-3.5 py-5">
          <div className="mb-2 px-3 py-1 flex items-center justify-between">
            <p className="text-[10px] font-extrabold uppercase tracking-widest text-slate-500 dark:text-slate-400">
              {sectionTitle}
            </p>
            <span className="w-1.5 h-1.5 rounded-full bg-cyan-500 dark:bg-cyan-400/50" />
          </div>

          <nav className="flex flex-1 flex-col gap-1.5">
            {navLinks.map((item) => {
              const href = typeof item.href === "string" ? item.href.trim() : "";
              if (!href) return null;

              const Icon = item.icon;
              const isActive =
                pathname === href ||
                (href !== "/student/dashboard" && pathname.startsWith(href));

              return (
                <Link
                  key={href}
                  href={href}
                  onClick={onClose}
                  aria-current={isActive ? "page" : undefined}
                  className={`group relative flex items-center justify-between rounded-2xl px-3.5 py-2.5 text-xs font-semibold transition-all duration-200 ${
                    isActive
                      ? "bg-cyan-500/10 dark:bg-gradient-to-r dark:from-cyan-500/15 dark:via-indigo-500/10 dark:to-transparent text-cyan-900 dark:text-white border border-cyan-500/30 shadow-sm dark:shadow-[0_0_20px_rgba(6,182,212,0.15)]"
                      : "text-slate-600 dark:text-slate-400 hover:bg-slate-100 dark:hover:bg-white/[0.04] hover:text-slate-900 dark:hover:text-slate-200 border border-transparent"
                  }`}
                >
                  {/* Left accent bar on active */}
                  {isActive && (
                    <span className="absolute left-0 top-1/2 -translate-y-1/2 w-1 h-5 rounded-r-full bg-cyan-500 dark:bg-cyan-400 shadow-[0_0_8px_#22d3ee]" />
                  )}

                  <div className="flex items-center gap-3">
                    <Icon
                      className={`h-4 w-4 transition-colors ${
                        isActive
                          ? "text-cyan-600 dark:text-cyan-400"
                          : "text-slate-500 group-hover:text-slate-800 dark:group-hover:text-slate-300"
                      }`}
                    />
                    <span>{item.label}</span>
                  </div>

                  {item.badge && (
                    <span
                      className={`text-[9px] font-extrabold uppercase px-1.5 py-0.5 rounded-md ${
                        item.badge === "AI"
                          ? "bg-purple-500/15 dark:bg-purple-500/20 text-purple-700 dark:text-purple-300 border border-purple-500/30"
                          : item.badge === "Play"
                          ? "bg-emerald-500/15 dark:bg-emerald-500/20 text-emerald-700 dark:text-emerald-300 border border-emerald-500/30 shadow-[0_0_8px_rgba(16,185,129,0.3)]"
                          : "bg-cyan-500/15 dark:bg-cyan-500/20 text-cyan-700 dark:text-cyan-300 border border-cyan-500/30"
                      }`}
                    >
                      {item.badge}
                    </span>
                  )}
                </Link>
              );
            })}
          </nav>

          {/* Quick learning loop indicator for student */}
          {role === "STUDENT" && (
            <div className="mt-auto rounded-2xl border border-slate-200/80 dark:border-white/[0.08] bg-slate-100/90 dark:bg-gradient-to-br dark:from-indigo-950/40 dark:via-[#0B1124] dark:to-cyan-950/30 p-4 shadow-sm dark:shadow-inner">
              <div className="mb-2 flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <span className="flex h-2 w-2 rounded-full bg-cyan-500 dark:bg-cyan-400 shadow-[0_0_8px_#22d3ee] animate-pulse" />
                  <span className="text-[11px] font-bold text-slate-900 dark:text-white tracking-wide">
                    Adaptive Loop Active
                  </span>
                </div>
                <Sparkles className="w-3.5 h-3.5 text-cyan-600 dark:text-cyan-400" />
              </div>
              <p className="text-[10px] leading-relaxed text-slate-600 dark:text-slate-400">
                Cognitive gap detection + real-time Knowledge DNA calculation active.
              </p>
            </div>
          )}
        </div>
      </aside>
    </>
  );
};