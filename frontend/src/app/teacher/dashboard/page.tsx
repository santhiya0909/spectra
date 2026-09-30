"use client";

import React from "react";
import Link from "next/link";
import { useQuery } from "@tanstack/react-query";
import { teacherService, TeacherDashboardData } from "@/services/teacher.service";
import { RoleLayout } from "@/components/layout/RoleLayout";
import { StatCard } from "@/components/common/StatCard";
import { Badge } from "@/components/common/Badge";
import { ProgressBar } from "@/components/common/ProgressBar";
import {
  Users,
  Award,
  CheckCircle2,
  AlertTriangle,
  ArrowRight,
  Layers,
  BookOpen,
  Sparkles
} from "lucide-react";

export default function TeacherDashboardPage() {
  const { data: dash, isLoading } = useQuery<TeacherDashboardData>({
    queryKey: ["teacherDashboard"],
    queryFn: teacherService.getDashboard,
  });

  return (
    <RoleLayout allowedRoles={["TEACHER", "ADMIN"]}>
      <div className="space-y-6">
        <div>
          <h1 className="text-2xl font-bold tracking-tight text-slate-900 dark:text-white">Instructor &amp; Class Overview</h1>
          <p className="mt-1 text-sm text-slate-500 dark:text-slate-400">
            Real-time classroom telemetry, knowledge gap detection, and student risk intervention alerts.
          </p>
        </div>

        {/* Metric Cards */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          <StatCard
            title="Total Students"
            value={dash?.total_students || 0}
            subtitle="Enrolled active learners"
            icon={Users}
            color="brand"
          />
          <StatCard
            title="Class Average"
            value={`${dash?.average_class_performance || 0}%`}
            subtitle="Across all diagnostic quizzes"
            icon={Award}
            color="emerald"
          />
          <StatCard
            title="Curriculum Completion"
            value={`${dash?.completion_rate || 0}%`}
            subtitle="Completed lessons ratio"
            icon={CheckCircle2}
            color="purple"
          />
          <StatCard
            title="Needs Attention"
            value={dash?.students_needing_attention || 0}
            subtitle="At-risk learners (<60% mastery)"
            icon={AlertTriangle}
            color="rose"
          />
        </div>

        {/* Main 2-Col Grid: Topic Gaps & Recent Alerts */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Topic Gaps */}
          <div className="lg:col-span-2 rounded-3xl border border-slate-200 dark:border-white/[0.08] bg-white dark:bg-[#0B1124]/85 p-6 shadow-sm">
            <div className="flex items-center justify-between mb-4">
              <div>
                <h3 className="font-bold text-slate-900 dark:text-white">Class Topic Gap Analytics</h3>
                <p className="text-xs text-slate-500 dark:text-slate-400">Topics requiring highest classroom intervention</p>
              </div>
              <Link href="/teacher/analytics" className="text-xs font-semibold text-brand-600 dark:text-cyan-400 hover:text-brand-700 dark:hover:text-cyan-300">
                Detailed View &rarr;
              </Link>
            </div>

            <div className="overflow-x-auto">
              <table className="w-full text-left text-xs">
                <thead className="border-b border-slate-200 dark:border-white/[0.06] bg-slate-50 dark:bg-white/[0.03] text-[11px] font-bold uppercase tracking-wider text-slate-400 dark:text-slate-500">
                  <tr>
                    <th className="px-4 py-3">Topic</th>
                    <th className="px-4 py-3">Subject</th>
                    <th className="px-4 py-3">Class Accuracy</th>
                    <th className="px-4 py-3 text-right">Needs Help</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-100 dark:divide-white/[0.04]">
                  {dash?.topic_gaps.map((tg) => (
                    <tr key={tg.topic_id} className="hover:bg-slate-50 dark:hover:bg-white/[0.03] transition">
                      <td className="px-4 py-3 font-semibold text-slate-900 dark:text-white">{tg.topic_name}</td>
                      <td className="px-4 py-3 text-slate-500 dark:text-slate-400">{tg.subject_name}</td>
                      <td className="px-4 py-3">
                        <div className="flex items-center gap-2">
                          <span className="font-bold text-slate-900 dark:text-white">{tg.class_average_accuracy}%</span>
                          <div className="w-20 hidden sm:block">
                            <ProgressBar progress={tg.class_average_accuracy} size="sm" color={tg.class_average_accuracy >= 70 ? "emerald" : tg.class_average_accuracy >= 50 ? "amber" : "rose"} showValue={false} />
                          </div>
                        </div>
                      </td>
                      <td className="px-4 py-3 text-right">
                        <Badge variant={tg.students_needing_intervention > 0 ? "rose" : "emerald"} size="sm">
                          {tg.students_needing_intervention} Students
                        </Badge>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>

          {/* Recent At-Risk Alerts */}
          <div className="rounded-3xl border border-slate-200 dark:border-white/[0.08] bg-white dark:bg-[#0B1124]/85 p-6 shadow-sm">
            <div className="flex items-center justify-between mb-4">
              <div>
                <h3 className="font-bold text-slate-900 dark:text-white">Intervention Alerts</h3>
                <p className="text-xs text-slate-500 dark:text-slate-400">Live alerts for teacher review</p>
              </div>
              <Link href="/teacher/alerts" className="text-xs font-semibold text-brand-600 dark:text-cyan-400 hover:text-brand-700 dark:hover:text-cyan-300">
                View All &rarr;
              </Link>
            </div>

            {dash?.recent_alerts && dash.recent_alerts.length > 0 ? (
              <div className="space-y-3">
                {dash.recent_alerts.slice(0, 5).map((al) => (
                  <div
                    key={al.id}
                    className="rounded-2xl border border-slate-100 dark:border-white/[0.05] bg-slate-50 dark:bg-white/[0.03] p-3.5 hover:border-slate-200 dark:hover:border-white/10 transition"
                  >
                    <div className="flex items-center justify-between">
                      <span className="text-xs font-bold text-slate-900 dark:text-white">{al.student_name}</span>
                      <Badge variant={al.severity === "HIGH" ? "rose" : "amber"} size="sm">
                        {al.alert_type}
                      </Badge>
                    </div>
                    <p className="text-[11px] text-slate-600 dark:text-slate-400 mt-1.5 leading-relaxed line-clamp-2">
                      {al.message}
                    </p>
                    <span className="block text-[10px] text-slate-400 mt-2">
                      Topic: {al.topic_name} &bull; Status: {al.status}
                    </span>
                  </div>
                ))}
              </div>
            ) : (
              <p className="text-xs text-slate-400 py-6 text-center">No pending intervention alerts.</p>
            )}
          </div>
        </div>
      </div>
    </RoleLayout>
  );
}
