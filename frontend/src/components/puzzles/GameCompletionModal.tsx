"use client";

import React, { useEffect } from "react";
import Link from "next/link";
import { Sparkles, Trophy, RotateCcw, ArrowLeft, Clock, Zap, CheckCircle2 } from "lucide-react";
import { getRandomRelaxationQuote } from "@/lib/puzzleLab";

interface GameCompletionModalProps {
  isOpen: boolean;
  gameTitle: string;
  score: number;
  timeSeconds: number;
  moves?: number;
  isNewBest?: boolean;
  xpAwarded?: number;
  onPlayAgain: () => void;
  customStats?: Array<{ label: string; value: string | number }>;
}

export default function GameCompletionModal({
  isOpen,
  gameTitle,
  score,
  timeSeconds,
  moves,
  isNewBest = false,
  xpAwarded = 20,
  onPlayAgain,
  customStats,
}: GameCompletionModalProps) {
  const [quote, setQuote] = React.useState("");

  useEffect(() => {
    if (isOpen) {
      setQuote(getRandomRelaxationQuote());
    }
  }, [isOpen]);

  if (!isOpen) return null;

  const formatTime = (secs: number) => {
    const m = Math.floor(secs / 60);
    const s = secs % 60;
    return `${m.toString().padStart(2, "0")}:${s.toString().padStart(2, "0")}`;
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 dark:bg-black/80 backdrop-blur-md animate-in fade-in duration-300">
      <div className="relative w-full max-w-md rounded-3xl bg-white dark:bg-[#0B1124] border border-cyan-500/40 p-6 sm:p-8 shadow-2xl dark:shadow-[0_0_50px_rgba(6,182,212,0.25)] text-center overflow-hidden">
        {/* Ambient Top Glow */}
        <div className="absolute -top-24 left-1/2 -translate-x-1/2 w-64 h-32 bg-gradient-to-b from-cyan-500/20 dark:from-cyan-500/30 to-purple-500/10 dark:to-purple-500/20 blur-3xl rounded-full pointer-events-none" />

        {/* Header Icon */}
        <div className="relative mx-auto w-16 h-16 rounded-2xl bg-gradient-to-tr from-cyan-500 to-purple-600 flex items-center justify-center text-white shadow-[0_0_25px_rgba(6,182,212,0.5)] mb-4 animate-bounce">
          <Sparkles className="w-8 h-8" />
        </div>

        {/* Title */}
        <div className="space-y-1 mb-4">
          <span className="text-xs font-black tracking-widest text-cyan-600 dark:text-cyan-400 uppercase">
            ✨ Well Played ✨
          </span>
          <h2 className="text-2xl font-black text-slate-900 dark:text-white tracking-tight">{gameTitle}</h2>
          {isNewBest && (
            <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-amber-500/15 dark:bg-amber-500/20 border border-amber-500/40 text-amber-700 dark:text-amber-300 text-xs font-bold mt-1">
              <Trophy className="w-3.5 h-3.5 text-amber-500 dark:text-amber-400" />
              New Personal Best!
            </div>
          )}
        </div>

        {/* Big Score Display */}
        <div className="my-5 p-4 rounded-2xl bg-slate-100/80 dark:bg-[#070A14]/80 border border-slate-200 dark:border-white/[0.08]">
          <span className="text-[11px] font-extrabold text-slate-500 dark:text-slate-400 uppercase tracking-widest block">
            Final Score
          </span>
          <span className="text-4xl sm:text-5xl font-black text-transparent bg-clip-text bg-gradient-to-r from-cyan-600 via-sky-600 to-purple-600 dark:from-cyan-400 dark:via-sky-300 dark:to-purple-400 font-mono">
            {score}
          </span>
          <span className="text-xs text-slate-500 dark:text-slate-400 block mt-1">Points</span>
        </div>

        {/* Detailed Metrics */}
        <div className="grid grid-cols-2 gap-3 mb-6">
          <div className="p-3 rounded-xl bg-slate-50 dark:bg-white/[0.03] border border-slate-200/80 dark:border-white/[0.06] flex items-center gap-3">
            <div className="w-8 h-8 rounded-lg bg-cyan-500/10 flex items-center justify-center text-cyan-600 dark:text-cyan-400 shrink-0">
              <Clock className="w-4 h-4" />
            </div>
            <div className="text-left">
              <span className="text-[10px] font-bold text-slate-500 dark:text-slate-400 uppercase block">Time</span>
              <span className="text-sm font-black text-slate-900 dark:text-white font-mono">{formatTime(timeSeconds)}</span>
            </div>
          </div>

          {moves !== undefined ? (
            <div className="p-3 rounded-xl bg-slate-50 dark:bg-white/[0.03] border border-slate-200/80 dark:border-white/[0.06] flex items-center gap-3">
              <div className="w-8 h-8 rounded-lg bg-purple-500/10 flex items-center justify-center text-purple-600 dark:text-purple-400 shrink-0">
                <Zap className="w-4 h-4" />
              </div>
              <div className="text-left">
                <span className="text-[10px] font-bold text-slate-500 dark:text-slate-400 uppercase block">Moves</span>
                <span className="text-sm font-black text-slate-900 dark:text-white font-mono">{moves}</span>
              </div>
            </div>
          ) : customStats && customStats.length > 0 ? (
            <div className="p-3 rounded-xl bg-slate-50 dark:bg-white/[0.03] border border-slate-200/80 dark:border-white/[0.06] flex items-center gap-3">
              <div className="w-8 h-8 rounded-lg bg-emerald-500/10 flex items-center justify-center text-emerald-600 dark:text-emerald-400 shrink-0">
                <CheckCircle2 className="w-4 h-4" />
              </div>
              <div className="text-left">
                <span className="text-[10px] font-bold text-slate-500 dark:text-slate-400 uppercase block">{customStats[0].label}</span>
                <span className="text-sm font-black text-slate-900 dark:text-white font-mono">{customStats[0].value}</span>
              </div>
            </div>
          ) : (
            <div className="p-3 rounded-xl bg-slate-50 dark:bg-white/[0.03] border border-slate-200/80 dark:border-white/[0.06] flex items-center gap-3">
              <div className="w-8 h-8 rounded-lg bg-emerald-500/10 flex items-center justify-center text-emerald-600 dark:text-emerald-400 shrink-0">
                <CheckCircle2 className="w-4 h-4" />
              </div>
              <div className="text-left">
                <span className="text-[10px] font-bold text-slate-500 dark:text-slate-400 uppercase block">Reward</span>
                <span className="text-sm font-black text-emerald-600 dark:text-emerald-400 font-mono">+{xpAwarded} XP</span>
              </div>
            </div>
          )}
        </div>

        {/* Relaxation Quote */}
        <p className="text-xs text-slate-600 dark:text-slate-400 italic mb-6 px-2">
          &ldquo;{quote}&rdquo;
        </p>

        {/* Action Buttons */}
        <div className="flex flex-col sm:flex-row items-center gap-3">
          <button
            onClick={onPlayAgain}
            className="w-full sm:flex-1 py-3 px-4 rounded-xl bg-gradient-to-r from-cyan-500 to-sky-500 hover:from-cyan-400 hover:to-sky-400 text-black font-extrabold text-sm flex items-center justify-center gap-2 shadow-md transition-all"
          >
            <RotateCcw className="w-4 h-4" />
            Play Again
          </button>

          <Link
            href="/student/puzzles"
            className="w-full sm:flex-1 py-3 px-4 rounded-xl bg-slate-100 hover:bg-slate-200 dark:bg-[#0F172E] dark:hover:bg-[#1C2950] border border-slate-300 dark:border-white/10 text-slate-800 dark:text-white font-bold text-sm flex items-center justify-center gap-2 transition-all"
          >
            <ArrowLeft className="w-4 h-4" />
            Back to Lab
          </Link>
        </div>
      </div>
    </div>
  );
}
