"use client";

import React from "react";
import Link from "next/link";
import { useQuery } from "@tanstack/react-query";
import { studentService, StudentDashboardData } from "@/services/student.service";
import { RoleLayout } from "@/components/layout/RoleLayout";
import { StatCard } from "@/components/common/StatCard";
import { ProgressBar } from "@/components/common/ProgressBar";
import { Badge } from "@/components/common/Badge";
import {
  TrendingUp,
  Award,
  BookOpen,
  Flame,
  ArrowRight,
  AlertCircle,
  Lightbulb,
  CheckCircle2,
  Calendar,
  Sparkles,
  PlayCircle
} from "lucide-react";

export default function StudentDashboardPage() {
  const { data, isLoading, error } = useQuery<StudentDashboardData>({
    queryKey: ["studentDashboard"],
    queryFn: studentService.getDashboard,
  });

  return (
    <RoleLayout allowedRoles={["STUDENT", "ADMIN"]}>
      {isLoading ? (
        <div className="space-y-6 animate-pulse">
          <div className="h-20 bg-slate-200 rounded-2xl w-full" />
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
            {[1, 2, 3, 4].map((i) => (
              <div key={i} className="h-28 bg-slate-200 rounded-2xl" />
            ))}
          </div>
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            <div className="lg:col-span-2 h-72 bg-slate-200 rounded-2xl" />
            <div className="h-72 bg-slate-200 rounded-2xl" />
          </div>
        </div>
      ) : error ? (
        <div className="rounded-2xl border border-rose-200 bg-rose-50 p-6 text-rose-700">
          <h3 className="font-bold">Error loading dashboard</h3>
          <p className="text-sm mt-1">{(error as any)?.message || "Failed to load dashboard data."}</p>
        </div>
      ) : data ? (
        <div className="space-y-6">
          {/* Header Greeting Banner */}
          <div className="rounded-3xl bg-gradient-to-r from-brand-700 via-secondary-700 to-indigo-900 p-6 sm:p-8 text-white shadow-lg">
            <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
              <div>
                <span className="inline-flex items-center gap-1.5 rounded-full bg-white/10 px-3 py-1 text-xs font-semibold backdrop-blur">
                  <Sparkles className="h-3.5 w-3.5 text-accent-400" /> Continuous Learning Loop
                </span>
                <h1 className="mt-2 text-2xl sm:text-3xl font-extrabold tracking-tight">
                  {data.greeting}
                </h1>
                <p className="mt-1 text-sm text-brand-100 max-w-xl">
                  {data.student.department} &bull; Semester {data.student.semester} &bull; ID: {data.student.student_id}
                </p>
              </div>

              {/* Recommended Next Activity Quick Card */}
              {data.recommended_next_activity && (
                <div className="rounded-2xl bg-white/10 p-4 backdrop-blur border border-white/15 max-w-md w-full">
                  <div className="flex items-center gap-2 text-xs font-semibold text-accent-300 mb-1">
                    <Lightbulb className="h-4 w-4" /> Next Recommended Focus
                  </div>
                  <h4 className="font-bold text-sm text-white line-clamp-1">
                    {data.recommended_next_activity.title}
                  </h4>
                  <p className="text-xs text-brand-100 line-clamp-2 mt-1">
                    {data.recommended_next_activity.reason}
                  </p>
                  <Link
                    href={
                      data.recommended_next_activity.recommendation_type === "ASSESSMENT"
                        ? "/student/quizzes/1"
                        : data.recommended_next_activity.resource_id
                        ? `/student/lessons/${data.recommended_next_activity.resource_id}`
                        : "/student/recommendations"
                    }
                    className="mt-3 inline-flex items-center gap-1.5 rounded-lg bg-white px-3 py-1.5 text-xs font-bold text-brand-700 shadow hover:bg-brand-50 transition"
                  >
                    <span>Start Activity</span>
                    <ArrowRight className="h-3.5 w-3.5" />
                  </Link>
                </div>
              )}
            </div>
          </div>

          {/* Metric Stat Cards */}
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
            <StatCard
              title="Overall Progress"
              value={`${data.overall_progress}%`}
              subtitle={`${data.lessons_completed} of ${data.total_lessons} lessons completed`}
              icon={TrendingUp}
              color="brand"
            />
            <StatCard
              title="Average Quiz Score"
              value={`${data.average_quiz_score}%`}
              subtitle="Calculated across all assessments"
              icon={Award}
              color="emerald"
            />
            <StatCard
              title="Lessons Completed"
              value={data.lessons_completed}
              subtitle="Interactive concept modules"
              icon={BookOpen}
              color="cyan"
            />
            <StatCard
              title="Learning Streak"
              value={`${data.current_streak} Days`}
              subtitle="Active daily study record"
              icon={Flame}
              color="amber"
            />
          </div>

          {/* Main Grid: Learning Path & Weak Topics */}
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            {/* Left 2 Cols: Today's Learning Plan & Subject Progress */}
            <div className="lg:col-span-2 space-y-6">
              {/* Today's Learning Plan */}
              <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
                <div className="flex items-center justify-between mb-4">
                  <div className="flex items-center gap-2">
                    <Calendar className="h-5 w-5 text-brand-600" />
                    <h3 className="font-bold text-slate-900">Today&apos;s Adaptive Learning Plan</h3>
                  </div>
                  <Link
                    href="/student/learning-plan"
                    className="text-xs font-semibold text-brand-600 hover:text-brand-700"
                  >
                    Full Roadmap &rarr;
                  </Link>
                </div>

                {data.today_learning_plan && data.today_learning_plan.length > 0 ? (
                  <div className="space-y-3">
                    {data.today_learning_plan.map((item, idx) => (
                      <div
                        key={item.id}
                        className="flex items-center justify-between rounded-xl border border-slate-100 bg-slate-50/60 p-3.5 hover:bg-slate-50 transition"
                      >
                        <div className="flex items-center gap-3">
                          <div className={`flex h-8 w-8 items-center justify-center rounded-lg text-xs font-bold ${
                            item.completed ? "bg-emerald-100 text-emerald-700" : "bg-brand-100 text-brand-700"
                          }`}>
                            {idx + 1}
                          </div>
                          <div>
                            <h4 className="text-sm font-semibold text-slate-900">{item.title}</h4>
                            <p className="text-xs text-slate-500">{item.description}</p>
                          </div>
                        </div>

                        <Link
                          href={item.resource_type === "LESSON" ? `/student/lessons/${item.resource_id}` : `/student/quizzes/${item.resource_id}`}
                          className="flex items-center gap-1 text-xs font-semibold text-brand-600 hover:text-brand-700 px-3 py-1.5 rounded-lg border border-slate-200 bg-white shadow-sm"
                        >
                          <PlayCircle className="h-3.5 w-3.5" />
                          <span>Action</span>
                        </Link>
                      </div>
                    ))}
                  </div>
                ) : (
                  <p className="text-xs text-slate-500 py-4 text-center">No pending items. Take a quiz to refresh your learning plan!</p>
                )}
              </div>

              {/* Subject Progress */}
              <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
                <div className="flex items-center justify-between mb-4">
                  <h3 className="font-bold text-slate-900">Enrolled Subject Progress</h3>
                  <Link href="/student/subjects" className="text-xs font-semibold text-brand-600 hover:text-brand-700">
                    Explore Subjects &rarr;
                  </Link>
                </div>

                <div className="space-y-4">
                  {(data.subject_progress || []).map((subj) => (
                    <div key={subj.subject_id} className="rounded-xl border border-slate-100 p-3.5">
                      <div className="flex items-center justify-between mb-2">
                        <div>
                          <span className="text-xs font-bold text-slate-400 uppercase mr-2">{subj.code}</span>
                          <span className="text-sm font-bold text-slate-900">{subj.subject_name}</span>
                        </div>
                        <span className="text-xs font-semibold text-slate-500">
                          {subj.completed_lessons}/{subj.total_lessons} Lessons
                        </span>
                      </div>
                      <ProgressBar progress={subj.percentage} color="brand" />
                    </div>
                  ))}
                  {(!data.subject_progress || data.subject_progress.length === 0) && (
                    <p className="text-xs text-slate-500 py-3 text-center">No enrolled subjects found.</p>
                  )}
                </div>
              </div>
            </div>

            {/* Right Column: Weak Topics & Recent Results */}
            <div className="space-y-6">
              {/* Knowledge Gap Detection (Weak Topics) */}
              <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
                <div className="flex items-center gap-2 mb-3">
                  <AlertCircle className="h-5 w-5 text-amber-500" />
                  <h3 className="font-bold text-slate-900">Identified Knowledge Gaps</h3>
                </div>
                <p className="text-xs text-slate-500 mb-4">
                  Topics with accuracy below 60% prioritized for targeted intervention.
                </p>

                {(data.weak_topics || []).length > 0 ? (
                  <div className="space-y-3">
                    {data.weak_topics.map((wt) => (
                      <div
                        key={wt.topic_id}
                        className="rounded-xl border border-amber-200/60 bg-amber-50/50 p-3.5"
                      >
                        <div className="flex items-center justify-between">
                          <h4 className="text-sm font-bold text-slate-900">{wt.topic_name}</h4>
                          <Badge variant="rose" size="sm">
                            {wt.accuracy}% Accuracy
                          </Badge>
                        </div>
                        <p className="text-xs text-slate-600 mt-1">
                          Current mastery: {wt.mastery_score}%. Review recommended.
                        </p>
                        <div className="mt-3 flex gap-2">
                          <Link
                            href="/student/quizzes/1"
                            className="rounded-lg bg-amber-600 px-2.5 py-1 text-[11px] font-semibold text-white shadow-sm hover:bg-amber-700"
                          >
                            Practice 10 Questions
                          </Link>
                          <Link
                            href="/student/ai-tutor"
                            className="rounded-lg border border-slate-200 bg-white px-2.5 py-1 text-[11px] font-semibold text-slate-700 hover:bg-slate-50"
                          >
                            Ask AI Tutor
                          </Link>
                        </div>
                      </div>
                    ))}
                  </div>
                ) : (
                  <div className="rounded-xl border border-emerald-200 bg-emerald-50 p-4 text-center">
                    <CheckCircle2 className="h-6 w-6 text-emerald-600 mx-auto mb-1" />
                    <p className="text-xs font-semibold text-emerald-800">No weak topics detected!</p>
                    <p className="text-[11px] text-emerald-600">All assessed topics are above 60% mastery.</p>
                  </div>
                )}
              </div>

              {/* Recent Quiz Results */}
              <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
                <div className="flex items-center justify-between mb-3">
                  <h3 className="font-bold text-slate-900">Recent Quiz Results</h3>
                  <Link href="/student/progress" className="text-xs font-semibold text-brand-600 hover:text-brand-700">
                    History &rarr;
                  </Link>
                </div>

                {(data.recent_quiz_results || []).length > 0 ? (
                  <div className="space-y-2.5">
                    {data.recent_quiz_results.map((res) => (
                      <Link
                        key={res.attempt_id}
                        href={`/student/results/${res.attempt_id}`}
                        className="flex items-center justify-between rounded-xl border border-slate-100 p-3 hover:border-brand-200 hover:bg-slate-50 transition"
                      >
                        <div>
                          <p className="text-xs font-semibold text-slate-900 line-clamp-1">{res.quiz_title}</p>
                          <p className="text-[11px] text-slate-400">{res.subject_name}</p>
                        </div>
                        <Badge
                          variant={res.percentage >= 70 ? "emerald" : res.percentage >= 50 ? "amber" : "rose"}
                          size="sm"
                        >
                          {res.percentage}%
                        </Badge>
                      </Link>
                    ))}
                  </div>
                ) : (
                  <p className="text-xs text-slate-500 py-3 text-center">No assessments completed yet.</p>
                )}
              </div>
            </div>
          </div>
        </div>
      ) : null}
    </RoleLayout>
  );
}
