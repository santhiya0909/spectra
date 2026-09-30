"use client";

import React, { useState, useEffect } from "react";
import { puzzleService } from "@/services/puzzle.service";
import { 
  X, 
  Sparkles, 
  CheckCircle2, 
  HelpCircle, 
  ArrowRight, 
  ChevronRight,
  Zap,
  Target
} from "lucide-react";

interface TopicPracticeModalProps {
  isOpen: boolean;
  onClose: () => void;
  topicId: number;
  topicName: string;
  onCompleted?: (xpEarned: number) => void;
}

export default function TopicPracticeModal({
  isOpen,
  onClose,
  topicId,
  topicName,
  onCompleted
}: TopicPracticeModalProps) {
  const [questions, setQuestions] = useState<any[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [selectedAnswers, setSelectedAnswers] = useState<Record<number, string>>({});
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [completionResult, setCompletionResult] = useState<{
    xp_earned: number;
    message: string;
  } | null>(null);

  useEffect(() => {
    if (isOpen && topicId) {
      setIsLoading(true);
      setCompletionResult(null);
      setSelectedAnswers({});
      setCurrentIndex(0);
      puzzleService.getTopicPractice(topicId)
        .then((data) => {
          setQuestions(data || []);
        })
        .catch((err) => {
          console.error("Failed to load practice questions", err);
          setQuestions([]);
        })
        .finally(() => {
          setIsLoading(false);
        });
    }
  }, [isOpen, topicId]);

  if (!isOpen) return null;

  const currentQuestion = questions[currentIndex];
  const isLastQuestion = currentIndex === questions.length - 1;

  const handleSelectOption = (opt: string) => {
    if (completionResult) return;
    setSelectedAnswers(prev => ({
      ...prev,
      [currentQuestion.id]: opt,
    }));
  };

  const handleNext = () => {
    if (currentIndex < questions.length - 1) {
      setCurrentIndex(prev => prev + 1);
    }
  };

  const handleSubmit = async () => {
    setIsSubmitting(true);
    try {
      const answersPayload = Object.entries(selectedAnswers).map(([qId, ans]) => ({
        question_id: Number(qId),
        selected_answer: ans,
      }));
      const res = await puzzleService.submitTopicPractice(topicId, answersPayload);
      setCompletionResult({
        xp_earned: res.xp_earned,
        message: res.message || "Topic practice completed successfully!",
      });
      if (onCompleted) {
        onCompleted(res.xp_earned);
      }
    } catch (err) {
      console.error("Error submitting practice", err);
    } finally {
      setIsSubmitting(false);
    }
  };

  // Parse options if stored as string
  let parsedOptions: string[] = [];
  if (currentQuestion) {
    if (Array.isArray(currentQuestion.options)) {
      parsedOptions = currentQuestion.options;
    } else if (typeof currentQuestion.options === "string") {
      try {
        parsedOptions = JSON.parse(currentQuestion.options);
      } catch {
        parsedOptions = [];
      }
    }
  }

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-sm animate-in fade-in">
      <div className="bg-white rounded-3xl max-w-lg w-full shadow-2xl border border-slate-100 overflow-hidden flex flex-col max-h-[90vh]">
        {/* Modal Header */}
        <div className="px-6 py-5 bg-gradient-to-r from-indigo-600 to-purple-600 text-white flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-white/20 backdrop-blur-md flex items-center justify-center text-white">
              <Target className="w-5 h-5" />
            </div>
            <div>
              <span className="text-xs uppercase font-bold tracking-wider text-indigo-200">
                Quick Concept Practice
              </span>
              <h3 className="text-base font-bold text-white line-clamp-1">
                {topicName}
              </h3>
            </div>
          </div>
          <button
            onClick={onClose}
            className="w-8 h-8 rounded-full bg-white/10 hover:bg-white/20 flex items-center justify-center text-white transition-colors"
          >
            <X className="w-4 h-4" />
          </button>
        </div>

        {/* Modal Body */}
        <div className="p-6 overflow-y-auto flex-1">
          {isLoading ? (
            <div className="py-12 text-center text-slate-500">
              <div className="w-8 h-8 border-3 border-indigo-600 border-t-transparent rounded-full animate-spin mx-auto mb-3" />
              <p className="text-sm font-medium">Loading practice questions...</p>
            </div>
          ) : completionResult ? (
            <div className="py-8 text-center">
              <div className="w-16 h-16 rounded-full bg-emerald-100 text-emerald-600 mx-auto mb-4 flex items-center justify-center shadow-lg shadow-emerald-100">
                <CheckCircle2 className="w-10 h-10" />
              </div>
              <h4 className="text-xl font-bold text-slate-900 mb-2">
                Concept Check Complete!
              </h4>
              <p className="text-slate-600 text-sm mb-6 max-w-xs mx-auto">
                {completionResult.message}
              </p>
              <div className="inline-flex items-center gap-2 px-4 py-2 rounded-2xl bg-amber-50 border border-amber-200 text-amber-800 font-bold text-sm mb-6">
                <Sparkles className="w-5 h-5 text-amber-500" />
                +{completionResult.xp_earned} XP Awarded
              </div>
              <div>
                <button
                  type="button"
                  onClick={onClose}
                  className="w-full py-3 rounded-xl bg-indigo-600 text-white font-bold text-sm hover:bg-indigo-700 shadow-md shadow-indigo-200 transition-all"
                >
                  Continue Learning
                </button>
              </div>
            </div>
          ) : questions.length === 0 ? (
            <div className="py-12 text-center text-slate-500">
              <p className="text-sm">No practice questions available for this topic right now.</p>
              <button
                type="button"
                onClick={onClose}
                className="mt-4 px-4 py-2 bg-slate-100 text-slate-700 rounded-xl text-xs font-semibold"
              >
                Close
              </button>
            </div>
          ) : (
            <div>
              {/* Progress indicator */}
              <div className="flex items-center justify-between text-xs text-slate-500 font-semibold mb-3">
                <span>Question {currentIndex + 1} of {questions.length}</span>
                <span className="text-indigo-600 font-bold">+10 XP upon completion</span>
              </div>
              <div className="w-full h-1.5 bg-slate-100 rounded-full overflow-hidden mb-6">
                <div 
                  className="h-full bg-indigo-600 transition-all duration-300"
                  style={{ width: `${((currentIndex + 1) / questions.length) * 100}%` }}
                />
              </div>

              {/* Question Text */}
              <p className="text-base font-semibold text-slate-900 mb-5 leading-snug">
                {currentQuestion.question_text}
              </p>

              {/* Options */}
              <div className="space-y-2.5 mb-6">
                {parsedOptions.map((opt, i) => {
                  const isSelected = selectedAnswers[currentQuestion.id] === opt;
                  return (
                    <button
                      key={i}
                      type="button"
                      onClick={() => handleSelectOption(opt)}
                      className={`w-full text-left p-3.5 rounded-xl border text-sm font-medium transition-all flex items-center justify-between ${
                        isSelected
                          ? "border-indigo-600 bg-indigo-50/70 text-indigo-950 ring-2 ring-indigo-500/20 shadow-sm"
                          : "border-slate-200 hover:border-slate-300 hover:bg-slate-50 text-slate-700"
                      }`}
                    >
                      <span className="flex items-center gap-3">
                        <span className={`w-6 h-6 rounded-lg text-xs font-bold flex items-center justify-center border ${
                          isSelected
                            ? "bg-indigo-600 text-white border-indigo-600"
                            : "bg-slate-100 text-slate-600 border-slate-200"
                        }`}>
                          {String.fromCharCode(65 + i)}
                        </span>
                        <span>{opt}</span>
                      </span>
                    </button>
                  );
                })}
              </div>

              {/* Navigation Footer */}
              <div className="flex items-center justify-between pt-4 border-t border-slate-100">
                <button
                  type="button"
                  disabled={currentIndex === 0}
                  onClick={() => setCurrentIndex(prev => prev - 1)}
                  className="px-4 py-2 text-xs font-semibold text-slate-600 hover:text-slate-900 disabled:opacity-30"
                >
                  Previous
                </button>

                {isLastQuestion ? (
                  <button
                    type="button"
                    disabled={isSubmitting || !selectedAnswers[currentQuestion.id]}
                    onClick={handleSubmit}
                    className="px-6 py-2.5 rounded-xl bg-emerald-600 hover:bg-emerald-700 text-white text-xs font-bold shadow-md shadow-emerald-200 flex items-center gap-2 disabled:opacity-50"
                  >
                    {isSubmitting ? "Submitting..." : "Complete Practice (+10 XP)"}
                  </button>
                ) : (
                  <button
                    type="button"
                    disabled={!selectedAnswers[currentQuestion.id]}
                    onClick={handleNext}
                    className="px-5 py-2.5 rounded-xl bg-indigo-600 hover:bg-indigo-700 text-white text-xs font-bold shadow-md shadow-indigo-200 flex items-center gap-2 disabled:opacity-50"
                  >
                    <span>Next</span>
                    <ChevronRight className="w-4 h-4" />
                  </button>
                )}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
