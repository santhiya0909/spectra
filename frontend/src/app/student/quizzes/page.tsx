"use client";

import React from "react";
import Link from "next/link";
import { useQuery } from "@tanstack/react-query";
import { quizService, Quiz } from "@/services/quiz.service";
import { RoleLayout } from "@/components/layout/RoleLayout";
import { GlassCard } from "@/components/common/GlassCard";
import { Badge } from "@/components/common/Badge";
import {
  HelpCircle,
  PlayCircle,
  Award,
  Clock,
  Sparkles,
  CheckCircle2,
  BrainCircuit,
  AlertCircle,
  RefreshCw,
  Zap,
} from "lucide-react";

export default function StudentQuizzesPage() {
  const { data, isLoading, error, refetch, isFetching } = useQuery<Quiz[]>({
    queryKey: ["quizzes"],
    queryFn: () => quizService.getQuizzes(),
  });

  const rawData = data as any;
  const quizzes: Quiz[] = Array.isArray(rawData)
    ? rawData
    : Array.isArray(rawData?.quizzes)
    ? rawData.quizzes
    : Array.isArray(rawData?.data)
    ? rawData.data
    : [];

  return (
    <RoleLayout allowedRoles={["STUDENT", "ADMIN"]}>
      <div className="space-y-6 pb-14">
        {/* Header */}
        <div className="relative overflow-hidden rounded-3xl bg-gradient-to-r from-[#0B1530] via-[#10103A] to-[#140C2C] p-6 sm:p-8 text-white shadow-xl shadow-cyan-950/20 border border-white/10">
          <div className="absolute -top-16 -right-16 w-72 h-72 bg-cyan-500/15 rounded-full blur-[100px] pointer-events-none" />
          <div className="absolute -bottom-16 -left-16 w-72 h-72 bg-purple-500/15 rounded-full blur-[100px] pointer-events-none" />

          <div className="relative z-10 flex flex-col sm:flex-row sm:items-center justify-between gap-4">
            <div>
              <div className="inline-flex items-center gap-1.5 rounded-full bg-cyan-500/15 px-3 py-1 text-xs font-bold text-cyan-300 border border-cyan-400/30 shadow-[0_0_12px_rgba(6,182,212,0.2)] mb-3">
                <BrainCircuit className="h-3.5 w-3.5 text-cyan-300" />
                <span>Dynamic Assessment &bull; Knowledge Gap Feed</span>
              </div>
              <h1 className="text-2xl sm:text-3xl font-black tracking-tight">Adaptive Quiz Catalog</h1>
              <p className="mt-1 text-sm text-slate-300 max-w-xl font-normal leading-relaxed">
                Assessments adjust question difficulty dynamically to evaluate and diagnose your core topic mastery in real-time.
              </p>
            </div>

            <button
              onClick={() => refetch()}
              disabled={isFetching}
              className="inline-flex items-center gap-1.5 rounded-xl border border-white/10 bg-white/[0.05] hover:bg-white/10 px-4 py-2.5 text-xs font-bold text-slate-300 hover:text-white shadow-sm backdrop-blur-sm transition disabled:opacity-50 self-start sm:self-center"
            >
              <RefreshCw className={`h-3.5 w-3.5 text-cyan-400 ${isFetching ? "animate-spin" : ""}`} />
              <span>Refresh</span>
            </button>
          </div>
        </div>

        {/* Demo Diagnostic Highlighting */}
        <div className="rounded-3xl border border-cyan-500/40 bg-gradient-to-r from-[#0B1530] via-[#101436] to-[#150D2E] p-6 shadow-[0_0_30px_rgba(6,182,212,0.15)] backdrop-blur-2xl">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
            <div className="flex items-start gap-3.5">
              <div className="flex h-11 w-11 shrink-0 items-center justify-center rounded-2xl bg-cyan-500 text-black shadow-[0_0_15px_#22d3ee]">
                <BrainCircuit className="h-6 w-6" />
              </div>
              <div>
                <span className="text-[10px] font-extrabold uppercase tracking-widest text-cyan-300 block">
                  Targeted Learning Loop Diagnostic
                </span>
                <h3 className="text-base font-bold text-white mt-0.5">
                  Java Functions &amp; Parameters Assessment
                </h3>
                <p className="text-xs text-slate-300 mt-1 max-w-xl">
                  Test your understanding of method signatures, parameter passing, and recursion.
                  Your score dynamically feeds into the knowledge gap detection engine.
                </p>
              </div>
            </div>

            <Link
              href="/student/quizzes/1"
              className="inline-flex items-center gap-2 rounded-2xl bg-cyan-500 hover:bg-cyan-400 px-5 py-2.5 text-xs font-black text-black shadow-[0_0_20px_rgba(6,182,212,0.4)] transition self-start sm:self-center shrink-0"
            >
              <PlayCircle className="h-4 w-4" />
              <span>Take Assessment</span>
            </Link>
          </div>
        </div>

        {/* Catalog Grid */}
        {isLoading ? (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6 animate-pulse">
            {[1, 2, 3, 4].map((i) => (
              <div key={i} className="h-48 bg-slate-800/40 rounded-3xl border border-white/5" />
            ))}
          </div>
        ) : error ? (
          <GlassCard className="p-8 text-center border-rose-500/30 bg-rose-950/20 text-rose-300">
            <AlertCircle className="h-8 w-8 mx-auto mb-2 text-rose-400" />
            <h3 className="font-bold text-sm text-white">Failed to load quizzes</h3>
            <p className="text-xs text-rose-300 mt-1">{(error as any)?.message || "Please try again."}</p>
            <button
              onClick={() => refetch()}
              className="mt-4 inline-flex items-center gap-1.5 rounded-xl bg-cyan-500 text-black px-4 py-2 text-xs font-bold shadow hover:bg-cyan-400 transition"
            >
              <RefreshCw className="h-3.5 w-3.5" />
              <span>Retry</span>
            </button>
          </GlassCard>
        ) : quizzes.length === 0 ? (
          <GlassCard className="p-12 text-center">
            <HelpCircle className="h-10 w-10 mx-auto text-slate-500 mb-2" />
            <h3 className="font-bold text-white text-base">No assessments found</h3>
            <p className="text-xs text-slate-400 mt-1">Check back later or explore curriculum lessons.</p>
          </GlassCard>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {quizzes.map((quiz) => (
              <div
                key={quiz.id}
                className="group flex flex-col justify-between rounded-3xl border border-white/[0.08] bg-[#0B1124]/85 p-6 backdrop-blur-xl shadow-lg hover:border-cyan-500/40 hover:shadow-[0_0_25px_-5px_rgba(6,182,212,0.2)] transition-all duration-300 hover:-translate-y-1"
              >
                <div>
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-[10px] font-extrabold uppercase tracking-widest text-slate-400">
                      {quiz.subject_name || "General Assessment"}
                    </span>
                    <Badge
                      variant={quiz.quiz_type === "ADAPTIVE" ? "cyan" : "brand"}
                      size="sm"
                    >
                      {quiz.quiz_type}
                    </Badge>
                  </div>

                  <h3 className="text-base font-bold text-white group-hover:text-cyan-300 transition-colors mt-1">
                    {quiz.title}
                  </h3>
                  <p className="text-xs text-slate-400 mt-2 line-clamp-2 leading-relaxed">
                    {quiz.description || "Diagnose foundational and advanced concepts with real-time feedback."}
                  </p>
                </div>

                <div className="mt-6 border-t border-white/[0.06] pt-4 flex items-center justify-between">
                  <div className="flex items-center gap-3 text-xs text-slate-400 font-medium">
                    <span className="flex items-center gap-1">
                      <HelpCircle className="h-3.5 w-3.5 text-cyan-400" />
                      {quiz.question_count} Questions
                    </span>
                    {quiz.best_score !== null && quiz.best_score !== undefined && (
                      <span className="flex items-center gap-1 font-bold text-emerald-400 font-mono">
                        <Award className="h-3.5 w-3.5" />
                        Best: {quiz.best_score}%
                      </span>
                    )}
                  </div>

                  <Link
                    href={`/student/quizzes/${quiz.id}`}
                    className="inline-flex items-center gap-1.5 rounded-xl bg-cyan-500 hover:bg-cyan-400 text-black px-4 py-2 text-xs font-black shadow-[0_0_12px_rgba(6,182,212,0.3)] transition"
                  >
                    <span>Start</span>
                    <PlayCircle className="h-3.5 w-3.5" />
                  </Link>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </RoleLayout>
  );
}
