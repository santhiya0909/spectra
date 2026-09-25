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
  Loader2
} from "lucide-react";

export default function QuizResultPage() {
  const params = useParams();
  const attemptId = Number(params?.id);

  const { data: result, isLoading } = useQuery<QuizResult>({
    queryKey: ["quizResult", attemptId],
    queryFn: () => quizService.getAttemptDetail(attemptId),
    enabled: !!attemptId,
  });

  return (
    <RoleLayout allowedRoles={["STUDENT", "ADMIN"]}>
      <div className="mx-auto max-w-4xl space-y-6">
        {isLoading ? (
          <div className="flex h-96 flex-col items-center justify-center gap-3">
            <Loader2 className="h-8 w-8 animate-spin text-brand-600" />
            <p className="text-sm font-medium text-slate-500">Loading diagnostic results and recommendations...</p>
          </div>
        ) : result ? (
          <div className="space-y-6">
            {/* Score Summary Banner */}
            <div className="rounded-3xl bg-gradient-to-r from-slate-900 via-brand-900 to-indigo-950 p-6 sm:p-8 text-white shadow-xl">
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-6">
                <div>
                  <span className="inline-flex items-center gap-1 text-xs font-bold uppercase tracking-wider text-accent-400">
                    <Award className="h-4 w-4" /> Assessment Evaluation
                  </span>
                  <h1 className="text-2xl sm:text-3xl font-extrabold mt-1">{result.quiz_title}</h1>
                  <p className="text-xs text-slate-300 mt-1">
                    Completed Attempt #{result.attempt_id} &bull; Score: {result.score}/{result.total_questions} Questions Correct
                  </p>
                </div>

                <div className="flex items-center gap-4 self-start sm:self-center">
                  <div className="text-center bg-white/10 rounded-2xl p-4 backdrop-blur border border-white/15 min-w-[110px]">
                    <span className="text-3xl sm:text-4xl font-black text-white">{result.percentage}%</span>
                    <span className="block text-[11px] font-semibold text-brand-200 uppercase mt-0.5">
                      {result.status}
                    </span>
                  </div>
                </div>
              </div>
            </div>

            {/* Knowledge Gap & Recommendations Alert */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {/* Weak Topics */}
              <div className="rounded-2xl border border-amber-200 bg-amber-50/60 p-5 shadow-sm">
                <div className="flex items-center gap-2 mb-2">
                  <AlertTriangle className="h-5 w-5 text-amber-600" />
                  <h3 className="font-bold text-slate-900 text-sm">Knowledge Gap Diagnostic</h3>
                </div>
                {result.weak_topics && result.weak_topics.length > 0 ? (
                  <div>
                    <p className="text-xs text-slate-600 mb-3">
                      The analyzer flagged the following weak areas based on your responses:
                    </p>
                    <div className="flex flex-wrap gap-2">
                      {result.weak_topics.map((wt, i) => (
                        <Badge key={i} variant="rose" size="md">
                          {wt}
                        </Badge>
                      ))}
                    </div>
                  </div>
                ) : (
                  <p className="text-xs text-emerald-700 font-medium">
                    No critical weak spots identified! Solid performance demonstrated across all tested topics.
                  </p>
                )}
              </div>

              {/* Generated Recommendations */}
              <div className="rounded-2xl border border-brand-200 bg-brand-50/60 p-5 shadow-sm">
                <div className="flex items-center gap-2 mb-2">
                  <Lightbulb className="h-5 w-5 text-brand-600" />
                  <h3 className="font-bold text-slate-900 text-sm">Adaptive Next Steps</h3>
                </div>
                <p className="text-xs text-slate-600 mb-3">
                  Recommendation engine updated your personalized learning path:
                </p>
                <div className="space-y-1.5">
                  {(result.recommendations_generated || []).map((rec, i) => (
                    <div key={i} className="flex items-center gap-2 text-xs font-semibold text-brand-900">
                      <span className="h-1.5 w-1.5 rounded-full bg-brand-600" />
                      <span>{rec}</span>
                    </div>
                  ))}
                  {(!result.recommendations_generated || result.recommendations_generated.length === 0) && (
                    <p className="text-xs text-slate-500">No new recommendations generated for this attempt.</p>
                  )}
                </div>
              </div>
            </div>

            {/* Quick Actions */}
            <div className="flex flex-wrap items-center justify-between gap-3 rounded-2xl border border-slate-200 bg-white p-4 shadow-sm">
              <Link
                href="/student/dashboard"
                className="inline-flex items-center gap-1.5 text-xs font-bold text-slate-700 hover:text-slate-900 px-3 py-2 rounded-xl hover:bg-slate-100"
              >
                <LayoutDashboard className="h-4 w-4" />
                <span>Return to Dashboard</span>
              </Link>

              <div className="flex items-center gap-2">
                <Link
                  href={`/student/quizzes/${result.quiz_id}`}
                  className="inline-flex items-center gap-1.5 rounded-xl border border-slate-200 bg-white px-3.5 py-2 text-xs font-bold text-slate-700 hover:bg-slate-50 shadow-sm"
                >
                  <RotateCcw className="h-3.5 w-3.5" />
                  <span>Retake Assessment</span>
                </Link>
                <Link
                  href="/student/recommendations"
                  className="inline-flex items-center gap-1.5 rounded-xl bg-brand-600 px-4 py-2 text-xs font-bold text-white hover:bg-brand-700 shadow-sm"
                >
                  <span>View Recommendations</span>
                  <ArrowRight className="h-3.5 w-3.5" />
                </Link>
              </div>
            </div>

            {/* Question Breakdown with Explanations */}
            <div className="space-y-4">
              <h3 className="text-lg font-bold text-slate-900">Question-by-Question Review</h3>

              <div className="space-y-4">
                {(result.questions_review || []).map((item, idx) => (
                  <div
                    key={item.id}
                    className={`rounded-2xl border p-5 sm:p-6 shadow-sm ${
                      item.is_correct
                        ? "border-emerald-200 bg-emerald-50/20"
                        : "border-rose-200 bg-rose-50/20"
                    }`}
                  >
                    <div className="flex items-start justify-between gap-3 mb-2">
                      <div className="flex items-center gap-2">
                        <span className="text-xs font-bold text-slate-400">#{idx + 1}</span>
                        <span className="text-xs font-semibold text-slate-500 uppercase">
                          {item.topic_name}
                        </span>
                      </div>
                      <Badge variant={item.is_correct ? "emerald" : "rose"} size="sm">
                        {item.is_correct ? (
                          <span className="flex items-center gap-1">
                            <CheckCircle2 className="h-3 w-3" /> Correct
                          </span>
                        ) : (
                          <span className="flex items-center gap-1">
                            <XCircle className="h-3 w-3" /> Incorrect
                          </span>
                        )}
                      </Badge>
                    </div>

                    <h4 className="text-sm sm:text-base font-bold text-slate-900 leading-snug">
                      {item.question_text}
                    </h4>

                    {/* Answers */}
                    <div className="mt-4 grid grid-cols-1 sm:grid-cols-2 gap-3 text-xs">
                      <div className={`p-3 rounded-xl border ${
                        item.is_correct
                          ? "border-emerald-300 bg-emerald-50 text-emerald-900 font-semibold"
                          : "border-rose-300 bg-rose-50 text-rose-900 font-semibold"
                      }`}>
                        <span className="block text-[11px] font-bold text-slate-500 uppercase mb-1">
                          Your Answer
                        </span>
                        {item.selected_answer || "No answer selected"}
                      </div>

                      <div className="p-3 rounded-xl border border-slate-200 bg-white text-slate-900 font-semibold">
                        <span className="block text-[11px] font-bold text-emerald-600 uppercase mb-1">
                          Correct Answer
                        </span>
                        {item.correct_answer}
                      </div>
                    </div>

                    {/* Explanation */}
                    {item.explanation && (
                      <div className="mt-4 rounded-xl border border-slate-200 bg-white p-3 text-xs text-slate-600">
                        <span className="font-bold text-slate-900 block mb-0.5">Explanation:</span>
                        {item.explanation}
                      </div>
                    )}
                  </div>
                ))}
              </div>
            </div>
          </div>
        ) : (
          <div className="rounded-2xl border border-dashed border-slate-300 p-8 text-center text-slate-500">
            Assessment result not found.
          </div>
        )}
      </div>
    </RoleLayout>
  );
}
