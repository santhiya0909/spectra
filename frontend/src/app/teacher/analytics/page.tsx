"use client";

import React from "react";
import { useQuery } from "@tanstack/react-query";
import { teacherService, TopicGap } from "@/services/teacher.service";
import { RoleLayout } from "@/components/layout/RoleLayout";
import { Badge } from "@/components/common/Badge";
import { ProgressBar } from "@/components/common/ProgressBar";
import { 
  Layers, 
  AlertTriangle, 
  Users, 
  BookOpen, 
  Zap, 
  TrendingUp, 
  Award,
  CheckCircle2
} from "lucide-react";

export default function TeacherAnalyticsPage() {
  const { data: topicGaps, isLoading: gapsLoading } = useQuery<TopicGap[]>({
    queryKey: ["teacherTopicGaps"],
    queryFn: teacherService.getTopicGaps,
  });

  const { data: detailedAnalytics, isLoading: detailedLoading } = useQuery({
    queryKey: ["teacherDetailedAnalytics"],
    queryFn: teacherService.getDetailedAnalytics,
  });

  return (
    <RoleLayout allowedRoles={["TEACHER", "ADMIN"]}>
      <div className="space-y-8 pb-16">
        <div>
          <h1 className="text-2xl font-black tracking-tight text-slate-900 dark:text-white">
            Instructor Analytics &amp; Curriculum Gaps
          </h1>
          <p className="mt-1 text-sm text-slate-500 dark:text-slate-400">
            Class-wide aggregated diagnostic scores, interactive puzzle problem-solving metrics, and topics requiring intervention.
          </p>
        </div>

        {/* Top 3 Summary Cards */}
        {detailedAnalytics && (
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
            <div className="p-5 rounded-3xl bg-white dark:bg-[#0B1124]/85 border border-slate-200/90 dark:border-white/[0.08] shadow-sm flex items-center gap-4">
              <div className="w-12 h-12 rounded-2xl bg-indigo-50 dark:bg-indigo-900/20 border border-indigo-100 dark:border-indigo-500/20 flex items-center justify-center text-indigo-600 dark:text-indigo-400">
                <BookOpen className="w-6 h-6" />
              </div>
              <div>
                <span className="text-xs uppercase font-bold text-slate-400 dark:text-slate-500 block tracking-wider">Curriculum Tracks</span>
                <span className="text-2xl font-black text-slate-900 dark:text-white">
                  {detailedAnalytics.subject_breakdowns?.length || 8} Active
                </span>
                <span className="text-xs text-slate-500 dark:text-slate-400 block">10 lessons per subject track</span>
              </div>
            </div>

            <div className="p-5 rounded-3xl bg-white dark:bg-[#0B1124]/85 border border-slate-200/90 dark:border-white/[0.08] shadow-sm flex items-center gap-4">
              <div className="w-12 h-12 rounded-2xl bg-purple-50 dark:bg-purple-900/20 border border-purple-100 dark:border-purple-500/20 flex items-center justify-center text-purple-600 dark:text-purple-400">
                <Zap className="w-6 h-6" />
              </div>
              <div>
                <span className="text-xs uppercase font-bold text-slate-400 dark:text-slate-500 block tracking-wider">Interactive Puzzles</span>
                <span className="text-2xl font-black text-slate-900 dark:text-white">
                  {detailedAnalytics.total_puzzles_available || 80}
                </span>
                <span className="text-xs text-slate-500 dark:text-slate-400 block">
                  {detailedAnalytics.recent_student_puzzle_attempts?.length || 0} recent student submissions
                </span>
              </div>
            </div>

            <div className="p-5 rounded-3xl bg-white dark:bg-[#0B1124]/85 border border-slate-200/90 dark:border-white/[0.08] shadow-sm flex items-center gap-4">
              <div className="w-12 h-12 rounded-2xl bg-rose-50 dark:bg-rose-900/20 border border-rose-100 dark:border-rose-500/20 flex items-center justify-center text-rose-600 dark:text-rose-400">
                <AlertTriangle className="w-6 h-6" />
              </div>
              <div>
                <span className="text-xs uppercase font-bold text-slate-400 dark:text-slate-500 block tracking-wider">At-Risk Topics</span>
                <span className="text-2xl font-black text-rose-600 dark:text-rose-400">
                  {topicGaps?.filter(t => t.students_needing_intervention > 0).length || 0} Topics
                </span>
                <span className="text-xs text-slate-500 dark:text-slate-400 block">Accuracy below 60% threshold</span>
              </div>
            </div>
          </div>
        )}

        {/* Subject Track Performance */}
        {detailedAnalytics?.subject_breakdowns && (
          <div className="rounded-3xl border border-slate-200/90 dark:border-white/[0.08] bg-white dark:bg-[#0B1124]/85 p-6 shadow-sm space-y-4">
            <h2 className="text-base font-bold text-slate-900 dark:text-white flex items-center gap-2">
              <TrendingUp className="w-5 h-5 text-indigo-600 dark:text-indigo-400" />
              <span>Subject Track &amp; Puzzle Solve Overview</span>
            </h2>
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
              {detailedAnalytics.subject_breakdowns.map((subj: any) => (
                <div key={subj.subject_id} className="p-4 rounded-2xl border border-slate-100 dark:border-white/[0.05] bg-slate-50/60 dark:bg-white/[0.02] space-y-2">
                  <div className="flex items-center justify-between">
                    <span className="text-[10px] font-extrabold uppercase px-2 py-0.5 rounded bg-white dark:bg-white/[0.07] text-indigo-700 dark:text-indigo-300 border border-indigo-100 dark:border-indigo-500/20">
                      {subj.code}
                    </span>
                    <span className="text-xs font-bold text-slate-900 dark:text-white">{subj.average_quiz_score}% Avg</span>
                  </div>
                  <h4 className="text-xs font-bold text-slate-900 dark:text-white truncate">{subj.subject_name}</h4>
                  <div className="text-[11px] text-slate-500 dark:text-slate-400 space-y-0.5 pt-1 border-t border-slate-200/60 dark:border-white/[0.05]">
                    <div className="flex justify-between">
                      <span>Curriculum:</span>
                      <span className="font-semibold text-slate-700 dark:text-slate-300">{subj.lessons_count} Lessons</span>
                    </div>
                    <div className="flex justify-between">
                      <span>Puzzle Solves:</span>
                      <span className="font-semibold text-purple-700 dark:text-purple-400">{subj.puzzles_solved_count}</span>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Topic Gap Analysis Table */}
        <div className="rounded-3xl border border-slate-200/90 dark:border-white/[0.08] bg-white dark:bg-[#0B1124]/85 p-6 shadow-sm space-y-4">
          <div className="flex items-center justify-between">
            <div>
              <h2 className="text-base font-bold text-slate-900 dark:text-white flex items-center gap-2">
                <Layers className="w-5 h-5 text-amber-500 dark:text-amber-400" />
                <span>Targeted Intervention Table</span>
              </h2>
              <p className="text-xs text-slate-500 dark:text-slate-400 mt-0.5">
                Ordered by topics requiring instructor attention and adaptive assignment.
              </p>
            </div>
          </div>

          {gapsLoading ? (
            <div className="space-y-3 animate-pulse">
              {[1, 2, 3].map((i) => (
                <div key={i} className="h-16 bg-slate-100 dark:bg-white/[0.04] rounded-xl" />
              ))}
            </div>
          ) : topicGaps && topicGaps.length > 0 ? (
            <div className="overflow-x-auto">
              <table className="w-full text-left text-xs">
                <thead className="border-b border-slate-200 dark:border-white/[0.06] bg-slate-50 dark:bg-white/[0.03] text-[11px] font-bold uppercase tracking-wider text-slate-400 dark:text-slate-500">
                  <tr>
                    <th className="px-4 py-3">Topic</th>
                    <th className="px-4 py-3">Subject</th>
                    <th className="px-4 py-3">Class Accuracy</th>
                    <th className="px-4 py-3">Assessed Learners</th>
                    <th className="px-4 py-3">Intervention Needed</th>
                    <th className="px-4 py-3 text-right">Difficulty</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-100 dark:divide-white/[0.04]">
                  {topicGaps.map((tg) => (
                    <tr key={tg.topic_id} className="hover:bg-slate-50 dark:hover:bg-white/[0.03] transition">
                      <td className="px-4 py-3.5 font-bold text-slate-900 dark:text-white">{tg.topic_name}</td>
                      <td className="px-4 py-3.5 text-slate-500 dark:text-slate-400">{tg.subject_name}</td>
                      <td className="px-4 py-3.5">
                        <div className="flex items-center gap-2">
                          <span className="font-bold text-slate-900 dark:text-white">{tg.class_average_accuracy}%</span>
                          <div className="w-24">
                            <ProgressBar
                              progress={tg.class_average_accuracy}
                              size="sm"
                              color={tg.class_average_accuracy >= 70 ? "emerald" : tg.class_average_accuracy >= 50 ? "amber" : "rose"}
                              showValue={false}
                            />
                          </div>
                        </div>
                      </td>
                      <td className="px-4 py-3.5 font-medium text-slate-600 dark:text-slate-300">{tg.total_students_assessed} Students</td>
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
