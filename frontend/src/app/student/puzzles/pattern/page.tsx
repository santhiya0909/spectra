"use client";

import React, { useState, useEffect, useRef } from "react";
import Link from "next/link";
import { RoleLayout } from "@/components/layout/RoleLayout";
import { GlassCard } from "@/components/common/GlassCard";
import GameCompletionModal from "@/components/puzzles/GameCompletionModal";
import { recordGameCompletion, getPuzzleLabStats } from "@/lib/puzzleLab";
import {
  ArrowLeft,
  RotateCcw,
  Clock,
  Zap,
  CheckCircle2,
  Sparkles,
  Trophy,
  Flame,
  Circle,
  Square,
  Triangle,
  Hexagon,
  ArrowUp,
  ArrowRight,
  ArrowDown,
  ArrowLeft as ArrowLeftIcon,
  HelpCircle
} from "lucide-react";

interface PatternPuzzle {
  id: number;
  category: "Visual" | "Numerical" | "Rotation" | "Logic";
  prompt: string;
  sequence: Array<{ type: "text" | "shape"; value: string; color?: string }>;
  options: Array<{ value: string; label: string; isCorrect: boolean }>;
  explanation: string;
}

const PUZZLE_BANK: PatternPuzzle[] = [
  {
    id: 1,
    category: "Visual",
    prompt: "Identify the alternating color cycle",
    sequence: [
      { type: "text", value: "🔵", color: "text-cyan-400" },
      { type: "text", value: "🟣", color: "text-purple-400" },
      { type: "text", value: "🔵", color: "text-cyan-400" },
      { type: "text", value: "🟣", color: "text-purple-400" },
      { type: "text", value: "🔵", color: "text-cyan-400" },
    ],
    options: [
      { value: "🟣", label: "Violet Sphere", isCorrect: true },
      { value: "🔵", label: "Cyan Sphere", isCorrect: false },
      { value: "🟢", label: "Emerald Sphere", isCorrect: false },
      { value: "🟡", label: "Amber Sphere", isCorrect: false },
    ],
    explanation: "The sequence alternates strictly between Cyan 🔵 and Violet 🟣.",
  },
  {
    id: 2,
    category: "Numerical",
    prompt: "Binary exponential expansion",
    sequence: [
      { type: "text", value: "2" },
      { type: "text", value: "4" },
      { type: "text", value: "8" },
      { type: "text", value: "16" },
      { type: "text", value: "32" },
    ],
    options: [
      { value: "64", label: "2⁶ = 64", isCorrect: true },
      { value: "48", label: "48", isCorrect: false },
      { value: "54", label: "54", isCorrect: false },
      { value: "128", label: "128", isCorrect: false },
    ],
    explanation: "Each number doubles (×2) to produce the next power of two.",
  },
  {
    id: 3,
    category: "Rotation",
    prompt: "Clockwise 90° orbital rotation",
    sequence: [
      { type: "text", value: "⬆️" },
      { type: "text", value: "➡️" },
      { type: "text", value: "⬇️" },
      { type: "text", value: "⬅️" },
      { type: "text", value: "⬆️" },
    ],
    options: [
      { value: "➡️", label: "East (Right)", isCorrect: true },
      { value: "⬇️", label: "South (Down)", isCorrect: false },
      { value: "⬅️", label: "West (Left)", isCorrect: false },
      { value: "↖️", label: "North-West", isCorrect: false },
    ],
    explanation: "The vector rotates 90 degrees clockwise at each step.",
  },
  {
    id: 4,
    category: "Numerical",
    prompt: "Fibonacci series summation",
    sequence: [
      { type: "text", value: "1" },
      { type: "text", value: "1" },
      { type: "text", value: "2" },
      { type: "text", value: "3" },
      { type: "text", value: "5" },
      { type: "text", value: "8" },
    ],
    options: [
      { value: "13", label: "5 + 8 = 13", isCorrect: true },
      { value: "11", label: "11", isCorrect: false },
      { value: "15", label: "15", isCorrect: false },
      { value: "16", label: "16", isCorrect: false },
    ],
    explanation: "Each step equals the sum of the two previous terms (5 + 8 = 13).",
  },
  {
    id: 5,
    category: "Visual",
    prompt: "Geometric polygon vertex progression",
    sequence: [
      { type: "text", value: "▲ (3)", color: "text-emerald-400" },
      { type: "text", value: "■ (4)", color: "text-cyan-400" },
      { type: "text", value: "⬟ (5)", color: "text-purple-400" },
      { type: "text", value: "⬡ (6)", color: "text-amber-400" },
    ],
    options: [
      { value: "⯃ (7)", label: "Heptagon (7)", isCorrect: true },
      { value: "● (1)", label: "Circle (1)", isCorrect: false },
      { value: "▲ (3)", label: "Triangle (3)", isCorrect: false },
      { value: "■ (4)", label: "Square (4)", isCorrect: false },
    ],
    explanation: "Number of vertices increments by +1: Triangle (3) -> Square (4) -> Pentagon (5) -> Hexagon (6) -> Heptagon (7).",
  },
];

export default function PatternShiftPage() {
  const [currentIndex, setCurrentIndex] = useState(0);
  const [selectedAnswer, setSelectedAnswer] = useState<string | null>(null);
  const [isAnswerCorrect, setIsAnswerCorrect] = useState<boolean | null>(null);
  const [score, setScore] = useState(0);
  const [streak, setStreak] = useState(0);
  const [maxStreak, setMaxStreak] = useState(0);
  const [seconds, setSeconds] = useState(0);
  const [isCompleted, setIsCompleted] = useState(false);
  const [isNewBest, setIsNewBest] = useState(false);
  const [bestStats, setBestStats] = useState({ bestScore: 0, bestTime: 0 });

  const timerRef = useRef<NodeJS.Timeout | null>(null);

  const currentPuzzle = PUZZLE_BANK[currentIndex];

  const initGame = () => {
    setCurrentIndex(0);
    setSelectedAnswer(null);
    setIsAnswerCorrect(null);
    setScore(0);
    setStreak(0);
    setMaxStreak(0);
    setSeconds(0);
    setIsCompleted(false);

    if (timerRef.current) clearInterval(timerRef.current);
    timerRef.current = setInterval(() => {
      setSeconds((prev) => prev + 1);
    }, 1000);
  };

  useEffect(() => {
    const stats = getPuzzleLabStats();
    if (stats.games.pattern) {
      setBestStats({
        bestScore: stats.games.pattern.bestScore,
        bestTime: stats.games.pattern.bestTime,
      });
    }
    initGame();

    return () => {
      if (timerRef.current) clearInterval(timerRef.current);
    };
  }, []);

  const handleOptionSelect = (option: { value: string; label: string; isCorrect: boolean }) => {
    if (selectedAnswer !== null) return; // Prevent double tap

    setSelectedAnswer(option.value);
    const correct = option.isCorrect;
    setIsAnswerCorrect(correct);

    if (correct) {
      const comboMultiplier = 1 + streak * 0.25;
      const points = Math.round(180 * comboMultiplier);
      setScore((s) => s + points);
      setStreak((st) => {
        const next = st + 1;
        setMaxStreak((m) => Math.max(m, next));
        return next;
      });
    } else {
      // Gentle penalty: reset streak, but still award some engagement points
      setScore((s) => s + 40);
      setStreak(0);
    }

    // Advance to next pattern after gentle feedback delay
    setTimeout(() => {
      if (currentIndex + 1 < PUZZLE_BANK.length) {
        setCurrentIndex((i) => i + 1);
        setSelectedAnswer(null);
        setIsAnswerCorrect(null);
      } else {
        handleGameComplete();
      }
    }, 900);
  };

  const handleGameComplete = () => {
    if (timerRef.current) clearInterval(timerRef.current);

    const finalScore = score + (streak * 50);
    const { isNewBest: newBestRecord } = recordGameCompletion("pattern", finalScore, seconds);
    setIsNewBest(newBestRecord);
    setIsCompleted(true);
  };

  const formatTime = (secs: number) => {
    const m = Math.floor(secs / 60);
    const s = secs % 60;
    return `${m.toString().padStart(2, "0")}:${s.toString().padStart(2, "0")}`;
  };

  return (
    <RoleLayout allowedRoles={["STUDENT", "ADMIN", "TEACHER"]}>
      <div className="max-w-4xl mx-auto space-y-6 pb-16">
        {/* Navigation / Header */}
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-4 border-b border-white/[0.08]">
          <div className="flex items-center gap-3">
            <Link
              href="/student/puzzles"
              className="p-2.5 rounded-2xl bg-[#0B1124] border border-white/10 hover:border-cyan-500/40 text-slate-300 hover:text-white transition-colors shadow-sm"
              title="Return to Puzzle Lab"
            >
              <ArrowLeft className="w-5 h-5" />
            </Link>
            <div>
              <div className="flex items-center gap-2">
                <span className="text-[10px] font-extrabold uppercase tracking-widest text-cyan-300 bg-cyan-950/40 px-2.5 py-0.5 rounded-full border border-cyan-500/30">
                  SPECTRA Puzzle Lab
                </span>
                <span className="text-xs font-semibold text-slate-400">&bull; 2–4 min visual thinking</span>
              </div>
              <h1 className="text-xl sm:text-2xl font-black text-white mt-0.5 flex items-center gap-2">
                <span>🔢</span> Pattern Shift
              </h1>
            </div>
          </div>

          {/* Quick Actions */}
          <div className="flex items-center gap-2">
            <button
              onClick={initGame}
              className="px-4 py-2 rounded-xl bg-[#0B1124] hover:bg-[#121B35] border border-white/10 text-slate-300 hover:text-white text-xs font-bold flex items-center gap-2 transition-all shadow-sm"
            >
              <RotateCcw className="w-4 h-4 text-cyan-400" />
              Reset Game
            </button>
          </div>
        </div>

        {/* Live HUD Glass Bar */}
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
          <div className="p-3.5 rounded-2xl bg-[#0B1124]/80 border border-white/[0.08] backdrop-blur-xl flex items-center gap-3">
            <div className="w-9 h-9 rounded-xl bg-cyan-500/10 border border-cyan-500/20 flex items-center justify-center text-cyan-400 shrink-0">
              <Clock className="w-4 h-4" />
            </div>
            <div>
              <span className="text-[10px] font-bold text-slate-400 uppercase block tracking-wider">Time</span>
              <span className="text-lg font-black text-white font-mono">{formatTime(seconds)}</span>
            </div>
          </div>

          <div className="p-3.5 rounded-2xl bg-[#0B1124]/80 border border-white/[0.08] backdrop-blur-xl flex items-center gap-3">
            <div className="w-9 h-9 rounded-xl bg-purple-500/10 border border-purple-500/20 flex items-center justify-center text-purple-400 shrink-0">
              <Flame className="w-4 h-4" />
            </div>
            <div>
              <span className="text-[10px] font-bold text-slate-400 uppercase block tracking-wider">Streak</span>
              <span className="text-lg font-black text-purple-300 font-mono">
                {streak > 0 ? `${streak}x 🔥` : "0"}
              </span>
            </div>
          </div>

          <div className="p-3.5 rounded-2xl bg-[#0B1124]/80 border border-white/[0.08] backdrop-blur-xl flex items-center gap-3">
            <div className="w-9 h-9 rounded-xl bg-emerald-500/10 border border-emerald-500/20 flex items-center justify-center text-emerald-400 shrink-0">
              <CheckCircle2 className="w-4 h-4" />
            </div>
            <div>
              <span className="text-[10px] font-bold text-slate-400 uppercase block tracking-wider">Round</span>
              <span className="text-lg font-black text-emerald-400 font-mono">
                {currentIndex + 1} / {PUZZLE_BANK.length}
              </span>
            </div>
          </div>

          <div className="p-3.5 rounded-2xl bg-[#0B1124]/80 border border-white/[0.08] backdrop-blur-xl flex items-center gap-3">
            <div className="w-9 h-9 rounded-xl bg-amber-500/10 border border-amber-500/20 flex items-center justify-center text-amber-400 shrink-0">
              <Trophy className="w-4 h-4" />
            </div>
            <div>
              <span className="text-[10px] font-bold text-slate-400 uppercase block tracking-wider">Score</span>
              <span className="text-lg font-black text-amber-300 font-mono">
                {score}
              </span>
            </div>
          </div>
        </div>

        {/* Pattern Board Canvas */}
        <div className="relative p-6 sm:p-10 rounded-3xl bg-[#0B1124]/90 border border-white/[0.08] shadow-2xl backdrop-blur-2xl">
          {/* Category Tag */}
          <div className="flex items-center justify-between mb-8">
            <span className="px-3 py-1 rounded-full text-[10px] font-extrabold uppercase tracking-wider bg-purple-500/10 border border-purple-500/30 text-purple-300">
              {currentPuzzle.category} Pattern
            </span>
            <span className="text-xs text-slate-400">
              {currentPuzzle.prompt}
            </span>
          </div>

          {/* Sequence Train */}
          <div className="flex flex-wrap items-center justify-center gap-3 sm:gap-4 my-8">
            {currentPuzzle.sequence.map((item, idx) => (
              <div
                key={idx}
                className="w-14 h-14 sm:w-20 sm:h-20 rounded-2xl bg-[#070A14] border border-white/10 shadow-lg flex items-center justify-center text-2xl sm:text-3xl font-black font-mono text-white transition-all transform hover:scale-105"
              >
                <span className={item.color || "text-white"}>{item.value}</span>
              </div>
            ))}

            {/* Target Missing Slot [ ? ] */}
            <div
              className={`w-14 h-14 sm:w-20 sm:h-20 rounded-2xl border-2 border-dashed flex items-center justify-center text-2xl sm:text-3xl font-black font-mono transition-all duration-300 ${
                selectedAnswer !== null
                  ? isAnswerCorrect
                    ? "bg-emerald-500/20 border-emerald-400 text-emerald-300 shadow-[0_0_25px_rgba(16,185,129,0.5)] scale-110"
                    : "bg-rose-500/20 border-rose-400 text-rose-300"
                  : "border-cyan-400/60 bg-cyan-500/5 text-cyan-300 shadow-[0_0_20px_rgba(6,182,212,0.2)] animate-pulse"
              }`}
            >
              {selectedAnswer !== null ? selectedAnswer : "?"}
            </div>
          </div>

          {/* Interactive Shape/Number Tray */}
          <div className="mt-12 text-center">
            <span className="text-xs font-bold text-slate-400 block mb-4 uppercase tracking-widest">
              ✦ Select the Missing Element ✦
            </span>

            <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 max-w-xl mx-auto">
              {currentPuzzle.options.map((option, idx) => {
                const isSelected = selectedAnswer === option.value;
                return (
                  <button
                    key={idx}
                    onClick={() => handleOptionSelect(option)}
                    disabled={selectedAnswer !== null}
                    className={`p-4 rounded-2xl border transition-all duration-200 flex flex-col items-center justify-center gap-1.5 ${
                      isSelected
                        ? option.isCorrect
                          ? "bg-emerald-500/25 border-emerald-500 text-white shadow-[0_0_25px_rgba(16,185,129,0.4)] scale-105"
                          : "bg-rose-500/25 border-rose-500 text-white"
                        : "bg-[#070A14]/90 border-white/10 hover:border-cyan-500/50 hover:bg-[#0F172E] text-slate-200 hover:text-white shadow-sm hover:scale-[1.03] active:scale-[0.98]"
                    }`}
                  >
                    <span className="text-2xl font-black font-mono">{option.value}</span>
                    <span className="text-[10px] text-slate-400 font-medium">{option.label}</span>
                  </button>
                );
              })}
            </div>
          </div>
        </div>

        {/* Completion Modal */}
        <GameCompletionModal
          isOpen={isCompleted}
          gameTitle="Pattern Shift"
          score={score}
          timeSeconds={seconds}
          isNewBest={isNewBest}
          customStats={[{ label: "Max Streak", value: `${maxStreak}x 🔥` }]}
          onPlayAgain={initGame}
        />
      </div>
    </RoleLayout>
  );
}
