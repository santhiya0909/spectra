"use client";

import React, { useState, useEffect } from "react";
import Link from "next/link";
import { RoleLayout } from "@/components/layout/RoleLayout";
import { GlassCard } from "@/components/common/GlassCard";
import { getPuzzleLabStats, PuzzleLabStats } from "@/lib/puzzleLab";
import {
  Sparkles,
  Zap,
  Clock,
  Trophy,
  ArrowRight,
  Flame,
  Brain,
  Hash,
  Type,
  Grid,
  Gamepad2,
  CheckCircle2,
  Shield,
  Activity,
  Smile
} from "lucide-react";

interface MiniGameDef {
  key: "memory" | "pattern" | "word" | "tiles";
  title: string;
  icon: any;
  emoji: string;
  description: string;
  timeEstimate: string;
  difficulty: "Casual" | "Medium" | "Challenging";
  href: string;
  accentColor: string;
  badgeBg: string;
  badgeBorder: string;
  badgeText: string;
}

const MINI_GAMES: MiniGameDef[] = [
  {
    key: "memory",
    title: "Memory Match",
    icon: Brain,
    emoji: "🧠",
    description: "Match tech concepts & code symbol pairs to test and train your recall.",
    timeEstimate: "2–3 min",
    difficulty: "Casual",
    href: "/student/puzzles/memory",
    accentColor: "from-cyan-500/20 to-sky-500/10 border-cyan-500/30 hover:border-cyan-400",
    badgeBg: "bg-cyan-500/15",
    badgeBorder: "border-cyan-500/30",
    badgeText: "text-cyan-300",
  },
  {
    key: "pattern",
    title: "Pattern Shift",
    icon: Hash,
    emoji: "🔢",
    description: "Shift through visual sequences, orbital rotations, and numerical logic patterns.",
    timeEstimate: "2–4 min",
    difficulty: "Medium",
    href: "/student/puzzles/pattern",
    accentColor: "from-purple-500/20 to-indigo-500/10 border-purple-500/30 hover:border-purple-400",
    badgeBg: "bg-purple-500/15",
    badgeBorder: "border-purple-500/30",
    badgeText: "text-purple-300",
  },
  {
    key: "word",
    title: "Word Scramble",
    icon: Type,
    emoji: "🔤",
    description: "Rearrange scrambled letter tiles into computer science & logic terminology.",
    timeEstimate: "2–3 min",
    difficulty: "Casual",
    href: "/student/puzzles/word",
    accentColor: "from-emerald-500/20 to-teal-500/10 border-emerald-500/30 hover:border-emerald-400",
    badgeBg: "bg-emerald-500/15",
    badgeBorder: "border-emerald-500/30",
    badgeText: "text-emerald-300",
  },
  {
    key: "tiles",
    title: "Tile Puzzle",
    icon: Grid,
    emoji: "🧩",
    description: "Slide numbered tiles into perfect sequential order with minimum moves.",
    timeEstimate: "3–5 min",
    difficulty: "Medium",
    href: "/student/puzzles/tiles",
    accentColor: "from-amber-500/20 to-orange-500/10 border-amber-500/30 hover:border-amber-400",
    badgeBg: "bg-amber-500/15",
    badgeBorder: "border-amber-500/30",
    badgeText: "text-amber-300",
  },
];

export default function StudentPuzzleLabPage() {
  const [stats, setStats] = useState<PuzzleLabStats | null>(null);

  useEffect(() => {
    setStats(getPuzzleLabStats());
  }, []);

  return (
    <RoleLayout allowedRoles={["STUDENT", "ADMIN", "TEACHER"]}>
      <div className="max-w-7xl mx-auto space-y-8 pb-16">
        {/* HERO BANNER: SPECTRA PUZZLE LAB */}
        <div className="relative overflow-hidden rounded-3xl border border-white/[0.08] bg-gradient-to-br from-[#0B1124] via-[#0F172E] to-[#080C1A] p-6 sm:p-10 shadow-2xl backdrop-blur-2xl">
          {/* Ambient Lighting Orbs */}
          <div className="absolute top-0 right-1/4 -mt-20 w-96 h-96 rounded-full bg-cyan-500/10 blur-3xl pointer-events-none" />
          <div className="absolute bottom-0 right-0 -mr-20 w-80 h-80 rounded-full bg-purple-500/10 blur-3xl pointer-events-none" />

          <div className="relative z-10 flex flex-col lg:flex-row lg:items-center justify-between gap-8">
            <div className="space-y-3 max-w-2xl">
              <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-cyan-500/10 border border-cyan-500/30 text-cyan-300 text-xs font-black tracking-wider uppercase">
                <Gamepad2 className="w-3.5 h-3.5 text-cyan-400" />
                SPECTRA Puzzle Lab
              </div>

              <h1 className="text-3xl sm:text-4xl lg:text-5xl font-black text-white tracking-tight">
                🧩 SPECTRA PUZZLE LAB
              </h1>

              <p className="text-slate-300 text-sm sm:text-base leading-relaxed italic">
                &ldquo;Take a break. Play something quick. Keep your mind sharp.&rdquo;
              </p>

              <div className="flex flex-wrap items-center gap-3 pt-2 text-xs text-slate-400">
                <span className="flex items-center gap-1.5 text-slate-300">
                  <Smile className="w-4 h-4 text-emerald-400" /> Zero Exam Stress
                </span>
                <span>&bull;</span>
                <span className="flex items-center gap-1.5 text-slate-300">
                  <Zap className="w-4 h-4 text-cyan-400" /> +20 XP Per Play
                </span>
                <span>&bull;</span>
                <span className="flex items-center gap-1.5 text-slate-300">
                  <Brain className="w-4 h-4 text-purple-400" /> Cognitive Workout
                </span>
              </div>
            </div>

            {/* TODAY'S MINI CHALLENGE HERO CARD */}
            <div className="w-full lg:w-80 p-5 rounded-2xl bg-[#070A14]/90 border border-cyan-500/30 shadow-[0_0_30px_rgba(6,182,212,0.15)] flex flex-col justify-between space-y-4">
              <div className="space-y-1.5">
                <div className="flex items-center justify-between">
                  <span className="text-[10px] font-black uppercase tracking-widest text-cyan-400">
                    ✦ Today&apos;s Mini Challenge
                  </span>
                  <span className="text-[10px] font-bold text-amber-400 bg-amber-500/10 px-2 py-0.5 rounded-full border border-amber-500/30">
                    2 min
                  </span>
                </div>
                <h3 className="text-base font-black text-white">
                  Beat Your Memory Match Record
                </h3>
                <p className="text-xs text-slate-400 leading-normal">
                  Can you beat your best score of {stats?.games?.memory?.bestScore || 920} in under 60 seconds?
                </p>
              </div>

              <Link
                href="/student/puzzles/memory"
                className="w-full py-2.5 px-4 rounded-xl bg-gradient-to-r from-cyan-500 to-sky-500 hover:from-cyan-400 hover:to-sky-400 text-black font-extrabold text-xs flex items-center justify-center gap-2 shadow-[0_0_20px_rgba(6,182,212,0.4)] transition-all"
              >
                Play Now <ArrowRight className="w-4 h-4" />
              </Link>
            </div>
          </div>
        </div>

        {/* COGNITIVE ACTIVITY STATS (LIGHTWEIGHT ENGAGEMENT) */}
        <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
          <div className="p-5 rounded-3xl bg-white/80 dark:bg-[#0B1124]/80 border border-slate-200/90 dark:border-white/[0.08] backdrop-blur-xl shadow-[0_8px_30px_rgb(0,0,0,0.04)] dark:shadow-lg flex items-center gap-4">
            <div className="w-12 h-12 rounded-2xl bg-cyan-500/15 border border-cyan-500/30 flex items-center justify-center text-cyan-500 dark:text-cyan-400 shrink-0 shadow-[0_0_15px_rgba(6,182,212,0.2)]">
              <Activity className="w-6 h-6" />
            </div>
            <div>
              <span className="text-[10px] font-extrabold text-slate-500 dark:text-slate-400 uppercase tracking-widest block">
                Puzzle Sessions
              </span>
              <span className="text-2xl sm:text-3xl font-black text-slate-900 dark:text-white font-mono">
                {stats?.totalSessions || 8}
              </span>
              <span className="text-[10px] text-slate-500 dark:text-slate-400 block mt-0.5">
                This week: +3 sessions
              </span>
            </div>
          </div>

          <div className="p-5 rounded-3xl bg-white/80 dark:bg-[#0B1124]/80 border border-slate-200/90 dark:border-white/[0.08] backdrop-blur-xl shadow-[0_8px_30px_rgb(0,0,0,0.04)] dark:shadow-lg flex items-center gap-4">
            <div className="w-12 h-12 rounded-2xl bg-purple-500/15 border border-purple-500/30 flex items-center justify-center text-purple-600 dark:text-purple-400 shrink-0 shadow-[0_0_15px_rgba(139,92,246,0.2)]">
              <Trophy className="w-6 h-6" />
            </div>
            <div>
              <span className="text-[10px] font-extrabold text-slate-500 dark:text-slate-400 uppercase tracking-widest block">
                Best Score
              </span>
              <span className="text-2xl sm:text-3xl font-black text-slate-900 dark:text-white font-mono">
                {Math.max(
                  stats?.games?.memory?.bestScore || 0,
                  stats?.games?.pattern?.bestScore || 0,
                  stats?.games?.word?.bestScore || 0,
                  stats?.games?.tiles?.bestScore || 0,
                  960
                )}
              </span>
              <span className="text-[10px] text-slate-500 dark:text-slate-400 block mt-0.5">
                All-time lab record
              </span>
            </div>
          </div>

          <div className="p-5 rounded-3xl bg-white/80 dark:bg-[#0B1124]/80 border border-slate-200/90 dark:border-white/[0.08] backdrop-blur-xl shadow-[0_8px_30px_rgb(0,0,0,0.04)] dark:shadow-lg flex items-center gap-4">
            <div className="w-12 h-12 rounded-2xl bg-amber-500/15 border border-amber-500/30 flex items-center justify-center text-amber-600 dark:text-amber-400 shrink-0 shadow-[0_0_15px_rgba(245,158,11,0.2)]">
              <Flame className="w-6 h-6" />
            </div>
            <div>
              <span className="text-[10px] font-extrabold text-slate-500 dark:text-slate-400 uppercase tracking-widest block">
                Daily Streak
              </span>
              <span className="text-2xl sm:text-3xl font-black text-slate-900 dark:text-white font-mono">
                {stats?.currentStreak || 3} Days
              </span>
              <span className="text-[10px] text-slate-500 dark:text-slate-400 block mt-0.5">
                Keep the rhythm going
              </span>
            </div>
          </div>

          <div className="p-5 rounded-3xl bg-white/80 dark:bg-[#0B1124]/80 border border-slate-200/90 dark:border-white/[0.08] backdrop-blur-xl shadow-[0_8px_30px_rgb(0,0,0,0.04)] dark:shadow-lg flex items-center gap-4">
            <div className="w-12 h-12 rounded-2xl bg-emerald-500/15 border border-emerald-500/30 flex items-center justify-center text-emerald-600 dark:text-emerald-400 shrink-0 shadow-[0_0_15px_rgba(16,185,129,0.2)]">
              <Zap className="w-6 h-6" />
            </div>
            <div>
              <span className="text-[10px] font-extrabold text-slate-500 dark:text-slate-400 uppercase tracking-widest block">
                Bonus XP Earned
              </span>
              <span className="text-2xl sm:text-3xl font-black text-emerald-600 dark:text-emerald-400 font-mono">
                +{stats?.totalXpEarned || 160}
              </span>
              <span className="text-[10px] text-slate-500 dark:text-slate-400 block mt-0.5">
                Added to SPECTRA Level
              </span>
            </div>
          </div>
        </div>

        {/* 4 MINI-GAMES SELECTION GRID */}
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <div>
              <h2 className="text-xl font-black text-slate-900 dark:text-white">Choose a Mini-Game</h2>
              <p className="text-xs text-slate-600 dark:text-slate-400">
                Pick any game for a quick 2–5 minute relaxing challenge.
              </p>
            </div>
            <span className="text-xs font-semibold text-cyan-600 dark:text-cyan-400">4 Games Available</span>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
            {MINI_GAMES.map((game) => {
              const gameStats = stats?.games[game.key];
              const bestScore = gameStats?.bestScore || 0;
              const IconComponent = game.icon;

              return (
                <div
                  key={game.key}
                  className={`group relative rounded-3xl bg-white/80 dark:bg-transparent bg-gradient-to-br ${game.accentColor} p-6 sm:p-7 border border-slate-200/90 dark:border-white/10 shadow-lg backdrop-blur-2xl transition-all duration-300 hover:scale-[1.01] hover:shadow-[0_0_30px_rgba(6,182,212,0.15)] flex flex-col justify-between`}
                >
                  <div className="space-y-4">
                    {/* Top Row: Icon + Badges */}
                    <div className="flex items-start justify-between">
                      <div className="w-14 h-14 rounded-2xl bg-slate-100 dark:bg-[#070A14] border border-slate-200 dark:border-white/10 flex items-center justify-center text-3xl shadow-md group-hover:scale-110 transition-transform">
                        <span>{game.emoji}</span>
                      </div>

                      <div className="flex items-center gap-2">
                        <span className={`px-2.5 py-1 rounded-full text-[10px] font-black uppercase tracking-wider ${game.badgeBg} border ${game.badgeBorder} ${game.badgeText}`}>
                          {game.difficulty}
                        </span>
                        <span className="px-2.5 py-1 rounded-full text-[10px] font-bold text-slate-600 dark:text-slate-400 bg-slate-100 dark:bg-black/40 border border-slate-200 dark:border-white/10">
                          {game.timeEstimate}
                        </span>
                      </div>
                    </div>

                    {/* Game Title & Description */}
                    <div>
                      <h3 className="text-xl font-black text-slate-900 dark:text-white group-hover:text-cyan-600 dark:group-hover:text-cyan-300 transition-colors">
                        {game.title}
                      </h3>
                      <p className="text-xs text-slate-600 dark:text-slate-300 mt-1 leading-relaxed">
                        {game.description}
                      </p>
                    </div>
                  </div>

                  {/* Bottom Row: Best Score & Play Button */}
                  <div className="pt-6 mt-4 border-t border-slate-200 dark:border-white/[0.08] flex items-center justify-between">
                    <div>
                      <span className="text-[10px] font-bold text-slate-500 dark:text-slate-400 uppercase tracking-widest block">
                        Personal Best
                      </span>
                      <span className="text-sm font-black text-amber-600 dark:text-amber-300 font-mono">
                        {bestScore > 0 ? `${bestScore} pts` : "Unplayed"}
                      </span>
                    </div>

                    <Link
                      href={game.href}
                      className="px-5 py-2.5 rounded-xl bg-slate-900 hover:bg-cyan-500 text-white hover:text-black dark:bg-white dark:hover:bg-cyan-400 dark:text-black font-extrabold text-xs flex items-center gap-2 shadow-lg transition-all group-hover:shadow-[0_0_20px_rgba(255,255,255,0.4)]"
                    >
                      Play <ArrowRight className="w-4 h-4" />
                    </Link>
                  </div>
                </div>
              );
            })}
          </div>
        </div>

        {/* COGNITIVE RELAXATION PHILOSOPHY CARD */}
        <div className="p-6 rounded-3xl bg-white/80 dark:bg-[#0B1124]/60 border border-slate-200/90 dark:border-white/[0.08] shadow-[0_8px_30px_rgb(0,0,0,0.04)] dark:shadow-none backdrop-blur-xl flex flex-col sm:flex-row items-center justify-between gap-4 text-center sm:text-left">
          <div className="flex items-center gap-4">
            <div className="w-12 h-12 rounded-2xl bg-cyan-500/10 border border-cyan-500/20 flex items-center justify-center text-cyan-600 dark:text-cyan-400 shrink-0">
              <Shield className="w-6 h-6" />
            </div>
            <div>
              <h4 className="text-sm font-black text-slate-900 dark:text-white">
                How does Puzzle Lab affect your Knowledge DNA?
              </h4>
              <p className="text-xs text-slate-600 dark:text-slate-400 mt-0.5">
                Puzzle Lab sessions reward bonus XP and stimulate focus without penalizing your Knowledge DNA. Real exams & quizzes remain separate.
              </p>
            </div>
          </div>

          <Link
            href="/student/knowledge-dna"
            className="px-4 py-2 rounded-xl bg-slate-100 hover:bg-slate-200 border border-slate-200 text-slate-700 hover:text-slate-900 dark:bg-[#0F172E] dark:hover:bg-[#1E293B] dark:border-white/10 text-xs font-bold dark:text-slate-300 dark:hover:text-white shrink-0 transition-colors"
          >
            View Knowledge DNA &rarr;
          </Link>
        </div>
      </div>
    </RoleLayout>
  );
}
