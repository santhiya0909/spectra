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
  HelpCircle,
  Code2,
  Database,
  Cpu,
  Globe,
  Layers,
  Terminal,
  ShieldCheck,
  Bot
} from "lucide-react";

interface CardItem {
  id: number;
  pairId: number;
  title: string;
  iconName: string;
  subtitle: string;
  color: string;
}

const TECH_PAIRS = [
  { pairId: 1, title: "Python", subtitle: "def func():", icon: Terminal, color: "text-amber-400 bg-amber-500/10 border-amber-500/30" },
  { pairId: 2, title: "Database", subtitle: "SELECT *", icon: Database, color: "text-cyan-400 bg-cyan-500/10 border-cyan-500/30" },
  { pairId: 3, title: "React", subtitle: "<Component />", icon: Code2, color: "text-sky-400 bg-sky-500/10 border-sky-500/30" },
  { pairId: 4, title: "AI Neural", subtitle: "Weights & Biases", icon: Bot, color: "text-purple-400 bg-purple-500/10 border-purple-500/30" },
  { pairId: 5, title: "Security", subtitle: "Hash & Auth", icon: ShieldCheck, color: "text-emerald-400 bg-emerald-500/10 border-emerald-500/30" },
  { pairId: 6, title: "Cloud API", subtitle: "HTTP 200 OK", icon: Globe, color: "text-indigo-400 bg-indigo-500/10 border-indigo-500/30" },
];

function shuffleCards() {
  const cards: Array<{
    id: number;
    pairId: number;
    title: string;
    subtitle: string;
    icon: any;
    color: string;
  }> = [];

  TECH_PAIRS.forEach((pair, idx) => {
    // 2 copies of each pair
    cards.push({ id: idx * 2 + 1, ...pair });
    cards.push({ id: idx * 2 + 2, ...pair });
  });

  // Fisher-Yates shuffle
  for (let i = cards.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [cards[i], cards[j]] = [cards[j], cards[i]];
  }

  return cards;
}

export default function MemoryMatchPage() {
  const [cards, setCards] = useState<any[]>([]);
  const [flippedIds, setFlippedIds] = useState<number[]>([]);
  const [matchedIds, setMatchedIds] = useState<number[]>([]);
  const [moves, setMoves] = useState(0);
  const [seconds, setSeconds] = useState(0);
  const [isPlaying, setIsPlaying] = useState(false);
  const [isCompleted, setIsCompleted] = useState(false);
  const [score, setScore] = useState(0);
  const [isNewBest, setIsNewBest] = useState(false);
  const [bestStats, setBestStats] = useState({ bestScore: 0, bestMoves: 0, bestTime: 0 });

  const timerRef = useRef<NodeJS.Timeout | null>(null);

  // Initialize game
  const initGame = () => {
    const newCards = shuffleCards();
    setCards(newCards);
    setFlippedIds([]);
    setMatchedIds([]);
    setMoves(0);
    setSeconds(0);
    setIsPlaying(true);
    setIsCompleted(false);

    if (timerRef.current) clearInterval(timerRef.current);
    timerRef.current = setInterval(() => {
      setSeconds((prev) => prev + 1);
    }, 1000);
  };

  useEffect(() => {
    const stats = getPuzzleLabStats();
    if (stats.games.memory) {
      setBestStats({
        bestScore: stats.games.memory.bestScore,
        bestMoves: stats.games.memory.bestMoves || 0,
        bestTime: stats.games.memory.bestTime,
      });
    }
    initGame();

    return () => {
      if (timerRef.current) clearInterval(timerRef.current);
    };
  }, []);

  const handleCardClick = (id: number) => {
    // Prevent clicking already flipped or matched cards or when 2 are already revealed
    if (flippedIds.includes(id) || matchedIds.includes(id) || flippedIds.length >= 2) {
      return;
    }

    const nextFlipped = [...flippedIds, id];
    setFlippedIds(nextFlipped);

    if (nextFlipped.length === 2) {
      setMoves((m) => m + 1);
      const [firstId, secondId] = nextFlipped;
      const card1 = cards.find((c) => c.id === firstId);
      const card2 = cards.find((c) => c.id === secondId);

      if (card1 && card2 && card1.pairId === card2.pairId) {
        // MATCH!
        setTimeout(() => {
          setMatchedIds((prev) => {
            const next = [...prev, firstId, secondId];
            if (next.length === cards.length) {
              handleGameComplete(moves + 1);
            }
            return next;
          });
          setFlippedIds([]);
        }, 500);
      } else {
        // NO MATCH -> flip back smoothly
        setTimeout(() => {
          setFlippedIds([]);
        }, 900);
      }
    }
  };

  const handleGameComplete = (finalMoves: number) => {
    if (timerRef.current) clearInterval(timerRef.current);
    setIsPlaying(false);

    // Calculate relaxing score (faster time + fewer moves = higher score, max 1000)
    const timePenalty = Math.min(300, seconds * 5);
    const movePenalty = Math.max(0, (finalMoves - 6) * 20);
    const calculatedScore = Math.max(250, 1000 - timePenalty - movePenalty);

    setScore(calculatedScore);

    const { isNewBest: newBestRecord } = recordGameCompletion("memory", calculatedScore, seconds, finalMoves);
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
                <span className="text-xs font-semibold text-slate-400">&bull; 2–3 min casual break</span>
              </div>
              <h1 className="text-xl sm:text-2xl font-black text-white mt-0.5 flex items-center gap-2">
                <span>🧠</span> Memory Match
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
              <Zap className="w-4 h-4" />
            </div>
            <div>
              <span className="text-[10px] font-bold text-slate-400 uppercase block tracking-wider">Moves</span>
              <span className="text-lg font-black text-white font-mono">{moves}</span>
            </div>
          </div>

          <div className="p-3.5 rounded-2xl bg-[#0B1124]/80 border border-white/[0.08] backdrop-blur-xl flex items-center gap-3">
            <div className="w-9 h-9 rounded-xl bg-emerald-500/10 border border-emerald-500/20 flex items-center justify-center text-emerald-400 shrink-0">
              <CheckCircle2 className="w-4 h-4" />
            </div>
            <div>
              <span className="text-[10px] font-bold text-slate-400 uppercase block tracking-wider">Pairs Matched</span>
              <span className="text-lg font-black text-emerald-400 font-mono">
                {matchedIds.length / 2} / {cards.length / 2 || 6}
              </span>
            </div>
          </div>

          <div className="p-3.5 rounded-2xl bg-[#0B1124]/80 border border-white/[0.08] backdrop-blur-xl flex items-center gap-3">
            <div className="w-9 h-9 rounded-xl bg-amber-500/10 border border-amber-500/20 flex items-center justify-center text-amber-400 shrink-0">
              <Trophy className="w-4 h-4" />
            </div>
            <div>
              <span className="text-[10px] font-bold text-slate-400 uppercase block tracking-wider">Best Score</span>
              <span className="text-lg font-black text-amber-300 font-mono">
                {bestStats.bestScore || 920}
              </span>
            </div>
          </div>
        </div>

        {/* Game Canvas / Card Grid */}
        <div className="relative p-6 sm:p-8 rounded-3xl bg-[#0B1124]/90 border border-white/[0.08] shadow-2xl backdrop-blur-2xl">
          <div className="text-center mb-6">
            <span className="text-xs font-black tracking-widest text-cyan-400 uppercase">
              ✦ Match the Concept Pairs ✦
            </span>
            <p className="text-xs text-slate-400 mt-0.5">
              Click two cards to reveal their code symbols. Match all 6 pairs to complete the session.
            </p>
          </div>

          <div className="grid grid-cols-3 sm:grid-cols-4 gap-3 sm:gap-4 max-w-2xl mx-auto">
            {cards.map((card) => {
              const isFlipped = flippedIds.includes(card.id) || matchedIds.includes(card.id);
              const isMatched = matchedIds.includes(card.id);
              const IconComponent = card.icon;

              return (
                <button
                  key={card.id}
                  onClick={() => handleCardClick(card.id)}
                  disabled={isMatched || flippedIds.length >= 2}
                  className={`relative aspect-[4/5] rounded-2xl transition-all duration-300 transform select-none ${
                    isMatched
                      ? "ring-2 ring-emerald-500/50 shadow-[0_0_20px_rgba(16,185,129,0.3)] opacity-90 scale-[0.98]"
                      : isFlipped
                      ? "ring-2 ring-cyan-500/50 shadow-[0_0_20px_rgba(6,182,212,0.3)] scale-[1.02]"
                      : "hover:scale-[1.03] hover:border-white/30"
                  }`}
                  style={{ perspective: 1000 }}
                >
                  <div
                    className={`w-full h-full rounded-2xl border transition-all duration-500 flex flex-col items-center justify-center p-3 text-center ${
                      isFlipped
                        ? "bg-[#0F172E] border-cyan-500/40"
                        : "bg-gradient-to-br from-[#0B1124] to-[#121B35] border-white/10 hover:border-cyan-500/40 cursor-pointer shadow-lg"
                    }`}
                  >
                    {isFlipped ? (
                      <div className="space-y-2 animate-in zoom-in-95 duration-200">
                        <div
                          className={`w-10 h-10 sm:w-12 sm:h-12 mx-auto rounded-xl flex items-center justify-center border ${card.color}`}
                        >
                          <IconComponent className="w-5 h-5 sm:w-6 sm:h-6" />
                        </div>
                        <div>
                          <span className="text-xs sm:text-sm font-black text-white block">
                            {card.title}
                          </span>
                          <span className="text-[10px] text-slate-400 font-mono block mt-0.5">
                            {card.subtitle}
                          </span>
                        </div>
                      </div>
                    ) : (
                      <div className="flex flex-col items-center justify-center space-y-1.5 opacity-80 group-hover:opacity-100">
                        <div className="w-8 h-8 rounded-xl bg-white/[0.04] border border-white/10 flex items-center justify-center text-cyan-400/80">
                          <Sparkles className="w-4 h-4" />
                        </div>
                        <span className="text-[10px] font-bold text-slate-400 uppercase tracking-widest">
                          SPECTRA
                        </span>
                      </div>
                    )}
                  </div>
                </button>
              );
            })}
          </div>
        </div>

        {/* Completion Modal */}
        <GameCompletionModal
          isOpen={isCompleted}
          gameTitle="Memory Match"
          score={score}
          timeSeconds={seconds}
          moves={moves}
          isNewBest={isNewBest}
          onPlayAgain={initGame}
        />
      </div>
    </RoleLayout>
  );
}
