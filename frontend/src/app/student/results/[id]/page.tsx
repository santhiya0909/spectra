"use client";

import React from "react";
import Link from "next/link";
import { useParams } from "next/navigation";
import { useQuery } from "@tanstack/react-query";
import { quizService, QuizResult } from "@/services/quiz.service";
import { RoleLayout } from "@/components/layout/RoleLayout";
import { Badge } from "@/components/common/Badge";
import {
  Award,
  CheckCircle2,
  XCircle,
  Lightbulb,
  ArrowRight,
  RotateCcw,
  BookOpen,
  LayoutDashboard,
  AlertTriangle,
  Loader2,
  Sparkles,
  Trophy,
  Check,
  ChevronRight
} from "lucide-react";

export default function QuizResultPage() {
  const params = useParams();
  const attemptId = Number(params?.id);

  const { data: result, isLoading } = useQuery<QuizResult>({
    queryKey: ["quizResult", attemptId],
    queryFn: () => quizService.getAttemptDetail(attemptId),
    enabled: !!attemptId,
  });

  const isPassed = result?.status === "PASSED";
  const isPerfect = result?.percentage === 100;
  const xpEarned = isPassed ? (isPerfect ? 40 : 25) : 0;

  return (
    <RoleLayout allowedRoles={["STUDENT", "ADMIN"]}>
      <div className="mx-auto max-w-4xl space-y-8 pb-20">
        {isLoading ? (
          <div className="flex h-96 flex-col items-center justify-center gap-3">
            <Loader2 className="h-8 w-8 animate-spin text-indigo-600 dark:text-indigo-400" />
            <p className="text-sm font-medium text-slate-500 dark:text-slate-400">Grading assessment and calculating XP rewards...</p>
          </div>
        ) : result ? (
          <div className="space-y-8">
            {/* Celebration Banner — always dark gradient so no dark: needed */}
            <div className={`relative overflow-hidden rounded-3xl p-6 sm:p-8 text-white shadow-xl ${
              isPassed
                ? "bg-gradient-to-r from-emerald-600 via-teal-700 to-indigo-900 shadow-emerald-950/10"
                : "bg-gradient-to-r from-slate-900 via-rose-900 to-indigo-950 shadow-rose-950/10"
            }`}>
              <div className="relative z-10 flex flex-col sm:flex-row sm:items-center justify-between gap-6">
                <div className="space-y-2">
                  <div className="flex items-center gap-2">
                    <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-white/20 backdrop-blur-md text-xs font-bold uppercase tracking-wider text-white border border-white/10">
                      {isPassed ? <Trophy className="w-3.5 h-3.5 text-amber-300" /> : <AlertTriangle className="w-3.5 h-3.5 text-rose-300" />}
                      {isPassed ? "Assessment Passed 🎉" : "Needs Review"}
                    </span>
                    {xpEarned > 0 && (
                      <span className="inline-flex items-center gap-1 px-3 py-1 rounded-full bg-amber-400 text-slate-950 text-xs font-black shadow-sm">
                        <Sparkles className="w-3.5 h-3.5" /> +{xpEarned} XP Earned!
                      </span>
                    )}
                  </div>
                  <h1 className="text-2xl sm:text-3xl font-black text-white">{result.quiz_title}</h1>
                  <p className="text-sm text-indigo-100">
                    Accuracy Breakdown: {result.score} of {result.total_questions} questions correct ({result.percentage}%)
                  </p>
                </div>
                <div className="flex items-center gap-4 self-start sm:self-center">
                  <div className="text-center bg-white/15 rounded-2xl p-5 backdrop-blur-md border border-white/20 min-w-[120px]">
                    <span className="text-3xl sm:text-4xl font-black text-white block">{result.percentage}%</span>
                    <span className={`inline-block text-[11px] font-extrabold uppercase mt-1 px-2 py-0.5 rounded-full ${
                      isPassed ? "bg-emerald-400/20 text-emerald-200" : "bg-rose-400/20 text-rose-200"
                    }`}>
                      {result.status}
                    </span>
                  </div>
                </div>
              </div>
            </div>

            {/* Quick Actions Bar */}
            <div className="flex flex-wrap items-center justify-between gap-3 rounded-2xl border border-slate-200/90 dark:border-white/[0.08] bg-white dark:bg-[#0B1124]/85 p-4 shadow-sm">
              <Link
                href="/student/dashboard"
                className="inline-flex items-center gap-1.5 text-xs font-bold text-slate-700 dark:text-slate-300 hover:text-slate-900 dark:hover:text-white px-3 py-2 rounded-xl hover:bg-slate-100 dark:hover:bg-white/[0.06] transition-colors"
              >
                <LayoutDashboard className="h-4 w-4" />
                <span>Return to Dashboard</span>
              </Link>
              <div className="flex items-center gap-2">
                <Link
                  href={`/student/quizzes/${result.quiz_id}`}
                  className="inline-flex items-center gap-1.5 rounded-xl border border-slate-200 dark:border-white/[0.08] bg-white dark:bg-white/[0.04] px-4 py-2 text-xs font-bold text-slate-700 dark:text-slate-300 hover:bg-slate-50 dark:hover:bg-white/[0.08] shadow-sm transition"
                >
                  <RotateCcw className="h-3.5 w-3.5" />
                  <span>Retake Assessment</span>
                </Link>
                <Link
                  href="/student/subjects"
                  className="inline-flex items-center gap-1.5 rounded-xl bg-indigo-600 px-5 py-2 text-xs font-bold text-white hover:bg-indigo-700 shadow-md shadow-indigo-200 dark:shadow-indigo-950/40 transition"
                >
                  <span>Continue Curriculum</span>
                  <ArrowRight className="h-3.5 w-3.5" />
                </Link>
              </div>
            </div>

            {/* Knowledge Gap & Recommendations */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="rounded-2xl border border-amber-200/80 dark:border-amber-500/20 bg-gradient-to-br from-amber-50/70 dark:from-amber-900/10 to-white dark:to-[#0B1124]/85 p-5 shadow-sm space-y-3">
                <div className="flex items-center gap-2">
                  <div className="w-8 h-8 rounded-xl bg-amber-500 text-white flex items-center justify-center">
                    <AlertTriangle className="h-4 w-4" />
                  </div>
                  <div>
                    <h3 className="font-bold text-slate-900 dark:text-white text-sm">Knowledge Gap Diagnostic</h3>
                    <p className="text-[11px] text-slate-500 dark:text-slate-400">Targeted reinforcement</p>
                  </div>
                </div>
                {result.weak_topics && result.weak_topics.length > 0 ? (
                  <div>
                    <p className="text-xs text-slate-600 dark:text-slate-400 mb-2">Accuracy fell below 60% on these specific areas:</p>
                    <div className="flex flex-wrap gap-2">
                      {result.weak_topics.map((wt, i) => (
                        <span key={i} className="px-2.5 py-1 rounded-lg bg-rose-50 dark:bg-rose-950/20 text-rose-700 dark:text-rose-300 border border-rose-200 dark:border-rose-500/30 font-bold text-xs">
                          {wt}
                        </span>
                      ))}
                    </div>
                  </div>
                ) : (
                  <p className="text-xs text-emerald-700 dark:text-emerald-400 font-semibold flex items-center gap-1.5">
                    <CheckCircle2 className="w-4 h-4 text-emerald-500" />
                    No critical weak spots detected! Outstanding accuracy.
                  </p>
                )}
              </div>

              <div className="rounded-2xl border border-indigo-200/80 dark:border-indigo-500/20 bg-gradient-to-br from-indigo-50/70 dark:from-indigo-900/10 to-white dark:to-[#0B1124]/85 p-5 shadow-sm space-y-3">
                <div className="flex items-center gap-2">
                  <div className="w-8 h-8 rounded-xl bg-indigo-600 text-white flex items-center justify-center">
                    <Lightbulb className="h-4 w-4" />
                  </div>
                  <div>
                    <h3 className="font-bold text-slate-900 dark:text-white text-sm">Adaptive Next Steps</h3>
                    <p className="text-[11px] text-slate-500 dark:text-slate-400">Personalized learning engine</p>
                  </div>
                </div>
                <div className="space-y-1.5">
                  {(result.recommendations_generated || []).map((rec, i) => (
                    <div key={i} className="flex items-center gap-2 text-xs font-semibold text-slate-800 dark:text-slate-200">
                      <span className="h-1.5 w-1.5 rounded-full bg-indigo-600 shrink-0" />
                      <span>{rec}</span>
                    </div>
                  ))}
                  {(!result.recommendations_generated || result.recommendations_generated.length === 0) && (
                    <p className="text-xs text-slate-500 dark:text-slate-400">Proceed to the next module in your sequential curriculum.</p>
                  )}
                </div>
              </div>
            </div>

            {/* Question Breakdown */}
            <div className="space-y-4">
              <h3 className="text-lg font-bold text-slate-900 dark:text-white">Question-by-Question Review</h3>
              <div className="space-y-4">
                {(result.questions_review || []).map((item, idx) => (
                  <div
                    key={item.id}
                    className={`rounded-2xl border p-5 sm:p-6 shadow-sm transition-all ${
                      item.is_correct
                        ? "border-emerald-200 dark:border-emerald-500/20 bg-emerald-50/20 dark:bg-emerald-900/[0.08]"
                        : "border-rose-200 dark:border-rose-500/20 bg-rose-50/20 dark:bg-rose-900/[0.06]"
                    }`}
                  >
                    <div className="flex items-start justify-between gap-3 mb-2">
                      <div className="flex items-center gap-2">
                        <span className="text-xs font-extrabold text-slate-400">#{idx + 1}</span>
                        <span className="text-xs font-semibold text-slate-500 dark:text-slate-400 uppercase">{item.topic_name}</span>
                      </div>
                      <span className={`inline-flex items-center gap-1 text-xs font-bold px-2.5 py-0.5 rounded-full ${
                        item.is_correct
                          ? "bg-emerald-100 dark:bg-emerald-900/30 text-emerald-800 dark:text-emerald-300"
                          : "bg-rose-100 dark:bg-rose-900/30 text-rose-800 dark:text-rose-300"
                      }`}>
                        {item.is_correct ? (
                          <><Check className="h-3 w-3" /> Correct</>
                        ) : (
                          <><XCircle className="h-3 w-3" /> Incorrect</>
                        )}
                      </span>
                    </div>

                    <h4 className="text-sm sm:text-base font-bold text-slate-900 dark:text-white leading-snug">{item.question_text}</h4>

                    <div className="mt-4 grid grid-cols-1 sm:grid-cols-2 gap-3 text-xs">
                      <div className={`p-3.5 rounded-xl border ${
                        item.is_correct
                          ? "border-emerald-300 dark:border-emerald-500/30 bg-emerald-50 dark:bg-emerald-900/15 text-emerald-900 dark:text-emerald-200 font-semibold"
                          : "border-rose-300 dark:border-rose-500/30 bg-rose-50 dark:bg-rose-900/15 text-rose-900 dark:text-rose-200 font-semibold"
                      }`}>
                        <span className="block text-[10px] font-bold text-slate-500 dark:text-slate-400 uppercase tracking-wider mb-1">Your Answer</span>
                        {item.selected_answer || "No answer selected"}
                      </div>
                      <div className="p-3.5 rounded-xl border border-slate-200 dark:border-white/[0.08] bg-white dark:bg-white/[0.04] text-slate-900 dark:text-white font-semibold">
                        <span className="block text-[10px] font-bold text-emerald-600 dark:text-emerald-400 uppercase tracking-wider mb-1">Correct Answer</span>
                        {item.correct_answer}
                      </div>
                    </div>

                    {item.explanation && (
                      <div className="mt-4 rounded-xl border border-slate-200 dark:border-white/[0.08] bg-white dark:bg-white/[0.03] p-3.5 text-xs text-slate-600 dark:text-slate-400 leading-relaxed">
                        <span className="font-bold text-slate-900 dark:text-white block mb-1">Explanation:</span>
                        {item.explanation}
                      </div>
                    )}
                  </div>
                ))}
              </div>
            </div>
          </div>
        ) : (
          <div className="rounded-2xl border border-dashed border-slate-300 dark:border-white/10 p-8 text-center text-slate-500 dark:text-slate-400">
            Assessment result not found.
          </div>
        )}
      </div>
    </RoleLayout>
  );
}
