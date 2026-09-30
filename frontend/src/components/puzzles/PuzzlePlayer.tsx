"use client";

import React, { useState } from "react";
import Link from "next/link";
import { 
  Puzzle, 
  PuzzleSubmissionResult, 
  puzzleService 
} from "@/services/puzzle.service";
import { 
  CheckCircle2, 
  XCircle, 
  Sparkles, 
  HelpCircle, 
  ArrowUp, 
  ArrowDown, 
  RotateCcw,
  Zap,
  Code2,
  Check,
  ChevronRight,
  ArrowRight,
  Dna,
  Play,
  ExternalLink,
  BookOpen,
  Clock
} from "lucide-react";

interface PuzzlePlayerProps {
  puzzle: Puzzle;
  onSolved?: (result: PuzzleSubmissionResult) => void;
  isStandalonePage?: boolean;
}

export default function PuzzlePlayer({ puzzle, onSolved, isStandalonePage = false }: PuzzlePlayerProps) {
  // Parse puzzle_data if string
  let parsedData: any = puzzle.puzzle_data;
  if (typeof parsedData === "string") {
    try {
      parsedData = JSON.parse(parsedData);
    } catch {
      // keep as string
    }
  }

  // Derive specialized options / items
  const options: string[] = Array.isArray(parsedData)
    ? parsedData
    : Array.isArray(parsedData?.options)
    ? parsedData.options
    : [];

  const orderingItems: string[] = Array.isArray(parsedData)
    ? parsedData
    : Array.isArray(parsedData?.items)
    ? parsedData.items
    : [];

  const matchingPairs: Array<[string, string]> = Array.isArray(parsedData)
    ? parsedData
    : Array.isArray(parsedData?.pairs)
    ? parsedData.pairs
    : [];

  const codeSnippet: string = typeof parsedData === "string"
    ? parsedData
    : parsedData?.snippet || parsedData?.code || "";

  const placeholderText: string = parsedData?.placeholder || "Type exact keyword or value...";

  const [selectedAnswer, setSelectedAnswer] = useState<any>(() => {
    if (puzzle.puzzle_type === "ORDERING") {
      return [...orderingItems];
    }
    if (puzzle.puzzle_type === "MATCHING") {
      return {};
    }
    return "";
  });

  const [isSubmitting, setIsSubmitting] = useState(false);
  const [result, setResult] = useState<PuzzleSubmissionResult | null>(null);
  const [showHint, setShowHint] = useState(false);
  const [errorMsg, setErrorMsg] = useState<string | null>(null);
  const [startTime] = useState<number>(Date.now());

  const handleSubmit = async () => {
    setIsSubmitting(true);
    setErrorMsg(null);
    try {
      let payloadAnswer = selectedAnswer;
      if (puzzle.puzzle_type === "TRUE_FALSE" && typeof selectedAnswer === "string") {
        payloadAnswer = selectedAnswer.toLowerCase() === "true";
      }

      const elapsedSeconds = Math.max(1, Math.round((Date.now() - startTime) / 1000));
      const res = await puzzleService.submitPuzzle(puzzle.id, payloadAnswer, elapsedSeconds);
      setResult(res);
      if (res.is_correct && onSolved) {
        onSolved(res);
      }
    } catch (err: any) {
      setErrorMsg(err.message || "Failed to submit challenge answer.");
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleReset = () => {
    setResult(null);
    setShowHint(false);
    setErrorMsg(null);
    if (puzzle.puzzle_type === "ORDERING") {
      setSelectedAnswer([...orderingItems]);
    } else if (puzzle.puzzle_type === "MATCHING") {
      setSelectedAnswer({});
    } else {
      setSelectedAnswer("");
    }
  };

  const moveOrderingItem = (index: number, direction: "up" | "down") => {
    const list = [...(selectedAnswer as string[])];
    const targetIdx = direction === "up" ? index - 1 : index + 1;
    if (targetIdx < 0 || targetIdx >= list.length) return;
    const temp = list[index];
    list[index] = list[targetIdx];
    list[targetIdx] = temp;
    setSelectedAnswer(list);
  };

  const handleMatchingChange = (leftKey: string, rightVal: string) => {
    setSelectedAnswer((prev: any) => ({
      ...prev,
      [leftKey]: rightVal,
    }));
  };

  // State styling helper for Knowledge DNA badge
  const getStateColor = (state?: string | null) => {
    switch (state) {
      case "MASTERED":
        return "bg-emerald-500/20 text-emerald-300 border-emerald-500/40";
      case "DEVELOPING":
        return "bg-amber-500/20 text-amber-300 border-amber-500/40";
      case "WEAK":
        return "bg-rose-500/20 text-rose-300 border-rose-500/40";
      default:
        return "bg-slate-800 text-slate-300 border-slate-700";
    }
  };

  return (
    <div className="rounded-3xl border border-white/10 bg-[#0B1124]/90 backdrop-blur-2xl shadow-[0_8px_32px_0_rgba(0,0,0,0.45)] overflow-hidden transition-all">
      {/* Challenge Card Header */}
      <div className="p-6 border-b border-white/[0.08] bg-white/[0.02] flex flex-wrap items-center justify-between gap-4">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-2xl bg-cyan-500/15 border border-cyan-500/30 flex items-center justify-center text-cyan-400 shadow-[0_0_15px_rgba(6,182,212,0.2)]">
            <Zap className="w-5 h-5" />
          </div>
          <div>
            <span className="text-[10px] font-extrabold uppercase tracking-widest text-cyan-300 block">
              {puzzle.puzzle_type.replace(/_/g, " ")}
            </span>
            <h3 className="text-base font-bold text-white">
              {puzzle.title}
            </h3>
          </div>
        </div>

        <div className="flex items-center gap-2">
          <span className="inline-flex items-center gap-1 text-xs font-bold px-3 py-1 rounded-full bg-amber-500/15 text-amber-300 border border-amber-500/30 font-mono">
            <Sparkles className="w-3.5 h-3.5 text-amber-400" />
            +{puzzle.xp_reward || 15} XP
          </span>
          <span className={`text-[10px] font-extrabold uppercase px-3 py-1 rounded-full border ${
            puzzle.difficulty === "HARD"
              ? "bg-rose-500/15 text-rose-300 border-rose-500/30"
              : puzzle.difficulty === "MEDIUM"
              ? "bg-amber-500/15 text-amber-300 border-amber-500/30"
              : "bg-emerald-500/15 text-emerald-300 border-emerald-500/30"
          }`}>
            {puzzle.difficulty}
          </span>
          {puzzle.estimated_time && (
            <span className="hidden sm:inline-flex items-center gap-1 text-xs text-slate-400 bg-white/[0.05] px-2.5 py-1 rounded-full font-medium border border-white/5">
              <Clock className="w-3 h-3 text-slate-400" />
              {puzzle.estimated_time}
            </span>
          )}
        </div>
      </div>

      {/* Main Content Area */}
      <div className="p-6 sm:p-8">
        {puzzle.instructions && (
          <p className="text-xs font-bold text-cyan-400/90 mb-3 uppercase tracking-wider">
            {puzzle.instructions}
          </p>
        )}

        {/* Question Prompt */}
        <div className="mb-6">
          <h4 className="text-white font-bold text-base sm:text-lg leading-relaxed">
            {puzzle.question}
          </h4>
          {puzzle.description && puzzle.description !== puzzle.title && (
            <p className="text-xs text-slate-400 mt-1.5 leading-normal">
              {puzzle.description}
            </p>
          )}
        </div>

        {/* 1. MULTIPLE CHOICE */}
        {puzzle.puzzle_type === "MULTIPLE_CHOICE" && options.length > 0 && (
          <div className="space-y-3 mb-6">
            {options.map((opt: string, i: number) => {
              const isSelected = selectedAnswer === opt;
              return (
                <button
                  key={i}
                  type="button"
                  disabled={result?.is_correct}
                  onClick={() => setSelectedAnswer(opt)}
                  className={`w-full text-left p-4 rounded-2xl border text-sm font-medium transition-all flex items-center justify-between ${
                    isSelected
                      ? "border-cyan-400 bg-cyan-950/30 text-white ring-2 ring-cyan-500/20 shadow-[0_0_20px_rgba(6,182,212,0.2)]"
                      : "border-white/[0.08] hover:border-white/20 hover:bg-white/[0.04] text-slate-300 bg-[#090E20]/90"
                  }`}
                >
                  <span className="flex items-center gap-3.5">
                    <span className={`w-7 h-7 rounded-xl text-xs font-bold flex items-center justify-center border transition-colors ${
                      isSelected
                        ? "bg-cyan-500 text-black border-cyan-500 shadow-[0_0_10px_#22d3ee]"
                        : "bg-slate-800 text-slate-400 border-slate-700"
                    }`}>
                      {String.fromCharCode(65 + i)}
                    </span>
                    <span className="leading-relaxed">{opt}</span>
                  </span>
                  {isSelected && <Check className="w-5 h-5 text-cyan-400 shrink-0 ml-2" />}
                </button>
              );
            })}
          </div>
        )}

        {/* 2. TRUE / FALSE */}
        {puzzle.puzzle_type === "TRUE_FALSE" && (
          <div className="grid grid-cols-2 gap-4 mb-6">
            {["true", "false"].map((val) => {
              const isTrue = val === "true";
              const isSelected = selectedAnswer === val || selectedAnswer === isTrue;
              return (
                <button
                  key={val}
                  type="button"
                  disabled={result?.is_correct}
                  onClick={() => setSelectedAnswer(val)}
                  className={`py-5 px-6 rounded-2xl border-2 font-bold text-base transition-all flex items-center justify-center gap-2 shadow-sm ${
                    isSelected
                      ? isTrue
                        ? "border-emerald-500 bg-emerald-950/30 text-emerald-300 ring-2 ring-emerald-400/20 shadow-[0_0_20px_rgba(16,185,129,0.3)]"
                        : "border-rose-500 bg-rose-950/30 text-rose-300 ring-2 ring-rose-400/20 shadow-[0_0_20px_rgba(244,63,94,0.3)]"
                      : "border-white/[0.08] hover:border-white/20 text-slate-300 bg-[#090E20]/90 hover:bg-white/[0.04]"
                  }`}
                >
                  {isTrue ? "True ✓" : "False ✗"}
                </button>
              );
            })}
          </div>
        )}

        {/* 3. ORDERING / SEQUENCE */}
        {puzzle.puzzle_type === "ORDERING" && Array.isArray(selectedAnswer) && (
          <div className="space-y-3 mb-6">
            <span className="text-xs text-slate-400 block mb-2 font-medium">
              Use the arrows to arrange in correct execution or logical order:
            </span>
            {selectedAnswer.map((item: string, idx: number) => (
              <div
                key={idx}
                className="flex items-center justify-between p-3.5 rounded-2xl border border-white/[0.08] bg-[#090E20]/90 text-sm font-semibold text-slate-200 transition-all hover:border-cyan-500/30"
              >
                <div className="flex items-center gap-3">
                  <span className="w-7 h-7 rounded-xl bg-slate-800 text-cyan-300 border border-white/10 font-bold text-xs flex items-center justify-center font-mono">
                    {idx + 1}
                  </span>
                  <span>{item}</span>
                </div>

                <div className="flex items-center gap-1">
                  <button
                    type="button"
                    disabled={idx === 0 || result?.is_correct}
                    onClick={() => moveOrderingItem(idx, "up")}
                    className="p-1.5 rounded-lg border border-white/10 hover:bg-white/10 text-slate-400 hover:text-white disabled:opacity-30 disabled:cursor-not-allowed transition"
                    title="Move Up"
                  >
                    <ArrowUp className="w-4 h-4" />
                  </button>
                  <button
                    type="button"
                    disabled={idx === selectedAnswer.length - 1 || result?.is_correct}
                    onClick={() => moveOrderingItem(idx, "down")}
                    className="p-1.5 rounded-lg border border-white/10 hover:bg-white/10 text-slate-400 hover:text-white disabled:opacity-30 disabled:cursor-not-allowed transition"
                    title="Move Down"
                  >
                    <ArrowDown className="w-4 h-4" />
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}

        {/* 4. CODE / SQL OUTPUT */}
        {puzzle.puzzle_type === "CODE_OUTPUT" && (
          <div className="space-y-4 mb-6">
            {codeSnippet && (
              <div className="rounded-2xl border border-white/10 bg-[#050811] p-4 text-xs font-mono text-cyan-300 shadow-inner overflow-x-auto">
                <div className="flex items-center gap-2 mb-2 pb-2 border-b border-white/10 text-slate-500">
                  <Code2 className="w-4 h-4 text-cyan-400" />
                  <span className="text-[10px] uppercase font-bold tracking-wider">Executable Snippet</span>
                </div>
                <pre className="whitespace-pre-wrap leading-relaxed">{codeSnippet}</pre>
              </div>
            )}

            {options.length > 0 ? (
              <div className="space-y-2">
                <span className="text-xs text-slate-400 block font-medium">Select the correct output:</span>
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                  {options.map((opt: string, i: number) => {
                    const isSelected = selectedAnswer === opt;
                    return (
                      <button
                        key={i}
                        type="button"
                        disabled={result?.is_correct}
                        onClick={() => setSelectedAnswer(opt)}
                        className={`p-3.5 rounded-2xl border text-xs font-mono text-left transition-all ${
                          isSelected
                            ? "border-cyan-400 bg-cyan-950/30 text-cyan-300 shadow-[0_0_15px_rgba(6,182,212,0.25)]"
                            : "border-white/[0.08] bg-[#090E20]/90 text-slate-300 hover:border-white/20"
                        }`}
                      >
                        {opt}
                      </button>
                    );
                  })}
                </div>
              </div>
            ) : (
              <div className="space-y-2">
                <span className="text-xs text-slate-400 block font-medium">Type the exact output:</span>
                <input
                  type="text"
                  disabled={result?.is_correct}
                  value={selectedAnswer}
                  onChange={(e) => setSelectedAnswer(e.target.value)}
                  placeholder={placeholderText}
                  className="w-full p-3.5 rounded-2xl border border-white/10 bg-[#090E20] text-sm text-white font-mono placeholder:text-slate-500 focus:outline-none focus:border-cyan-400 focus:ring-2 focus:ring-cyan-500/20"
                />
              </div>
            )}
          </div>
        )}

        {/* 5. FILL IN THE BLANK */}
        {puzzle.puzzle_type === "FILL_BLANK" && (
          <div className="space-y-3 mb-6">
            <span className="text-xs text-slate-400 block font-medium">Provide the missing term or symbol:</span>
            <input
              type="text"
              disabled={result?.is_correct}
              value={selectedAnswer}
              onChange={(e) => setSelectedAnswer(e.target.value)}
              placeholder={placeholderText}
              className="w-full p-4 rounded-2xl border border-white/10 bg-[#090E20] text-sm text-white font-semibold placeholder:text-slate-500 focus:outline-none focus:border-cyan-400 focus:ring-2 focus:ring-cyan-500/20"
            />
          </div>
        )}

        {/* 6. CONCEPT MATCHING */}
        {puzzle.puzzle_type === "MATCHING" && (
          <div className="space-y-3 mb-6">
            <span className="text-xs text-slate-400 block font-medium">Pair each concept on the left with its corresponding property:</span>
            {matchingPairs.length > 0 && (
              matchingPairs.map(([left, right], idx) => {
                const uniqueOptions = Array.from(new Set(matchingPairs.map((p) => p[1])));
                return (
                  <div
                    key={idx}
                    className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 p-3.5 rounded-2xl border border-white/[0.08] bg-[#090E20]/90"
                  >
                    <span className="text-xs font-bold text-slate-200">{left}</span>
                    <select
                      disabled={result?.is_correct}
                      value={selectedAnswer[left] || ""}
                      onChange={(e) => handleMatchingChange(left, e.target.value)}
                      className="p-2 rounded-xl border border-white/10 bg-[#050811] text-xs text-white focus:outline-none focus:border-cyan-400"
                    >
                      <option value="">Select matching term...</option>
                      {uniqueOptions.map((opt, optIdx) => (
                        <option key={optIdx} value={opt}>
                          {opt}
                        </option>
                      ))}
                    </select>
                  </div>
                );
              })
            )}
          </div>
        )}

        {/* ============================================================== */}
        {/* SUBMISSION FEEDBACK & KNOWLEDGE DNA INTELLIGENCE CARD */}
        {/* ============================================================== */}
        {result && (
          <div className={`p-5 sm:p-6 rounded-3xl mb-6 transition-all border backdrop-blur-xl ${
            result.is_correct
              ? "bg-emerald-950/20 border-emerald-500/30 text-emerald-200 shadow-[0_0_30px_rgba(16,185,129,0.15)]"
              : "bg-rose-950/20 border-rose-500/30 text-rose-200 shadow-[0_0_30px_rgba(244,63,94,0.15)]"
          }`}>
            <div className="flex items-start gap-4">
              {result.is_correct ? (
                <div className="w-10 h-10 rounded-2xl bg-emerald-500 text-black flex items-center justify-center shrink-0 shadow-[0_0_15px_#10b981]">
                  <CheckCircle2 className="w-6 h-6" />
                </div>
              ) : (
                <div className="w-10 h-10 rounded-2xl bg-rose-500 text-white flex items-center justify-center shrink-0 shadow-[0_0_15px_#f43f5e]">
                  <XCircle className="w-6 h-6" />
                </div>
              )}

              <div className="flex-1 space-y-3">
                <div className="flex flex-wrap items-center justify-between gap-2">
                  <h4 className="font-extrabold text-base sm:text-lg text-white">
                    {result.is_correct ? "✓ Correct! Challenge Solved" : "Not quite right yet"}
                  </h4>
                  {result.xp_earned > 0 && (
                    <span className="inline-flex items-center gap-1 font-extrabold text-xs bg-emerald-500 text-black px-3 py-1 rounded-full shadow-[0_0_10px_#10b981]">
                      <Sparkles className="w-3.5 h-3.5" /> +{result.xp_earned} XP Earned
                    </span>
                  )}
                </div>

                {/* What SPECTRA learned about you */}
                {result.spectra_feedback && (
                  <div className="p-3.5 rounded-2xl bg-white/[0.04] border border-white/10 text-xs sm:text-sm text-slate-200 leading-relaxed shadow-sm">
                    <span className="font-bold text-cyan-300 block mb-0.5">
                      What SPECTRA learned about you:
                    </span>
                    {result.spectra_feedback}
                  </div>
                )}

                {/* Knowledge DNA live update banner */}
                {result.topic_name && result.mastery_after !== null && result.mastery_after !== undefined && (
                  <div className="p-3.5 rounded-2xl bg-[#090E20] border border-white/10 text-white flex flex-wrap items-center justify-between gap-3 shadow-md">
                    <div className="flex items-center gap-2.5">
                      <div className="w-7 h-7 rounded-xl bg-gradient-to-br from-cyan-400 to-indigo-500 flex items-center justify-center text-white">
                        <Dna className="w-4 h-4" />
                      </div>
                      <div>
                        <span className="text-[10px] uppercase font-bold tracking-widest text-cyan-300 block">
                          Knowledge DNA Recalculated
                        </span>
                        <span className="text-xs font-bold text-white">
                          {result.topic_name}
                        </span>
                      </div>
                    </div>

                    <div className="flex items-center gap-2 text-xs font-mono font-bold">
                      <span className={`px-2 py-0.5 rounded-lg border text-[11px] ${getStateColor(result.mastery_state_before)}`}>
                        {result.mastery_before ?? 0}%
                      </span>
                      <span className="text-slate-400">&rarr;</span>
                      <span className={`px-2 py-0.5 rounded-lg border text-[11px] font-bold ${getStateColor(result.mastery_state_after)}`}>
                        {result.mastery_after}%
                      </span>
                    </div>
                  </div>
                )}

                {/* Detailed Concept Explanation */}
                {result.explanation && (
                  <p className="text-xs text-slate-300 bg-white/[0.03] p-3 rounded-xl border border-white/10 leading-relaxed">
                    <span className="font-bold text-white">Why this works: </span>
                    {result.explanation}
                  </p>
                )}

                {/* Optional Hint on Incorrect */}
                {!result.is_correct && result.hint && showHint && (
                  <div className="text-xs text-amber-300 bg-amber-950/30 p-3 rounded-xl border border-amber-500/30">
                    <span className="font-bold">Guided Hint: </span>
                    {result.hint}
                  </div>
                )}

                {/* Curated YouTube Video Remediation if Struggling */}
                {result.recommended_video && !result.is_correct && (
                  <div className="p-4 rounded-2xl bg-rose-950/30 border border-rose-500/30 space-y-3">
                    <div className="flex items-center gap-2 text-xs font-bold text-rose-300">
                      <Play className="w-4 h-4 fill-rose-500 text-rose-500" />
                      <span>Recommended Concept Explanation</span>
                    </div>
                    <div className="flex flex-col sm:flex-row items-center gap-3 bg-[#0B1124] p-3 rounded-xl border border-white/10">
                      {result.recommended_video.thumbnail_url && (
                        <img
                          src={result.recommended_video.thumbnail_url}
                          alt={result.recommended_video.title}
                          className="w-full sm:w-28 aspect-video object-cover rounded-lg"
                        />
                      )}
                      <div className="flex-1 space-y-1">
                        <h5 className="text-xs font-bold text-white line-clamp-1">
                          {result.recommended_video.title}
                        </h5>
                        <p className="text-[11px] text-slate-400">
                          {result.recommended_video.channel_name} &bull; YouTube Walkthrough
                        </p>
                        <a
                          href={result.recommended_video.url}
                          target="_blank"
                          rel="noreferrer"
                          className="inline-flex items-center gap-1.5 text-xs font-bold text-cyan-400 hover:text-cyan-300 pt-1"
                        >
                          <span>Watch Explanation</span>
                          <ExternalLink className="w-3.5 h-3.5" />
                        </a>
                      </div>
                    </div>
                  </div>
                )}

                {/* Action Buttons for Next Steps */}
                <div className="flex flex-wrap items-center gap-3 pt-2">
                  <Link
                    href="/student/knowledge-dna"
                    className="px-4 py-2 rounded-xl border border-cyan-500/30 hover:bg-cyan-500/10 text-cyan-300 text-xs font-bold transition-colors flex items-center gap-1.5"
                  >
                    <Dna className="w-3.5 h-3.5" />
                    <span>View in Knowledge DNA</span>
                  </Link>

                  {result.next_puzzle_id && (
                    <Link
                      href={`/student/puzzles/${result.next_puzzle_id}`}
                      className="px-4 py-2 rounded-xl bg-gradient-to-r from-purple-600 to-indigo-600 hover:from-purple-500 hover:to-indigo-500 text-white text-xs font-bold transition-all shadow-[0_0_15px_rgba(139,92,246,0.3)] flex items-center gap-1.5"
                    >
                      <span>Next Challenge</span>
                      <ArrowRight className="w-3.5 h-3.5" />
                    </Link>
                  )}

                  {result.next_lesson_id && (
                    <Link
                      href={`/student/lessons/${result.next_lesson_id}`}
                      className="px-4 py-2 rounded-xl bg-gradient-to-r from-emerald-600 to-teal-600 hover:from-emerald-500 hover:to-teal-500 text-white text-xs font-bold transition-all shadow-[0_0_15px_rgba(16,185,129,0.3)] flex items-center gap-1.5"
                    >
                      <BookOpen className="w-3.5 h-3.5" />
                      <span>Continue to Next Lesson</span>
                    </Link>
                  )}
                </div>
              </div>
            </div>
          </div>
        )}

        {errorMsg && (
          <div className="p-3.5 rounded-2xl bg-rose-950/30 border border-rose-500/30 text-rose-300 text-xs mb-4">
            {errorMsg}
          </div>
        )}

        {/* Footer Actions */}
        <div className="flex items-center justify-between pt-4 border-t border-white/[0.08]">
          <div>
            {!result?.is_correct && (
              <button
                type="button"
                onClick={() => setShowHint(!showHint)}
                className="inline-flex items-center gap-1.5 text-xs font-semibold text-slate-400 hover:text-cyan-300 transition-colors"
              >
                <HelpCircle className="w-4 h-4" />
                {showHint ? "Hide Hint" : "Need a Hint?"}
              </button>
            )}
          </div>

          <div className="flex items-center gap-2.5">
            {result && !result.is_correct && (
              <button
                type="button"
                onClick={handleReset}
                className="px-4 py-2.5 text-xs font-bold text-slate-300 bg-white/[0.05] hover:bg-white/10 rounded-2xl border border-white/10 transition-colors flex items-center gap-1.5"
              >
                <RotateCcw className="w-3.5 h-3.5" />
                <span>Try Again</span>
              </button>
            )}

            {!result?.is_correct && (
              <button
                type="button"
                disabled={isSubmitting || !selectedAnswer || (Array.isArray(selectedAnswer) && selectedAnswer.length === 0)}
                onClick={handleSubmit}
                className="px-6 py-3 rounded-2xl font-black text-xs sm:text-sm text-black bg-gradient-to-r from-cyan-500 to-indigo-600 hover:from-cyan-400 hover:to-indigo-500 disabled:opacity-50 disabled:cursor-not-allowed shadow-[0_0_20px_rgba(6,182,212,0.4)] transition-all flex items-center gap-2 hover:scale-[1.02] active:scale-[0.98]"
              >
                {isSubmitting ? (
                  "Verifying..."
                ) : (
                  <>
                    <span>Check Answer</span>
                    <ChevronRight className="w-4 h-4" />
                  </>
                )}
              </button>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
