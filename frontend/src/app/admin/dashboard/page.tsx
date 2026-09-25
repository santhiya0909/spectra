"use client";

import React from "react";
import Link from "next/link";
import { useQuery } from "@tanstack/react-query";
import { adminService, AdminDashboardData } from "@/services/admin.service";
import { RoleLayout } from "@/components/layout/RoleLayout";
import { StatCard } from "@/components/common/StatCard";
import { Badge } from "@/components/common/Badge";
import {
  Users,
  BookOpen,
  HelpCircle,
  FileQuestion,
  Shield,
  Layers,
  History,
  ArrowRight
} from "lucide-react";

export default function AdminDashboardPage() {
  const { data: stats, isLoading } = useQuery<AdminDashboardData>({
    queryKey: ["adminDashboard"],
    queryFn: adminService.getDashboard,
  });

  return (
    <RoleLayout allowedRoles={["ADMIN"]}>
      <div className="space-y-6">
        <div>
          <h1 className="text-2xl font-bold tracking-tight text-slate-900">System Administration Console</h1>
          <p className="mt-1 text-sm text-slate-500">
            Monitor platform utilization, maintain curriculum entities, and audit system activities.
          </p>
        </div>

        {/* Platform Stat Cards */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
          <StatCard
            title="Total Registered Users"
            value={stats?.total_users || 0}
            subtitle={`${stats?.total_students || 0} Students &bull; ${stats?.total_teachers || 0} Teachers`}
            icon={Users}
            color="brand"
          />
          <StatCard
            title="Curriculum Subjects"
            value={stats?.total_subjects || 0}
            subtitle="Configured learning domains"
            icon={BookOpen}
            color="purple"
          />
          <StatCard
            title="Question Bank Volume"
            value={stats?.total_questions || 0}
            subtitle={`${stats?.total_quizzes || 0} Assessment Quizzes`}
            icon={FileQuestion}
            color="cyan"
          />
        </div>

        {/* Quick Management Navigation Cards */}
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-4">
          <Link
            href="/admin/users"
            className="group rounded-2xl border border-slate-200 bg-white p-5 shadow-sm hover:border-brand-300 hover:shadow-md transition"
          >
            <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-brand-50 text-brand-600 mb-3">
              <Users className="h-5 w-5" />
            </div>
            <h4 className="font-bold text-slate-900 text-sm">User Management</h4>
            <p className="text-xs text-slate-500 mt-1">Manage accounts and role permissions</p>
          </Link>

          <Link
            href="/admin/subjects"
            className="group rounded-2xl border border-slate-200 bg-white p-5 shadow-sm hover:border-brand-300 hover:shadow-md transition"
          >
            <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-purple-50 text-purple-600 mb-3">
              <BookOpen className="h-5 w-5" />
            </div>
            <h4 className="font-bold text-slate-900 text-sm">Subjects & Topics</h4>
            <p className="text-xs text-slate-500 mt-1">Curriculum structure and taxonomy</p>
          </Link>

          <Link
            href="/admin/questions"
            className="group rounded-2xl border border-slate-200 bg-white p-5 shadow-sm hover:border-brand-300 hover:shadow-md transition"
          >
            <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-cyan-50 text-cyan-600 mb-3">
              <FileQuestion className="h-5 w-5" />
            </div>
            <h4 className="font-bold text-slate-900 text-sm">Question Bank</h4>
            <p className="text-xs text-slate-500 mt-1">Diagnostic items and explanations</p>
          </Link>

          <Link
            href="/admin/quizzes"
            className="group rounded-2xl border border-slate-200 bg-white p-5 shadow-sm hover:border-brand-300 hover:shadow-md transition"
          >
            <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-emerald-50 text-emerald-600 mb-3">
              <HelpCircle className="h-5 w-5" />
            </div>
            <h4 className="font-bold text-slate-900 text-sm">Quiz Catalog</h4>
            <p className="text-xs text-slate-500 mt-1">Adaptive and diagnostic assessments</p>
          </Link>
        </div>

        {/* System Audit Logs */}
        <div className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
          <div className="flex items-center gap-2 mb-4">
            <History className="h-5 w-5 text-slate-600" />
            <h3 className="font-bold text-slate-900">System Activity & Audit Logs</h3>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead className="border-b border-slate-200 bg-slate-50 text-[11px] font-bold uppercase tracking-wider text-slate-400">
                <tr>
                  <th className="px-4 py-3">Timestamp</th>
                  <th className="px-4 py-3">Initiator</th>
                  <th className="px-4 py-3">Action</th>
                  <th className="px-4 py-3">Target Entity</th>
                  <th className="px-4 py-3 text-right">Entity ID</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100">
                {stats?.recent_logs?.map((log) => (
                  <tr key={log.id} className="hover:bg-slate-50 transition">
                    <td className="px-4 py-3 text-slate-400">
                      {new Date(log.created_at).toLocaleString()}
                    </td>
                    <td className="px-4 py-3 font-semibold text-slate-900">{log.user_name}</td>
                    <td className="px-4 py-3">
                      <Badge variant="brand" size="sm">
                        {log.action}
                      </Badge>
                    </td>
                    <td className="px-4 py-3 text-slate-600 font-medium">{log.entity}</td>
                    <td className="px-4 py-3 text-right text-slate-400 font-mono">
                      {log.entity_id || "-"}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </RoleLayout>
  );
}
