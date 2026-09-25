"use client";

import React from "react";
import { useQuery } from "@tanstack/react-query";
import { teacherService, TopicGap } from "@/services/teacher.service";
import { RoleLayout } from "@/components/layout/RoleLayout";
import { Badge } from "@/components/common/Badge";
import { ProgressBar } from "@/components/common/ProgressBar";
import { Layers, AlertTriangle, Users } from "lucide-react";

export default function TeacherAnalyticsPage() {
  const { data: topicGaps, isLoading } = useQuery<TopicGap[]>({
    queryKey: ["teacherTopicGaps"],
    queryFn: teacherService.getTopicGaps,
  });

  return (
    <RoleLayout allowedRoles={["TEACHER", "ADMIN"]}>
      <div className="space-y-6">
        <div>
          <h1 className="text-2xl font-bold tracking-tight text-slate-900">Topic Gap & Difficulty Analytics</h1>
          <p className="mt-1 text-sm text-slate-500">
            Class-wide aggregated diagnostic scores ordered by topics requiring immediate instructor intervention.
          </p>
        </div>

        <div className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
          {isLoading ? (
            <div className="space-y-3 animate-pulse">
              {[1, 2, 3].map((i) => (
                <div key={i} className="h-16 bg-slate-100 rounded-xl" />
              ))}
            </div>
          ) : topicGaps && topicGaps.length > 0 ? (
            <div className="overflow-x-auto">
              <table className="w-full text-left text-xs">
                <thead className="border-b border-slate-200 bg-slate-50 text-[11px] font-bold uppercase tracking-wider text-slate-400">
                  <tr>
                    <th className="px-4 py-3">Topic</th>
                    <th className="px-4 py-3">Subject</th>
                    <th className="px-4 py-3">Class Accuracy</th>
                    <th className="px-4 py-3">Assessed Learners</th>
                    <th className="px-4 py-3">Intervention Needed</th>
                    <th className="px-4 py-3 text-right">Difficulty</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-100">
                  {topicGaps.map((tg) => (
                    <tr key={tg.topic_id} className="hover:bg-slate-50 transition">
                      <td className="px-4 py-3.5 font-bold text-slate-900">{tg.topic_name}</td>
                      <td className="px-4 py-3.5 text-slate-500">{tg.subject_name}</td>
                      <td className="px-4 py-3.5">
                        <div className="flex items-center gap-2">
                          <span className="font-bold">{tg.class_average_accuracy}%</span>
                          <div className="w-24">
                            <ProgressBar progress={tg.class_average_accuracy} size="sm" color={tg.class_average_accuracy >= 70 ? "emerald" : tg.class_average_accuracy >= 50 ? "amber" : "rose"} showValue={false} />
                          </div>
                        </div>
                      </td>
                      <td className="px-4 py-3.5 font-medium text-slate-600">{tg.total_students_assessed} Students</td>
                      <td className="px-4 py-3.5">
                        <Badge variant={tg.students_needing_intervention > 0 ? "rose" : "emerald"} size="sm">
                          {tg.students_needing_intervention} Struggling
                        </Badge>
                      </td>
                      <td className="px-4 py-3.5 text-right">
                        <Badge variant={tg.difficulty === "EASY" ? "emerald" : tg.difficulty === "MEDIUM" ? "brand" : "purple"} size="sm">
                          {tg.difficulty}
                        </Badge>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          ) : (
            <p className="text-xs text-slate-400 py-6 text-center">No topic gap analytics available yet.</p>
          )}
        </div>
      </div>
    </RoleLayout>
  );
}
