"use client";

import React from "react";
import Link from "next/link";
import { useParams } from "next/navigation";
import { useQuery } from "@tanstack/react-query";
import { subjectService, Subject, Lesson } from "@/services/subject.service";
import { RoleLayout } from "@/components/layout/RoleLayout";
import { GlassCard } from "@/components/common/GlassCard";
import { Badge } from "@/components/common/Badge";
import {
  ArrowLeft,
  BookOpen,
  CheckCircle2,
  Clock,
  HelpCircle,
  PlayCircle,
  AlertCircle,
  RefreshCw,
  Layers,
  ChevronRight,
  Sparkles,
  Zap,
  Lock,
  Trophy,
  Check,
  Award
} from "lucide-react";

export default function SubjectDetailPage() {
  const params = useParams();
  const subjectId = Number(params?.id);

  const {
    data: subject,
    isLoading: subjectLoading,
    error: subjectError,
    refetch: refetchSubject,
  } = useQuery<Subject>({
    queryKey: ["subject", subjectId],
    queryFn: () => subjectService.getSubject(subjectId),
    enabled: !!subjectId,
  });

  const lessons: Lesson[] = subject?.lessons || [];
  const completedCount = lessons.filter((l) => l.status === "COMPLETED").length;
  const progressPct = subject?.progress_percentage ?? (lessons.length > 0 ? Math.round((completedCount / lessons.length) * 100) : 0);

  return (
    <RoleLayout allowedRoles={["STUDENT", "ADMIN"]}>
      <div className="space-y-8 pb-16">
        {/* Navigation Breadcrumb */}
        <Link
          href="/student/subjects"
          className="inline-flex items-center gap-1.5 text-xs font-semibold text-slate-400 hover:text-cyan-300 transition"
        >
          <ArrowLeft className="h-4 w-4" />
          <span>Back to All Subjects</span>
        </Link>

        {/* Subject Header Banner */}
        {subjectLoading ? (
          <div className="h-48 bg-slate-800/40 rounded-3xl animate-pulse border border-white/5" />
        ) : subjectError ? (
          <GlassCard className="p-8 text-center border-rose-500/30 bg-rose-950/20 text-rose-300">
            <AlertCircle className="h-8 w-8 mx-auto mb-2 text-rose-400" />
            <h3 className="font-bold text-sm text-white">Failed to load subject details</h3>
            <p className="text-xs text-rose-300 mt-1">{(subjectError as any)?.message || "Please try again."}</p>
            <button
              onClick={() => refetchSubject()}
              className="mt-4 inline-flex items-center gap-1.5 rounded-xl bg-cyan-500 text-black px-4 py-2 text-xs font-bold shadow hover:bg-cyan-400 transition"
            >
              <RefreshCw className="h-3.5 w-3.5" />
              <span>Retry</span>
            </button>
          </GlassCard>
        ) : subject ? (
          <div className="relative overflow-hidden rounded-3xl bg-gradient-to-r from-[#0B1530] via-[#10103A] to-[#140C2C] p-6 sm:p-8 text-white shadow-xl shadow-cyan-950/20 border border-white/10">
            <div className="absolute -top-16 -right-16 w-72 h-72 bg-cyan-500/15 rounded-full blur-[100px] pointer-events-none" />
            <div className="absolute -bottom-16 -left-16 w-72 h-72 bg-purple-500/15 rounded-full blur-[100px] pointer-events-none" />

            <div className="relative z-10 flex flex-col md:flex-row md:items-center justify-between gap-6">
              <div className="space-y-3 max-w-2xl">
                <div className="flex flex-wrap items-center gap-2">
                  <span className="rounded-lg bg-cyan-950/50 backdrop-blur-md px-3 py-1 text-xs font-mono font-bold text-cyan-300 uppercase border border-cyan-500/30">
                    {subject.code}
                  </span>
                  <span className="rounded-lg bg-purple-950/50 backdrop-blur-md px-3 py-1 text-xs font-semibold text-purple-300 border border-purple-500/30">
                    {subject.category?.replace(/_/g, " ") || "COMPUTER SCIENCE"}
                  </span>
                  <span className="rounded-lg bg-emerald-950/50 backdrop-blur-md px-3 py-1 text-xs font-semibold text-emerald-300 border border-emerald-500/30">
                    {subject.difficulty_level || "INTERMEDIATE"}
                  </span>
                </div>

                <h1 className="text-2xl sm:text-4xl font-black text-white tracking-tight">
                  {subject.name}
                </h1>
                <p className="text-sm sm:text-base text-slate-300 leading-relaxed font-normal">
                  {subject.description}
                </p>

                <div className="flex flex-wrap items-center gap-4 pt-1 text-xs font-semibold text-slate-400">
                  <span className="flex items-center gap-1.5 text-cyan-300">
                    <BookOpen className="w-4 h-4 text-cyan-400" />
                    {lessons.length} Sequential Lessons
                  </span>
                  <span>&bull;</span>
                  <span className="flex items-center gap-1.5 text-purple-300">
                    <Zap className="w-4 h-4 text-purple-400" />
                    {lessons.length} Interactive Puzzles
                  </span>
                  <span>&bull;</span>
                  <span className="flex items-center gap-1.5 text-emerald-300">
                    <HelpCircle className="w-4 h-4 text-emerald-400" />
                    Checkpoint Quizzes
                  </span>
                </div>
              </div>

              {/* Subject Progress Card */}
              <div className="w-full md:w-64 rounded-2xl bg-[#080D1F]/90 backdrop-blur-xl border border-white/10 p-5 shrink-0 shadow-lg">
                <span className="text-[10px] uppercase font-bold tracking-widest text-slate-400 block mb-1">
                  Track Mastery
                </span>
                <div className="flex items-baseline justify-between mb-2">
                  <span className="text-3xl font-black text-white font-mono">{progressPct}%</span>
                  <span className="text-xs font-semibold text-cyan-400">
                    {completedCount} / {lessons.length} done
                  </span>
                </div>
                <div className="w-full h-2 bg-slate-800 rounded-full overflow-hidden mb-3 border border-white/5">
                  <div
                    className="h-full bg-gradient-to-r from-cyan-500 to-indigo-500 rounded-full shadow-[0_0_10px_#06b6d4] transition-all duration-500"
                    style={{ width: `${progressPct}%` }}
                  />
                </div>
                <span className="text-[11px] text-slate-400 block leading-tight">
                  Complete each lesson module to earn +30 completion XP.
                </span>
              </div>
            </div>
          </div>
        ) : null}

        {/* Sequential Learning Path */}
        <div className="space-y-6">
          <div className="flex items-center justify-between">
            <div>
              <h2 className="text-xl font-bold text-white">
                Curriculum Learning Path
              </h2>
              <p className="text-xs text-slate-400 mt-0.5">
                Work through lessons sequentially. Each includes concept deep-dives, practice problems, and interactive puzzles.
              </p>
            </div>
            <span className="text-xs font-bold text-cyan-300 bg-cyan-950/40 border border-cyan-500/30 px-3 py-1 rounded-full font-mono">
              {lessons.length} Lessons Available
            </span>
          </div>

          <div className="space-y-4">
            {lessons.map((lesson, idx) => {
              const isCompleted = lesson.status === "COMPLETED";
              const isCurrent = !isCompleted && (idx === 0 || lessons[idx - 1]?.status === "COMPLETED");
              const isLocked = !isCompleted && !isCurrent;
              
              const showMilestone = idx > 0 && idx % 3 === 0;

              return (
                <React.Fragment key={lesson.id}>
                  {showMilestone && (
                    <div className="my-6 flex items-center justify-center gap-3">
                      <div className="h-px bg-white/[0.08] flex-1" />
                      <div className="inline-flex items-center gap-2 px-3.5 py-1 rounded-full bg-amber-500/10 border border-amber-500/30 text-amber-300 text-xs font-bold shadow-sm">
                        <Trophy className="w-4 h-4 text-amber-400" />
                        <span>Checkpoint Milestone {idx / 3} Passed</span>
                      </div>
                      <div className="h-px bg-white/[0.08] flex-1" />
                    </div>
                  )}

                  <div
                    className={`rounded-3xl border transition-all duration-300 bg-[#0B1124]/85 p-5 sm:p-6 backdrop-blur-xl shadow-lg ${
                      isCompleted
                        ? "border-emerald-500/30 hover:border-emerald-500/50"
                        : isCurrent
                        ? "border-cyan-400 ring-2 ring-cyan-500/20 shadow-[0_0_25px_rgba(6,182,212,0.2)]"
                        : "border-white/[0.08] opacity-75 hover:opacity-100 hover:border-white/20"
                    }`}
                  >
                    <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
                      <div className="flex items-start gap-4 flex-1">
                        {/* Status Icon */}
                        <div
                          className={`w-11 h-11 shrink-0 rounded-2xl flex items-center justify-center font-black text-sm shadow-sm ${
                            isCompleted
                              ? "bg-emerald-500 text-black shadow-[0_0_10px_#10b981]"
                              : isCurrent
                              ? "bg-cyan-500 text-black shadow-[0_0_12px_#06b6d4] animate-pulse"
                              : "bg-slate-800 text-slate-500"
                          }`}
                        >
                          {isCompleted ? (
                            <Check className="w-6 h-6 stroke-[3]" />
                          ) : isLocked ? (
                            <Lock className="w-5 h-5 text-slate-500" />
                          ) : (
                            idx + 1
                          )}
                        </div>

                        {/* Lesson Details */}
                        <div className="space-y-1.5 flex-1">
                          <div className="flex flex-wrap items-center gap-2">
                            <span className="text-[10px] font-bold text-slate-400 uppercase tracking-wider">
                              Lesson {idx + 1}
                            </span>
                            <span className="text-xs font-semibold text-slate-400 flex items-center gap-1">
                              <Clock className="w-3.5 h-3.5 text-slate-400" />
                              {lesson.estimated_minutes || 15} mins
                            </span>
                            <span className="inline-flex items-center gap-1 text-[10px] font-bold text-amber-300 bg-amber-500/15 px-2 py-0.5 rounded-full border border-amber-500/25 font-mono">
                              <Sparkles className="w-3 h-3 text-amber-400" /> +30 XP
                            </span>
                            <span className="inline-flex items-center gap-1 text-[10px] font-bold text-purple-300 bg-purple-500/15 px-2 py-0.5 rounded-full border border-purple-500/25">
                              <Zap className="w-3 h-3 text-purple-400" /> Interactive Puzzle
                            </span>
                          </div>

                          <h3 className="text-base sm:text-lg font-bold text-white">
                            {lesson.title}
                          </h3>

                          <p className="text-xs text-slate-400 leading-relaxed line-clamp-2">
                            {lesson.short_description || lesson.description}
                          </p>

                          {/* Topics as tags */}
                          {lesson.topics && lesson.topics.length > 0 && (
                            <div className="flex flex-wrap items-center gap-1.5 pt-1">
                              {lesson.topics.map((t) => (
                                <span
                                  key={t.id}
                                  className="text-[10px] font-medium px-2 py-0.5 rounded-md bg-white/[0.04] text-slate-300 border border-white/5"
                                >
                                  {t.name}
                                </span>
                              ))}
                            </div>
                          )}
                        </div>
                      </div>

                      {/* Action Button */}
                      <div className="flex items-center gap-3 shrink-0 self-start md:self-center">
                        <Link
                          href={`/student/lessons/${lesson.id}`}
                          className={`px-5 py-2.5 rounded-xl text-xs font-bold transition-all flex items-center gap-2 ${
                            isCompleted
                              ? "bg-white/[0.05] hover:bg-white/10 text-slate-300"
                              : isCurrent
                              ? "bg-cyan-500 hover:bg-cyan-400 text-black font-extrabold shadow-[0_0_15px_rgba(6,182,212,0.4)] scale-105"
                              : "bg-white/[0.04] hover:bg-white/10 text-slate-400 hover:text-white"
                          }`}
                        >
                          <PlayCircle className="w-4 h-4" />
                          <span>{isCompleted ? "Review" : isCurrent ? "Continue" : "Start"}</span>
                        </Link>
                      </div>
                    </div>
                  </div>
                </React.Fragment>
              );
            })}
          </div>
        </div>
      </div>
    </RoleLayout>
  );
}
