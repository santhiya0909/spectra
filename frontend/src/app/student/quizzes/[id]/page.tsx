"use client";

import React, { useState, useEffect } from "react";
import Link from "next/link";
import { useParams, useRouter } from "next/navigation";
import { useQuery, useMutation } from "@tanstack/react-query";
import { quizService, Question, QuizResult } from "@/services/quiz.service";
import { RoleLayout } from "@/components/layout/RoleLayout";
import {
  ArrowLeft,
  ArrowRight,
  Clock,
  CheckCircle2,
  AlertCircle,
  Loader2,
  Sparkles,
  Send,
  HelpCircle,
  Check,
  ChevronLeft,
  ChevronRight
} from "lucide-react";

export default function ActiveQuizPage() {
  const params = useParams();
  const router = useRouter();
  const quizId = Number(params?.id);

  const { data: questions, isLoading, error } = useQuery<Question[]>({
    queryKey: ["activeQuiz", quizId],
    queryFn: () => quizService.startQuiz(quizId),
    enabled: !!quizId,
  });

  const [currentIndex, setCurrentIndex] = useState(0);
  const [selectedAnswers, setSelectedAnswers] = useState<Record<number, string>>({});
  const [timeElapsed, setTimeElapsed] = useState(0);
  const [showConfirmModal, setShowConfirmModal] = useState(false);

  useEffect(() => {
    const timer = setInterval(() => {
      setTimeElapsed((prev) => prev + 1);
    }, 1000);
    return () => clearInterval(timer);
  }, []);

  const formatTime = (seconds: number) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins.toString().padStart(2, "0")}:${secs.toString().padStart(2, "0")}`;
  };

  const handleSelectOption = (questionId: number, option: string) => {
    setSelectedAnswers((prev) => ({
      ...prev,
      [questionId]: option,
    }));
  };

  const submitMutation = useMutation({
    mutationFn: () => {
      const answersPayload = (questions || []).map((q) => ({
        question_id: q.id,
        selected_answer: selectedAnswers[q.id] || "",
        time_taken: Math.max(1, Math.round(timeElapsed / (questions?.length || 1))),
      }));
      return quizService.submitQuiz(quizId, answersPayload);
    },
    onSuccess: (result: QuizResult) => {
      router.push(`/student/results/${result.attempt_id}`);
    },
  });

  if (isLoading) {
    return (
      <RoleLayout allowedRoles={["STUDENT", "ADMIN"]}>
        <div className="flex h-96 flex-col items-center justify-center gap-3">
          <Loader2 className="h-8 w-8 animate-spin text-indigo-600 dark:text-indigo-400" />
          <p className="text-sm font-medium text-slate-500 dark:text-slate-400">Preparing adaptive diagnostic questions...</p>
        </div>
      </RoleLayout>
    );
  }

  if (error || !questions || questions.length === 0) {
    return (
      <RoleLayout allowedRoles={["STUDENT", "ADMIN"]}>
        <div className="rounded-3xl border border-rose-200 dark:border-rose-500/30 bg-rose-50 dark:bg-rose-950/20 p-8 text-center text-rose-700 dark:text-rose-300 max-w-lg mx-auto mt-12">
          <AlertCircle className="h-10 w-10 mx-auto mb-3 text-rose-600 dark:text-rose-400" />
          <h3 className="font-bold text-base">Unable to load quiz assessment</h3>
          <p className="text-xs mt-1 text-slate-600 dark:text-slate-400">Please try again or select another quiz from your curriculum.</p>
          <Link
            href="/student/quizzes"
            className="mt-5 inline-block rounded-xl bg-slate-900 dark:bg-white dark:text-slate-900 px-5 py-2.5 text-xs font-bold text-white shadow-sm"
          >
            Back to Quizzes
          </Link>
        </div>
      </RoleLayout>
    );
  }

  const currentQ = questions[currentIndex];
  const totalQ = questions.length;
  const answeredCount = Object.keys(selectedAnswers).filter(k => Boolean(selectedAnswers[Number(k)])).length;
  const isAnswered = Boolean(selectedAnswers[currentQ?.id]);
  const isLastQuestion = currentIndex === totalQ - 1;

  let optionsList: string[] = [];
  if (currentQ) {
    if (Array.isArray(currentQ.options)) {
      optionsList = currentQ.options;
    } else if (typeof currentQ.options === "string") {
      try {
        optionsList = JSON.parse(currentQ.options);
      } catch {
        optionsList = [];
      }
    }
  }

  return (
    <RoleLayout allowedRoles={["STUDENT", "ADMIN"]}>
      <div className="mx-auto max-w-3xl space-y-6 pb-20">
        {/* Top Sticky Bar */}
        <div className="rounded-3xl border border-slate-200/90 dark:border-white/[0.08] bg-white dark:bg-[#0B1124]/85 p-4 sm:p-5 shadow-sm space-y-3">
          <div className="flex items-center justify-between">
            <Link
              href="/student/quizzes"
              className="inline-flex items-center gap-1.5 text-xs font-semibold text-slate-500 dark:text-slate-400 hover:text-indigo-600 dark:hover:text-indigo-400 transition"
            >
              <ArrowLeft className="h-4 w-4" />
              <span>Quit Assessment</span>
            </Link>

            {/* Timer */}
            <div className="inline-flex items-center gap-2 rounded-xl bg-slate-100 dark:bg-white/[0.06] px-3 py-1.5 text-xs font-mono font-bold text-slate-700 dark:text-slate-200">
              <Clock className="h-4 w-4 text-slate-500 dark:text-slate-400" />
              <span>{formatTime(timeElapsed)}</span>
            </div>

            {/* XP Bonus Indicator */}
            <div className="hidden sm:inline-flex items-center gap-1.5 rounded-full bg-amber-50 dark:bg-amber-900/20 border border-amber-200 dark:border-amber-500/25 px-3 py-1 text-xs font-bold text-amber-700 dark:text-amber-400">
              <Sparkles className="h-3.5 w-3.5 text-amber-500 dark:text-amber-400" />
              <span>+25 XP Pass &bull; +15 XP Perfect</span>
            </div>
          </div>

          {/* Progress Bar & Counter */}
          <div className="space-y-1.5">
            <div className="flex items-center justify-between text-xs font-bold text-slate-600 dark:text-slate-300">
              <span>Question {currentIndex + 1} of {totalQ}</span>
              <span className="text-indigo-600 dark:text-indigo-400">{answeredCount} of {totalQ} answered</span>
            </div>
            <div className="w-full h-2 bg-slate-100 dark:bg-white/[0.08] rounded-full overflow-hidden">
              <div
                className="h-full bg-indigo-600 rounded-full transition-all duration-300"
                style={{ width: `${((currentIndex + 1) / totalQ) * 100}%` }}
              />
            </div>
          </div>
        </div>

        {/* Question Navigator Pills */}
        <div className="flex flex-wrap items-center gap-2 px-1">
          {questions.map((q, idx) => {
            const hasAnswer = Boolean(selectedAnswers[q.id]);
            const isCurr = idx === currentIndex;

            return (
              <button
                key={q.id}
                type="button"
                onClick={() => setCurrentIndex(idx)}
                className={`w-8 h-8 rounded-xl text-xs font-bold transition-all flex items-center justify-center ${
                  isCurr
                    ? "bg-indigo-600 text-white ring-2 ring-indigo-500/20 shadow-sm"
                    : hasAnswer
                    ? "bg-emerald-100 dark:bg-emerald-900/25 text-emerald-800 dark:text-emerald-300 border border-emerald-200 dark:border-emerald-500/30"
                    : "bg-white dark:bg-white/[0.04] border border-slate-200 dark:border-white/[0.08] text-slate-600 dark:text-slate-300 hover:bg-slate-50 dark:hover:bg-white/[0.08]"
                }`}
              >
                {idx + 1}
              </button>
            );
          })}
        </div>

        {/* Main Question Card */}
        <div className="rounded-3xl border border-slate-200/90 dark:border-white/[0.08] bg-white dark:bg-[#0B1124]/85 p-6 sm:p-8 shadow-sm space-y-6">
          <div className="flex items-center justify-between">
            <span className="text-xs font-extrabold uppercase tracking-wider px-2.5 py-1 rounded-lg bg-indigo-50 dark:bg-indigo-900/25 text-indigo-700 dark:text-indigo-300 border border-indigo-100 dark:border-indigo-500/25">
              Multiple Choice
            </span>
            <span className="text-xs font-semibold text-slate-400">
              Difficulty: {currentQ?.difficulty || "MEDIUM"}
            </span>
          </div>

          <h2 className="text-lg sm:text-xl font-bold text-slate-900 dark:text-white leading-snug">
            {currentQ?.question_text}
          </h2>

          {/* Options */}
          <div className="space-y-3 pt-2">
            {optionsList.map((opt, optIdx) => {
              const isSelected = selectedAnswers[currentQ.id] === opt;
              const optionLetter = String.fromCharCode(65 + optIdx);

              return (
                <button
                  key={optIdx}
                  type="button"
                  onClick={() => handleSelectOption(currentQ.id, opt)}
                  className={`w-full text-left p-4 rounded-2xl border text-sm font-medium transition-all flex items-center justify-between ${
                    isSelected
                      ? "border-indigo-600 dark:border-indigo-500 bg-indigo-50/70 dark:bg-indigo-900/25 text-indigo-950 dark:text-indigo-100 ring-2 ring-indigo-500/20 shadow-sm"
                      : "border-slate-200/90 dark:border-white/[0.08] hover:border-slate-300 dark:hover:border-white/20 hover:bg-slate-50 dark:hover:bg-white/[0.04] text-slate-700 dark:text-slate-200 bg-white dark:bg-transparent"
                  }`}
                >
                  <div className="flex items-center gap-3.5 flex-1 pr-3">
                    <span className={`w-8 h-8 rounded-xl font-bold text-xs flex items-center justify-center shrink-0 border ${
                      isSelected
                        ? "bg-indigo-600 text-white border-indigo-600"
                        : "bg-slate-100 dark:bg-white/[0.06] text-slate-600 dark:text-slate-300 border-slate-200 dark:border-white/[0.08]"
                    }`}>
                      {optionLetter}
                    </span>
                    <span className="leading-relaxed">{opt}</span>
                  </div>
                  {isSelected && (
                    <div className="w-6 h-6 rounded-full bg-indigo-600 text-white flex items-center justify-center shrink-0">
                      <Check className="w-3.5 h-3.5 stroke-[3]" />
                    </div>
                  )}
                </button>
              );
            })}
          </div>
        </div>

        {/* Bottom Navigation Buttons */}
        <div className="flex items-center justify-between pt-2">
          <button
            type="button"
            disabled={currentIndex === 0}
            onClick={() => setCurrentIndex((prev) => prev - 1)}
            className="px-5 py-2.5 rounded-xl border border-slate-200 dark:border-white/[0.08] bg-white dark:bg-white/[0.04] hover:bg-slate-50 dark:hover:bg-white/[0.08] text-slate-700 dark:text-slate-300 text-xs font-bold shadow-sm transition-all disabled:opacity-40 disabled:pointer-events-none flex items-center gap-2"
          >
            <ChevronLeft className="w-4 h-4" />
            <span>Previous</span>
          </button>

          <div className="flex items-center gap-3">
            {isLastQuestion ? (
              <button
                type="button"
                onClick={() => setShowConfirmModal(true)}
                className="px-6 py-3 rounded-2xl bg-emerald-600 hover:bg-emerald-700 text-white text-xs font-bold shadow-md shadow-emerald-200 dark:shadow-emerald-950/40 transition-all flex items-center gap-2"
              >
                <Send className="w-4 h-4" />
                <span>Submit Quiz</span>
              </button>
            ) : (
              <button
                type="button"
                onClick={() => setCurrentIndex((prev) => prev + 1)}
                className="px-6 py-3 rounded-2xl bg-indigo-600 hover:bg-indigo-700 text-white text-xs font-bold shadow-md shadow-indigo-200 dark:shadow-indigo-950/40 transition-all flex items-center gap-2"
              >
                <span>Next Question</span>
                <ChevronRight className="w-4 h-4" />
              </button>
            )}
          </div>
        </div>

        {/* Submit Confirmation Modal */}
        {showConfirmModal && (
          <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-sm animate-in fade-in">
            <div className="bg-white dark:bg-[#0B1124] rounded-3xl max-w-sm w-full p-6 shadow-2xl border border-slate-100 dark:border-white/[0.08] text-center space-y-4">
              <div className="w-12 h-12 rounded-2xl bg-indigo-50 dark:bg-indigo-900/25 border border-indigo-100 dark:border-indigo-500/25 text-indigo-600 dark:text-indigo-400 mx-auto flex items-center justify-center">
                <HelpCircle className="w-6 h-6" />
              </div>
              <div>
                <h3 className="text-lg font-bold text-slate-900 dark:text-white">Ready to Submit?</h3>
                <p className="text-xs text-slate-500 dark:text-slate-400 mt-1">
                  You have answered {answeredCount} of {totalQ} questions.
                  {answeredCount < totalQ && (
                    <span className="block text-amber-600 dark:text-amber-400 font-semibold mt-1">
                      Warning: {totalQ - answeredCount} questions are still unanswered!
                    </span>
                  )}
                </p>
              </div>
              <div className="flex items-center gap-3 pt-2">
                <button
                  type="button"
                  onClick={() => setShowConfirmModal(false)}
                  className="flex-1 py-2.5 rounded-xl border border-slate-200 dark:border-white/[0.08] text-slate-700 dark:text-slate-300 text-xs font-bold hover:bg-slate-50 dark:hover:bg-white/[0.06]"
                >
                  Review
                </button>
                <button
                  type="button"
                  disabled={submitMutation.isPending}
                  onClick={() => submitMutation.mutate()}
                  className="flex-1 py-2.5 rounded-xl bg-emerald-600 hover:bg-emerald-700 text-white text-xs font-bold shadow-md shadow-emerald-200 dark:shadow-emerald-950/40 flex items-center justify-center gap-1.5"
                >
                  {submitMutation.isPending ? (
                    <Loader2 className="w-4 h-4 animate-spin" />
                  ) : (
                    <span>Confirm & Grade</span>
                  )}
                </button>
              </div>
            </div>
          </div>
        )}
      </div>
    </RoleLayout>
  );
}
