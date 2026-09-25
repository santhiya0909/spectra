"use client";

import React, { useState, useEffect } from "react";
import Link from "next/link";
import { useParams, useRouter } from "next/navigation";
import { useQuery, useMutation } from "@tanstack/react-query";
import { quizService, Question, QuizResult } from "@/services/quiz.service";
import { RoleLayout } from "@/components/layout/RoleLayout";
import { Badge } from "@/components/common/Badge";
import {
  ArrowLeft,
  ArrowRight,
  Clock,
  CheckCircle2,
  AlertCircle,
  Loader2,
  Sparkles,
  Send,
  HelpCircle
} from "lucide-react";

export default function ActiveQuizPage() {
  const params = useParams();
  const router = useRouter();
  const quizId = Number(params?.id);

  // Fetch quiz questions
  const { data: questions, isLoading, error } = useQuery<Question[]>({
    queryKey: ["activeQuiz", quizId],
    queryFn: () => quizService.startQuiz(quizId),
    enabled: !!quizId,
  });

  const [currentIndex, setCurrentIndex] = useState(0);
  const [selectedAnswers, setSelectedAnswers] = useState<Record<number, string>>({});
  const [timeElapsed, setTimeElapsed] = useState(0);
  const [showConfirmModal, setShowConfirmModal] = useState(false);

  // Timer
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
          <Loader2 className="h-8 w-8 animate-spin text-brand-600" />
          <p className="text-sm font-medium text-slate-500">Preparing adaptive diagnostic questions...</p>
        </div>
      </RoleLayout>
    );
  }

  if (error || !questions || questions.length === 0) {
    return (
      <RoleLayout allowedRoles={["STUDENT", "ADMIN"]}>
        <div className="rounded-2xl border border-rose-200 bg-rose-50 p-6 text-center text-rose-700">
          <AlertCircle className="h-8 w-8 mx-auto mb-2 text-rose-600" />
          <h3 className="font-bold">Unable to load quiz assessment</h3>
          <p className="text-xs mt-1">Please try again or select another quiz.</p>
          <Link
            href="/student/quizzes"
            className="mt-4 inline-block rounded-xl bg-slate-900 px-4 py-2 text-xs font-semibold text-white"
          >
            Back to Quizzes
          </Link>
        </div>
      </RoleLayout>
    );
  }

  const currentQ = questions[currentIndex];
  const totalQ = questions.length;
  const answeredCount = Object.keys(selectedAnswers).length;

  return (
    <RoleLayout allowedRoles={["STUDENT", "ADMIN"]}>
      <div className="mx-auto max-w-3xl space-y-6">
        {/* Top Status Bar */}
        <div className="flex items-center justify-between rounded-2xl border border-slate-200 bg-white px-5 py-3.5 shadow-sm">
          <Link
            href="/student/quizzes"
            className="inline-flex items-center gap-1.5 text-xs font-semibold text-slate-500 hover:text-slate-800"
          >
            <ArrowLeft className="h-4 w-4" />
            <span>Exit</span>
          </Link>

          <div className="flex items-center gap-4">
            <div className="flex items-center gap-1.5 text-xs font-bold text-slate-700 bg-slate-100 px-3 py-1.5 rounded-lg">
              <Clock className="h-3.5 w-3.5 text-slate-500" />
              <span>{formatTime(timeElapsed)}</span>
            </div>

            <button
              onClick={() => setShowConfirmModal(true)}
              className="rounded-xl bg-brand-600 px-4 py-1.5 text-xs font-bold text-white shadow-sm hover:bg-brand-700 transition"
            >
              Finish & Submit
            </button>
          </div>
        </div>

        {/* Question Navigation Bubbles */}
        <div className="flex flex-wrap gap-2 rounded-2xl border border-slate-200 bg-white p-3.5 shadow-sm">
          {questions.map((q, idx) => {
            const isAnswered = !!selectedAnswers[q.id];
            const isCurrent = idx === currentIndex;

            return (
              <button
                key={q.id}
                onClick={() => setCurrentIndex(idx)}
                className={`flex h-8 w-8 items-center justify-center rounded-lg text-xs font-bold transition ${
                  isCurrent
                    ? "bg-brand-600 text-white shadow"
                    : isAnswered
                    ? "bg-brand-100 text-brand-800 border border-brand-200"
                    : "bg-slate-100 text-slate-600 hover:bg-slate-200"
                }`}
              >
                {idx + 1}
              </button>
            );
          })}
        </div>

        {/* Question Card */}
        <div className="rounded-3xl border border-slate-200 bg-white p-6 sm:p-8 shadow-sm">
          <div className="flex items-center justify-between mb-4">
            <span className="text-xs font-bold text-slate-400 uppercase tracking-wider">
              Question {currentIndex + 1} of {totalQ} &bull; {currentQ.topic_name}
            </span>
            <Badge
              variant={currentQ.difficulty === "EASY" ? "emerald" : currentQ.difficulty === "MEDIUM" ? "brand" : "purple"}
              size="sm"
            >
              {currentQ.difficulty}
            </Badge>
          </div>

          <h2 className="text-lg sm:text-xl font-bold text-slate-900 leading-snug">
            {currentQ.question_text}
          </h2>

          {/* Options */}
          <div className="mt-6 space-y-3">
            {currentQ.options.map((option, optIdx) => {
              const isSelected = selectedAnswers[currentQ.id] === option;

              return (
                <div
                  key={optIdx}
                  onClick={() => handleSelectOption(currentQ.id, option)}
                  className={`flex items-center gap-3 rounded-2xl border p-4 cursor-pointer transition ${
                    isSelected
                      ? "border-brand-500 bg-brand-50/70 shadow-sm"
                      : "border-slate-200 bg-white hover:bg-slate-50 hover:border-slate-300"
                  }`}
                >
                  <div
                    className={`flex h-5 w-5 shrink-0 items-center justify-center rounded-full border text-xs font-bold ${
                      isSelected
                        ? "border-brand-600 bg-brand-600 text-white"
                        : "border-slate-300 bg-white text-slate-500"
                    }`}
                  >
                    {isSelected && <CheckCircle2 className="h-3.5 w-3.5" />}
                  </div>
                  <span className={`text-sm ${isSelected ? "font-semibold text-brand-900" : "text-slate-700"}`}>
                    {option}
                  </span>
                </div>
              );
            })}
          </div>

          {/* Bottom Nav inside Question */}
          <div className="mt-8 flex items-center justify-between border-t border-slate-100 pt-5">
            <button
              onClick={() => setCurrentIndex((prev) => Math.max(0, prev - 1))}
              disabled={currentIndex === 0}
              className="inline-flex items-center gap-1.5 rounded-xl border border-slate-200 px-4 py-2 text-xs font-semibold text-slate-700 hover:bg-slate-50 disabled:opacity-40"
            >
              <ArrowLeft className="h-3.5 w-3.5" />
              <span>Previous</span>
            </button>

            {currentIndex < totalQ - 1 ? (
              <button
                onClick={() => setCurrentIndex((prev) => Math.min(totalQ - 1, prev + 1))}
                className="inline-flex items-center gap-1.5 rounded-xl bg-slate-900 px-4 py-2 text-xs font-semibold text-white hover:bg-slate-800"
              >
                <span>Next Question</span>
                <ArrowRight className="h-3.5 w-3.5" />
              </button>
            ) : (
              <button
                onClick={() => setShowConfirmModal(true)}
                className="inline-flex items-center gap-1.5 rounded-xl bg-brand-600 px-5 py-2 text-xs font-bold text-white shadow hover:bg-brand-700"
              >
                <Send className="h-3.5 w-3.5" />
                <span>Submit Assessment</span>
              </button>
            )}
          </div>
        </div>

        {/* Submit Confirmation Modal */}
        {showConfirmModal && (
          <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/50 backdrop-blur-sm p-4">
            <div className="w-full max-w-md rounded-3xl bg-white p-6 shadow-xl border border-slate-200">
              <div className="flex h-12 w-12 items-center justify-center rounded-2xl bg-brand-50 text-brand-600 mb-4">
                <Send className="h-6 w-6" />
              </div>
              <h3 className="text-lg font-bold text-slate-900">Submit Quiz Assessment?</h3>
              <p className="text-xs text-slate-500 mt-1 leading-relaxed">
                You have answered <span className="font-bold text-slate-900">{answeredCount}</span> of{" "}
                <span className="font-bold text-slate-900">{totalQ}</span> questions.
                {answeredCount < totalQ && (
                  <span className="block text-amber-600 font-semibold mt-1">
                    Warning: You have {totalQ - answeredCount} unanswered questions!
                  </span>
                )}
              </p>

              <div className="mt-6 flex items-center justify-end gap-3">
                <button
                  type="button"
                  onClick={() => setShowConfirmModal(false)}
                  disabled={submitMutation.isPending}
                  className="rounded-xl border border-slate-200 px-4 py-2 text-xs font-semibold text-slate-700 hover:bg-slate-50"
                >
                  Return to Quiz
                </button>
                <button
                  type="button"
                  onClick={() => submitMutation.mutate()}
                  disabled={submitMutation.isPending}
                  className="inline-flex items-center gap-2 rounded-xl bg-brand-600 px-5 py-2 text-xs font-bold text-white shadow hover:bg-brand-700 disabled:opacity-50"
                >
                  {submitMutation.isPending ? (
                    <>
                      <Loader2 className="h-4 w-4 animate-spin" />
                      <span>Grading & Analyzing...</span>
                    </>
                  ) : (
                    <span>Confirm & Submit</span>
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
