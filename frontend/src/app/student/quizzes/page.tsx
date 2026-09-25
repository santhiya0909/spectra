"use client";

import React from "react";
import Link from "next/link";
import { useQuery } from "@tanstack/react-query";
import { quizService, Quiz } from "@/services/quiz.service";
import { RoleLayout } from "@/components/layout/RoleLayout";
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
  RefreshCw
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
      <div className="space-y-6">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div>
            <h1 className="text-2xl font-bold tracking-tight text-slate-900">Adaptive Quiz Catalog</h1>
            <p className="mt-1 text-sm text-slate-500">
              Assessments adjust question difficulty dynamically to evaluate and diagnose your core topic mastery.
            </p>
          </div>

          <button
            onClick={() => refetch()}
            disabled={isFetching}
            className="inline-flex items-center gap-1.5 rounded-xl border border-slate-200 bg-white px-3.5 py-2 text-xs font-semibold text-slate-700 shadow-sm hover:bg-slate-50 transition disabled:opacity-50 self-start sm:self-center"
          >
            <RefreshCw className={`h-3.5 w-3.5 text-slate-500 ${isFetching ? "animate-spin" : ""}`} />
            <span>Refresh</span>
          </button>
        </div>

        {/* Demo Diagnostic Highlighting */}
        <div className="rounded-3xl border border-brand-200 bg-gradient-to-r from-brand-50 to-indigo-50/50 p-6 shadow-sm">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
            <div className="flex items-start gap-3.5">
              <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-2xl bg-brand-600 text-white shadow-md">
                <BrainCircuit className="h-5 w-5" />
              </div>
              <div>
                <span className="text-[11px] font-bold uppercase tracking-wider text-brand-700">
                  Targeted Learning Loop Diagnostic
                </span>
                <h3 className="text-base font-bold text-slate-900 mt-0.5">
                  Java Functions & Parameters Assessment
                </h3>
                <p className="text-xs text-slate-600 mt-1 max-w-xl">
                  Test your understanding of method signatures, parameter passing, and recursion.
                  Your score dynamically feeds into the knowledge gap detection engine.
                </p>
              </div>
            </div>

            <Link
              href="/student/quizzes/1"
              className="inline-flex items-center gap-2 rounded-xl bg-brand-600 px-5 py-2.5 text-xs font-bold text-white shadow-md shadow-brand-500/20 hover:bg-brand-700 transition self-start sm:self-center shrink-0"
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
              <div key={i} className="h-48 bg-slate-200 rounded-2xl" />
            ))}
          </div>
        ) : error ? (
          <div className="rounded-2xl border border-rose-200 bg-rose-50 p-6 text-center text-rose-700">
            <AlertCircle className="h-8 w-8 mx-auto mb-2 text-rose-600" />
            <h3 className="font-bold text-sm">Failed to load quizzes</h3>
            <p className="text-xs text-rose-600 mt-1">{(error as any)?.message || "Please try again."}</p>
            <button
              onClick={() => refetch()}
              className="mt-4 inline-flex items-center gap-1.5 rounded-xl bg-rose-600 px-4 py-2 text-xs font-semibold text-white shadow hover:bg-rose-700"
            >
              <RefreshCw className="h-3.5 w-3.5" />
              <span>Retry</span>
            </button>
          </div>
        ) : quizzes.length === 0 ? (
          <div className="rounded-3xl border border-dashed border-slate-300 bg-white p-12 text-center text-slate-500">
            <HelpCircle className="h-10 w-10 mx-auto text-slate-400 mb-2" />
            <h3 className="font-bold text-slate-900">No assessments found</h3>
            <p className="text-xs text-slate-500 mt-1">Check back later or explore curriculum lessons.</p>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {quizzes.map((quiz) => (
              <div
                key={quiz.id}
                className="flex flex-col justify-between rounded-2xl border border-slate-200 bg-white p-6 shadow-sm hover:border-brand-200 hover:shadow-md transition"
              >
                <div>
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-[11px] font-bold text-slate-400 uppercase tracking-wider">
                      {quiz.subject_name || "General Assessment"}
                    </span>
                    <Badge
                      variant={quiz.quiz_type === "ADAPTIVE" ? "cyan" : "brand"}
                      size="sm"
                    >
                      {quiz.quiz_type}
                    </Badge>
                  </div>

                  <h3 className="text-lg font-bold text-slate-900 mt-1">{quiz.title}</h3>
                  <p className="text-xs text-slate-600 mt-2 line-clamp-2 leading-relaxed">
                    {quiz.description || "Diagnose foundational and advanced concepts."}
                  </p>
                </div>

                <div className="mt-6 border-t border-slate-100 pt-4 flex items-center justify-between">
                  <div className="flex items-center gap-3 text-xs text-slate-500 font-medium">
                    <span className="flex items-center gap-1">
                      <HelpCircle className="h-3.5 w-3.5 text-slate-400" />
                      {quiz.question_count} Questions
                    </span>
                    {quiz.best_score !== null && quiz.best_score !== undefined && (
                      <span className="flex items-center gap-1 font-semibold text-emerald-600">
                        <Award className="h-3.5 w-3.5" />
                        Best: {quiz.best_score}%
                      </span>
                    )}
                  </div>

                  <Link
                    href={`/student/quizzes/${quiz.id}`}
                    className="inline-flex items-center gap-1.5 rounded-xl bg-slate-900 px-4 py-2 text-xs font-semibold text-white shadow hover:bg-brand-600 transition"
                  >
                    <PlayCircle className="h-4 w-4" />
                    <span>{quiz.attempts_count ? "Retake Quiz" : "Start Quiz"}</span>
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
