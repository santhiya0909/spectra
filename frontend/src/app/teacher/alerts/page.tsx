"use client";

import React from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { teacherService, TeacherAlert } from "@/services/teacher.service";
import { RoleLayout } from "@/components/layout/RoleLayout";
import { Badge } from "@/components/common/Badge";
import { AlertTriangle, CheckCircle2, ShieldCheck, Loader2 } from "lucide-react";

export default function TeacherAlertsPage() {
  const queryClient = useQueryClient();

  const { data: alerts, isLoading } = useQuery<TeacherAlert[]>({
    queryKey: ["teacherAlerts"],
    queryFn: teacherService.getAlerts,
  });

  const updateStatusMutation = useMutation({
    mutationFn: ({ id, status }: { id: number; status: "REVIEWED" | "RESOLVED" }) =>
      teacherService.updateAlertStatus(id, status),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["teacherAlerts"] });
      queryClient.invalidateQueries({ queryKey: ["teacherDashboard"] });
    },
  });

  return (
    <RoleLayout allowedRoles={["TEACHER", "ADMIN"]}>
      <div className="space-y-6">
        <div>
          <h1 className="text-2xl font-bold tracking-tight text-slate-900 dark:text-white">Student Intervention Alerts</h1>
          <p className="mt-1 text-sm text-slate-500 dark:text-slate-400">
            Real-time notifications generated when students experience repeated difficulties or breakthrough mastery.
          </p>
        </div>

        <div className="space-y-3">
          {isLoading ? (
            <div className="space-y-3 animate-pulse">
              {[1, 2, 3].map((i) => (
                <div key={i} className="h-24 bg-slate-200 dark:bg-slate-700/40 rounded-2xl" />
              ))}
            </div>
          ) : alerts && alerts.length > 0 ? (
            alerts.map((alert) => (
              <div
                key={alert.id}
                className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 rounded-3xl border border-slate-200 dark:border-white/[0.08] bg-white dark:bg-[#0B1124]/85 p-5 shadow-sm hover:border-brand-200 dark:hover:border-cyan-500/30 transition"
              >
                <div className="flex items-start gap-4">
                  <div className={`mt-1 flex h-10 w-10 shrink-0 items-center justify-center rounded-2xl ${
                    alert.severity === "HIGH" ? "bg-rose-50 dark:bg-rose-900/20 text-rose-600 dark:text-rose-400" : "bg-amber-50 dark:bg-amber-900/20 text-amber-600 dark:text-amber-400"
                  }`}>
                    <AlertTriangle className="h-5 w-5" />
                  </div>
                  <div>
                    <div className="flex items-center gap-2">
                      <span className="text-sm font-bold text-slate-900 dark:text-white">{alert.student_name}</span>
                      <Badge variant={alert.severity === "HIGH" ? "rose" : "amber"} size="sm">
                        {alert.alert_type}
                      </Badge>
                      <span className="text-xs text-slate-400">&bull; {alert.topic_name}</span>
                    </div>
                    <p className="text-xs text-slate-600 dark:text-slate-400 mt-1 leading-relaxed max-w-2xl">{alert.message}</p>
                    <span className="text-[10px] text-slate-400 mt-1.5 block">
                      Status: <strong className="text-slate-700 dark:text-slate-300">{alert.status}</strong> &bull; Created: {new Date(alert.created_at).toLocaleString()}
                    </span>
                  </div>
                </div>

                <div className="flex items-center gap-2 self-end sm:self-center shrink-0">
                  {alert.status === "ACTIVE" && (
                    <button
                      onClick={() => updateStatusMutation.mutate({ id: alert.id, status: "REVIEWED" })}
                      disabled={updateStatusMutation.isPending}
                      className="inline-flex items-center gap-1 rounded-xl border border-slate-200 dark:border-white/[0.08] bg-slate-50 dark:bg-white/[0.04] px-3.5 py-1.5 text-xs font-semibold text-slate-700 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-white/[0.08] transition"
                    >
                      <CheckCircle2 className="h-3.5 w-3.5 text-brand-600 dark:text-cyan-400" />
                      <span>Mark Reviewed</span>
                    </button>
                  )}
                  {alert.status !== "RESOLVED" && (
                    <button
                      onClick={() => updateStatusMutation.mutate({ id: alert.id, status: "RESOLVED" })}
                      disabled={updateStatusMutation.isPending}
                      className="inline-flex items-center gap-1 rounded-xl bg-slate-900 dark:bg-white/[0.08] px-3.5 py-1.5 text-xs font-semibold text-white hover:bg-slate-800 dark:hover:bg-white/[0.15] transition"
                    >
                      <ShieldCheck className="h-3.5 w-3.5 text-emerald-400" />
                      <span>Resolve</span>
                    </button>
                  )}
                </div>
              </div>
            ))
          ) : (
            <div className="rounded-3xl border border-dashed border-slate-300 dark:border-white/10 p-12 text-center text-slate-500 dark:text-slate-400">
              No active teacher alerts. All students are progressing without risk triggers.
            </div>
          )}
        </div>
      </div>
    </RoleLayout>
  );
}
