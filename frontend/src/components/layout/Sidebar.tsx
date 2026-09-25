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
  Lightbulb,
  Compass,
  Bot,
  UserCheck,
  Users,
  AlertTriangle,
  FolderKanban,
  FileQuestion,
  Settings,
  Shield,
  Layers
} from "lucide-react";

interface SidebarProps {
  isOpen: boolean;
  onClose: () => void;
}

export const Sidebar: React.FC<SidebarProps> = ({ isOpen, onClose }) => {
  const pathname = usePathname();
  const { user } = useAuth();

  if (!user) return null;

  const role = user.role;

  const studentLinks = [
    { label: "Dashboard", href: "/student/dashboard", icon: LayoutDashboard },
    { label: "Subjects & Lessons", href: "/student/subjects", icon: BookOpen },
    { label: "Adaptive Quizzes", href: "/student/quizzes", icon: HelpCircle },
    { label: "Progress Analytics", href: "/student/progress", icon: TrendingUp },
    { label: "Smart Recommendations", href: "/student/recommendations", icon: Lightbulb },
    { label: "Learning Path", href: "/student/learning-plan", icon: Compass },
    { label: "AI Socratic Tutor", href: "/student/ai-tutor", icon: Bot },
    { label: "My Profile", href: "/student/profile", icon: UserCheck },
  ];

  const teacherLinks = [
    { label: "Class Overview", href: "/teacher/dashboard", icon: LayoutDashboard },
    { label: "Students Roster", href: "/teacher/students", icon: Users },
    { label: "Topic Gap Analytics", href: "/teacher/analytics", icon: Layers },
    { label: "Intervention Alerts", href: "/teacher/alerts", icon: AlertTriangle },
  ];

  const adminLinks = [
    { label: "Admin Console", href: "/admin/dashboard", icon: Shield },
    { label: "User Management", href: "/admin/users", icon: Users },
    { label: "Curriculum Subjects", href: "/admin/subjects", icon: BookOpen },
    { label: "Topics Management", href: "/admin/topics", icon: Layers },
    { label: "Question Bank", href: "/admin/questions", icon: FileQuestion },
    { label: "Quiz Catalog", href: "/admin/quizzes", icon: FolderKanban },
  ];

  const navLinks = role === "STUDENT" ? studentLinks : role === "TEACHER" ? teacherLinks : adminLinks;

  return (
    <>
      {/* Mobile Backdrop */}
      {isOpen && (
        <div
          onClick={onClose}
          className="fixed inset-0 z-40 bg-slate-900/50 backdrop-blur-sm md:hidden"
        />
      )}

      {/* Sidebar Panel */}
      <aside
        className={`fixed inset-y-0 left-0 z-40 flex w-64 flex-col border-r border-slate-200 bg-white pt-16 transition-transform duration-200 ease-in-out md:static md:translate-x-0 ${
          isOpen ? "translate-x-0" : "-translate-x-full"
        }`}
      >
        <div className="flex flex-1 flex-col gap-1 overflow-y-auto px-3 py-4">
          <div className="mb-2 px-3 py-1">
            <p className="text-[11px] font-bold uppercase tracking-wider text-slate-400">
              {role === "STUDENT" ? "Learning Hub" : role === "TEACHER" ? "Instructor Portal" : "System Administration"}
            </p>
          </div>

          <nav className="flex flex-1 flex-col gap-1">
            {navLinks.map((item) => {
              const Icon = item.icon;
              const isActive = pathname === item.href || (item.href !== "/student/dashboard" && pathname.startsWith(item.href));

              return (
                <Link
                  key={item.href}
                  href={item.href}
                  onClick={onClose}
                  className={`group flex items-center gap-3 rounded-lg px-3 py-2.5 text-sm font-medium transition-all ${
                    isActive
                      ? "bg-brand-50 text-brand-700 shadow-sm"
                      : "text-slate-600 hover:bg-slate-50 hover:text-slate-900"
                  }`}
                >
                  <Icon
                    className={`h-4 w-4 transition-colors ${
                      isActive ? "text-brand-600" : "text-slate-400 group-hover:text-slate-600"
                    }`}
                  />
                  <span>{item.label}</span>
                </Link>
              );
            })}
          </nav>

          {/* Quick learning loop indicator for student */}
          {role === "STUDENT" && (
            <div className="mt-auto rounded-xl border border-brand-100 bg-gradient-to-br from-brand-50 to-indigo-50/40 p-3.5">
              <div className="flex items-center gap-2 mb-1.5">
                <span className="flex h-2 w-2 rounded-full bg-brand-500 animate-pulse" />
                <span className="text-xs font-semibold text-brand-900">Adaptive Loop Active</span>
              </div>
              <p className="text-[11px] leading-relaxed text-slate-600">
                Assess → Analyze → Personalize → Practice → Reassess.
              </p>
            </div>
          )}
        </div>
      </aside>
    </>
  );
};
