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
  Shuffle,
  Lightbulb,
  HelpCircle,
  Delete,
  Flame
} from "lucide-react";

interface WordItem {
  word: string;
  category: string;
  hint: string;
}

const WORDS_BANK: WordItem[] = [
  { word: "PYTHON", category: "Programming", hint: "High-level language known for clean syntax and AI libraries" },
  { word: "SCHEMA", category: "Database", hint: "Blueprint structure representing table relationships & types" },
  { word: "BINARY", category: "Computer Systems", hint: "Base-2 numeric representation using only 0 and 1" },
  { word: "SYNTAX", category: "Compilers", hint: "Grammar rules defining valid code expressions in a language" },
  { word: "VECTOR", category: "Mathematics & AI", hint: "Mathematical object with magnitude and direction in n-dimensional space" },
  { word: "MATRIX", category: "Linear Algebra", hint: "Rectangular array of numbers arranged in rows and columns" },
  { word: "ROUTER", category: "Networking", hint: "Hardware or software device forwarding packets between networks" },
];

function scrambleString(str: string): string[] {
  const arr = str.split("");
  // Ensure it's not identical to the original word
  let attempts = 0;
  while (attempts < 10) {
    for (let i = arr.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [arr[i], arr[j]] = [arr[j], arr[i]];
    }
    if (arr.join("") !== str) break;
    attempts++;
  }
  return arr;
}

export default function WordScramblePage() {
  const [wordIndex, setWordIndex] = useState(0);
  const [targetWord, setTargetWord] = useState("");
  const [scrambledPool, setScrambledPool] = useState<Array<{ id: number; letter: string; used: boolean }>>([]);
  const [placedSlots, setPlacedSlots] = useState<Array<{ letter: string; poolId: number } | null>>([]);
  const [showHint, setShowHint] = useState(false);
  const [isSuccess, setIsSuccess] = useState(false);
  const [score, setScore] = useState(0);
  const [streak, setStreak] = useState(0);
  const [seconds, setSeconds] = useState(0);
  const [isCompleted, setIsCompleted] = useState(false);
  const [isNewBest, setIsNewBest] = useState(false);
  const [bestStats, setBestStats] = useState({ bestScore: 0, bestTime: 0 });

  const timerRef = useRef<NodeJS.Timeout | null>(null);

  const currentItem = WORDS_BANK[wordIndex % WORDS_BANK.length];

  const loadWord = (index: number) => {
    const item = WORDS_BANK[index % WORDS_BANK.length];
    setTargetWord(item.word);
    setShowHint(false);
    setIsSuccess(false);

    const letters = scrambleString(item.word);
    setScrambledPool(letters.map((l, i) => ({ id: i, letter: l, used: false })));
    setPlacedSlots(new Array(item.word.length).fill(null));
  };

  const initGame = () => {
    setWordIndex(0);
    setScore(0);
    setStreak(0);
    setSeconds(0);
    setIsCompleted(false);
    loadWord(0);

    if (timerRef.current) clearInterval(timerRef.current);
    timerRef.current = setInterval(() => {
      setSeconds((prev) => prev + 1);
    }, 1000);
  };

  useEffect(() => {
    const stats = getPuzzleLabStats();
    if (stats.games.word) {
      setBestStats({
        bestScore: stats.games.word.bestScore,
        bestTime: stats.games.word.bestTime,
      });
    }
    initGame();

    return () => {
      if (timerRef.current) clearInterval(timerRef.current);
    };
  }, []);

  // Click a letter tile in pool -> place in next empty slot
  const handleSelectPoolLetter = (item: { id: number; letter: string; used: boolean }) => {
    if (item.used || isSuccess) return;

    const firstEmptyIndex = placedSlots.findIndex((s) => s === null);
    if (firstEmptyIndex === -1) return;

    const nextSlots = [...placedSlots];
    nextSlots[firstEmptyIndex] = { letter: item.letter, poolId: item.id };
    setPlacedSlots(nextSlots);

    setScrambledPool((prev) =>
      prev.map((p) => (p.id === item.id ? { ...p, used: true } : p))
    );

    // Check if word is complete
    checkAnswer(nextSlots);
  };

  // Click a placed letter -> return to pool
  const handleRemovePlacedLetter = (slotIndex: number) => {
    if (isSuccess) return;
    const slot = placedSlots[slotIndex];
    if (!slot) return;

    const nextSlots = [...placedSlots];
    nextSlots[slotIndex] = null;
    setPlacedSlots(nextSlots);

    setScrambledPool((prev) =>
      prev.map((p) => (p.id === slot.poolId ? { ...p, used: false } : p))
    );
  };

  // Reset current word slots
  const handleClear = () => {
    if (isSuccess) return;
    setPlacedSlots(new Array(targetWord.length).fill(null));
    setScrambledPool((prev) => prev.map((p) => ({ ...p, used: false })));
  };

  // Re-shuffle unused letters
  const handleShuffle = () => {
    if (isSuccess) return;
    const unused = scrambledPool.filter((p) => !p.used);
    for (let i = unused.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [unused[i], unused[j]] = [unused[j], unused[i]];
    }
    setScrambledPool((prev) => {
      const usedItems = prev.filter((p) => p.used);
      return [...usedItems, ...unused];
    });
  };

  const checkAnswer = (slots: Array<{ letter: string; poolId: number } | null>) => {
    const isAllFilled = slots.every((s) => s !== null);
    if (!isAllFilled) return;

    const assembled = slots.map((s) => s?.letter).join("");
    if (assembled === targetWord) {
      // WORD SOLVED!
      setIsSuccess(true);
      const earned = Math.round(200 * (1 + streak * 0.25));
      setScore((s) => s + earned);
      setStreak((st) => st + 1);

      setTimeout(() => {
        if (wordIndex + 1 < 4) {
          // Play 4 words per quick session
          setWordIndex((prev) => {
            const nextIdx = prev + 1;
            loadWord(nextIdx);
            return nextIdx;
          });
        } else {
          handleGameComplete();
        }
      }, 1000);
    }
  };

  const handleGameComplete = () => {
    if (timerRef.current) clearInterval(timerRef.current);

    const finalScore = score + 100;
    const { isNewBest: newBestRecord } = recordGameCompletion("word", finalScore, seconds);
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
                <span className="text-xs font-semibold text-slate-400">&bull; 2–3 min word builder</span>
              </div>
              <h1 className="text-xl sm:text-2xl font-black text-white mt-0.5 flex items-center gap-2">
                <span>🔤</span> Word Scramble
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
              <span className="text-[10px] font-bold text-slate-400 uppercase block tracking-wider">Progress</span>
              <span className="text-lg font-black text-emerald-400 font-mono">
                {wordIndex + 1} / 4
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

        {/* Word Scramble Canvas */}
        <div className="relative p-6 sm:p-10 rounded-3xl bg-[#0B1124]/90 border border-white/[0.08] shadow-2xl backdrop-blur-2xl">
          {/* Category Tag & Hint Toggle */}
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 mb-8">
            <span className="px-3.5 py-1.5 rounded-full text-xs font-extrabold uppercase tracking-wider bg-cyan-500/10 border border-cyan-500/30 text-cyan-300 inline-block w-fit">
              Domain: {currentItem.category}
            </span>

            <button
              onClick={() => setShowHint(!showHint)}
              className="px-3 py-1.5 rounded-xl bg-[#0F172E] hover:bg-[#1E293B] border border-white/10 text-xs font-semibold text-slate-300 hover:text-white flex items-center gap-1.5 transition-colors w-fit"
            >
              <Lightbulb className={`w-3.5 h-3.5 ${showHint ? "text-amber-400" : "text-slate-400"}`} />
              {showHint ? "Hide Clue" : "Need a Hint?"}
            </button>
          </div>

          {showHint && (
            <div className="p-3 rounded-2xl bg-amber-500/10 border border-amber-500/20 text-xs text-amber-300 mb-6 flex items-center gap-2 animate-in fade-in duration-200">
              <Sparkles className="w-4 h-4 shrink-0 text-amber-400" />
              <span>{currentItem.hint}</span>
            </div>
          )}

          {/* Target Slots Row */}
          <div className="text-center mb-8">
            <span className="text-xs font-bold text-slate-400 block mb-4 uppercase tracking-widest">
              ✦ Target Word ✦
            </span>

            <div className="flex flex-wrap items-center justify-center gap-2 sm:gap-3">
              {placedSlots.map((slot, idx) => (
                <button
                  key={idx}
                  onClick={() => handleRemovePlacedLetter(idx)}
                  className={`w-12 h-14 sm:w-16 sm:h-18 rounded-2xl border-2 transition-all flex items-center justify-center text-xl sm:text-2xl font-black font-mono select-none ${
                    isSuccess
                      ? "bg-emerald-500/25 border-emerald-400 text-emerald-300 shadow-[0_0_20px_rgba(16,185,129,0.5)] scale-105"
                      : slot
                      ? "bg-[#0F172E] border-cyan-400/60 text-white shadow-md hover:border-rose-400 hover:text-rose-300"
                      : "bg-[#070A14] border-dashed border-white/20 text-transparent"
                  }`}
                  title={slot ? "Click to remove letter" : "Empty slot"}
                >
                  {slot ? slot.letter : ""}
                </button>
              ))}
            </div>
          </div>

          {/* Letter Pool */}
          <div className="mt-10 text-center">
            <span className="text-xs font-bold text-slate-400 block mb-4 uppercase tracking-widest">
              ✦ Scrambled Letters ✦
            </span>

            <div className="flex flex-wrap items-center justify-center gap-2 sm:gap-3 max-w-lg mx-auto">
              {scrambledPool.map((item) => (
                <button
                  key={item.id}
                  onClick={() => handleSelectPoolLetter(item)}
                  disabled={item.used || isSuccess}
                  className={`w-12 h-14 sm:w-16 sm:h-18 rounded-2xl border transition-all duration-200 flex items-center justify-center text-xl sm:text-2xl font-black font-mono shadow-md ${
                    item.used
                      ? "opacity-20 border-white/5 bg-transparent cursor-not-allowed scale-95"
                      : "bg-gradient-to-b from-[#121B35] to-[#0B1124] border-white/20 hover:border-cyan-400 text-white hover:scale-105 hover:shadow-[0_0_15px_rgba(6,182,212,0.3)] active:scale-95"
                  }`}
                >
                  {item.letter}
                </button>
              ))}
            </div>

            {/* Helper Buttons: Shuffle & Clear */}
            <div className="flex items-center justify-center gap-3 mt-8">
              <button
                onClick={handleShuffle}
                disabled={isSuccess}
                className="px-4 py-2 rounded-xl bg-[#0F172E] hover:bg-[#1E293B] border border-white/10 text-xs font-bold text-slate-300 hover:text-white flex items-center gap-2 transition-colors"
              >
                <Shuffle className="w-3.5 h-3.5 text-cyan-400" />
                Shuffle Letters
              </button>

              <button
                onClick={handleClear}
                disabled={isSuccess}
                className="px-4 py-2 rounded-xl bg-[#0F172E] hover:bg-[#1E293B] border border-white/10 text-xs font-bold text-slate-300 hover:text-white flex items-center gap-2 transition-colors"
              >
                <RotateCcw className="w-3.5 h-3.5 text-rose-400" />
                Clear Word
              </button>
            </div>
          </div>
        </div>

        {/* Completion Modal */}
        <GameCompletionModal
          isOpen={isCompleted}
          gameTitle="Word Scramble"
          score={score}
          timeSeconds={seconds}
          isNewBest={isNewBest}
          onPlayAgain={initGame}
        />
      </div>
    </RoleLayout>
  );
}
