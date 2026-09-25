"use client";

import React from "react";
import Link from "next/link";
import { useParams } from "next/navigation";
import { useQuery } from "@tanstack/react-query";
import { teacherService } from "@/services/teacher.service";
import { RoleLayout } from "@/components/layout/RoleLayout";
import { Badge } from "@/components/common/Badge";
import { ProgressBar } from "@/components/common/ProgressBar";
import {
  ArrowLeft,
  User,
  Award,
  BookOpen,
  AlertTriangle,
  Lightbulb,
  CheckCircle2,
  Calendar,
  HelpCircle,
  Loader2
} from "lucide-react";

export default function StudentDetailInspectPage() {
  const params = useParams();
  const studentId = Number(params?.id);

  const { data, isLoading } = useQuery({
    queryKey: ["teacherStudentDetail", studentId],
    queryFn: () => teacherService.getStudentDetail(studentId),
    enabled: !!studentId,
  });

  return (
    <RoleLayout allowedRoles={["TEACHER", "ADMIN"]}>
      <div className="mx-auto max-w-4xl space-y-6">
        <Link
          href="/teacher/students"
          className="inline-flex items-center gap-1.5 text-xs font-semibold text-slate-500 hover:text-slate-800"
        >
          <ArrowLeft className="h-4 w-4" />
          <span>Back to Students Roster</span>
        </Link>

        {isLoading ? (
          <div className="flex h-96 items-center justify-center">
            <Loader2 className="h-8 w-8 animate-spin text-brand-600" />
          </div>
        ) : data && data.student ? (
          <div className="space-y-6">
            {/* Student Header Card */}
            <div className="rounded-3xl border border-slate-200 bg-white p-6 sm:p-8 shadow-sm">
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
                <div className="flex items-center gap-4">
                  <div className="flex h-14 w-14 items-center justify-center rounded-2xl bg-brand-50 text-xl font-black text-brand-700">
                    {data.student.name.charAt(0)}
                  </div>
                  <div>
                    <h1 className="text-xl sm:text-2xl font-bold text-slate-900">{data.student.name}</h1>
                    <p className="text-xs text-slate-500">{data.student.email}</p>
                    <p className="text-xs text-slate-400 mt-1">
                      {data.student.student_id} &bull; {data.student.department} &bull; Semester {data.student.semester}
                    </p>
                  </div>
                </div>
              </div>
            </div>

            {/* Topic Mastery Profile */}
            <div className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
              <h3 className="font-bold text-slate-900 mb-4">Topic Mastery Diagnosed by SPECTRA</h3>
              <div className="space-y-3">
                {data.topic_performances?.map((tp: any) => (
                  <div
                    key={tp.topic_id}
                    className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 rounded-2xl border border-slate-100 bg-slate-50/50 p-4"
                  >
                    <div>
                      <h4 className="text-sm font-bold text-slate-900">{tp.topic_name}</h4>
                      <p className="text-xs text-slate-500">
                        Accuracy: {tp.accuracy}% &bull; Attempts: {tp.attempts}
                      </p>
                    </div>

                    <div className="flex items-center gap-4">
                      <div className="w-32">
                        <ProgressBar progress={tp.mastery_score} size="sm" color={tp.mastery_score >= 70 ? "emerald" : tp.mastery_score >= 50 ? "amber" : "rose"} />
                      </div>
                      <Badge variant={tp.status === "MASTERED" ? "emerald" : tp.status === "NEEDS_PRACTICE" ? "amber" : "rose"} size="sm">
                        {tp.status}
                      </Badge>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Assessment History */}
            <div className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
              <h3 className="font-bold text-slate-900 mb-4">Assessment History</h3>
              {data.recent_attempts && data.recent_attempts.length > 0 ? (
                <div className="space-y-2.5">
                  {data.recent_attempts.map((att: any) => (
                    <div
                      key={att.attempt_id}
                      className="flex items-center justify-between rounded-xl border border-slate-100 p-3 text-xs"
                    >
                      <span className="font-semibold text-slate-900">{att.quiz_title}</span>
                      <div className="flex items-center gap-3">
                        <span className="text-slate-400">{att.completed_at ? new Date(att.completed_at).toLocaleDateString() : ""}</span>
                        <Badge variant={att.percentage >= 70 ? "emerald" : att.percentage >= 50 ? "amber" : "rose"} size="sm">
                          {att.percentage}%
                        </Badge>
                      </div>
                    </div>
                  ))}
                </div>
              ) : (
                <p className="text-xs text-slate-400">No attempts logged yet.</p>
              )}
            </div>
          </div>
        ) : (
          <div className="rounded-2xl border border-dashed border-slate-300 p-8 text-center text-slate-500">
            Student details not available.
          </div>
        )}
      </div>
    </RoleLayout>
  );
}
