"use client";

import React from "react";
import Link from "next/link";
import { useQuery } from "@tanstack/react-query";
import { teacherService, StudentSummary } from "@/services/teacher.service";
import { RoleLayout } from "@/components/layout/RoleLayout";
import { Badge } from "@/components/common/Badge";
import { Users, AlertTriangle, ArrowRight, CheckCircle2 } from "lucide-react";

export default function TeacherStudentsPage() {
  const { data: students, isLoading } = useQuery<StudentSummary[]>({
    queryKey: ["teacherStudents"],
    queryFn: teacherService.getStudents,
  });

  return (
    <RoleLayout allowedRoles={["TEACHER", "ADMIN"]}>
      <div className="space-y-6">
        <div>
          <h1 className="text-2xl font-bold tracking-tight text-slate-900">Enrolled Students Roster</h1>
          <p className="mt-1 text-sm text-slate-500">
            Review individual learner metrics, identify struggling students, and inspect performance profiles.
          </p>
        </div>

        <div className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
          {isLoading ? (
            <div className="space-y-3 animate-pulse">
              {[1, 2, 3].map((i) => (
                <div key={i} className="h-16 bg-slate-100 rounded-xl" />
              ))}
            </div>
          ) : students && students.length > 0 ? (
            <div className="overflow-x-auto">
              <table className="w-full text-left text-xs">
                <thead className="border-b border-slate-200 bg-slate-50 text-[11px] font-bold uppercase tracking-wider text-slate-400">
                  <tr>
                    <th className="px-4 py-3">Student Name</th>
                    <th className="px-4 py-3">Student ID</th>
                    <th className="px-4 py-3">Department</th>
                    <th className="px-4 py-3">Average Score</th>
                    <th className="px-4 py-3">Quizzes</th>
                    <th className="px-4 py-3">Risk Status</th>
                    <th className="px-4 py-3 text-right">Actions</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-100">
                  {students.map((stu) => (
                    <tr key={stu.id} className="hover:bg-slate-50 transition">
                      <td className="px-4 py-3.5 font-bold text-slate-900">
                        <div>
                          <span>{stu.name}</span>
                          <span className="block text-[11px] font-normal text-slate-400">{stu.email}</span>
                        </div>
                      </td>
                      <td className="px-4 py-3.5 font-semibold text-slate-600">{stu.student_id}</td>
                      <td className="px-4 py-3.5 text-slate-500">{stu.department}</td>
                      <td className="px-4 py-3.5 font-bold text-slate-900">{stu.average_score}%</td>
                      <td className="px-4 py-3.5 font-medium text-slate-500">{stu.quizzes_completed}</td>
                      <td className="px-4 py-3.5">
                        {stu.at_risk ? (
                          <Badge variant="rose" size="sm">
                            <span className="flex items-center gap-1">
                              <AlertTriangle className="h-3 w-3" /> Needs Attention
                            </span>
                          </Badge>
                        ) : (
                          <Badge variant="emerald" size="sm">
                            <span className="flex items-center gap-1">
                              <CheckCircle2 className="h-3 w-3" /> On Track
                            </span>
                          </Badge>
                        )}
                      </td>
                      <td className="px-4 py-3.5 text-right">
                        <Link
                          href={`/teacher/students/${stu.id}`}
                          className="inline-flex items-center gap-1 rounded-xl bg-slate-900 px-3 py-1.5 text-xs font-semibold text-white shadow hover:bg-brand-600 transition"
                        >
                          <span>Inspect</span>
                          <ArrowRight className="h-3 w-3" />
                        </Link>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          ) : (
            <p className="text-xs text-slate-400 py-6 text-center">No enrolled students found.</p>
          )}
        </div>
      </div>
    </RoleLayout>
  );
}
