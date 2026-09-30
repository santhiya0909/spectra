"use client";

import React, { useEffect } from "react";
import Link from "next/link";
import { useParams, useRouter } from "next/navigation";
import { RoleLayout } from "@/components/layout/RoleLayout";
import { GlassCard } from "@/components/common/GlassCard";
import {
  ArrowLeft,
  Sparkles,
  Gamepad2,
  Brain,
  Hash,
  Type,
  Grid,
  ArrowRight,
  Smile
} from "lucide-react";

export default function StudentPuzzleRedirectPage() {
  const router = useRouter();
  const params = useParams();

  return (
    <RoleLayout allowedRoles={["STUDENT", "ADMIN", "TEACHER"]}>
      <div className="max-w-3xl mx-auto space-y-6 pb-16 pt-8">
        <div className="p-8 sm:p-12 rounded-3xl bg-[#0B1124] border border-cyan-500/30 shadow-[0_0_50px_rgba(6,182,212,0.15)] text-center space-y-6 backdrop-blur-2xl">
          <div className="w-16 h-16 rounded-2xl bg-gradient-to-tr from-cyan-500 to-purple-600 flex items-center justify-center text-white mx-auto shadow-[0_0_25px_rgba(6,182,212,0.5)]">
            <Gamepad2 className="w-8 h-8" />
          </div>

          <div className="space-y-2">
            <span className="text-xs font-black tracking-widest text-cyan-400 uppercase">
              ✦ SPECTRA PUZZLE LAB ✦
            </span>
            <h1 className="text-2xl sm:text-3xl font-black text-white">
              Take a Break. Play a Mini-Game.
            </h1>
            <p className="text-sm text-slate-300 max-w-md mx-auto leading-relaxed">
              No multiple-choice questions or exams here! Choose a quick 2–3 minute mini-game to relax and recharge your cognitive focus.
            </p>
          </div>

          {/* Quick Mini-Game Options */}
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 pt-4">
            <Link
              href="/student/puzzles/memory"
              className="p-4 rounded-2xl bg-[#070A14] border border-white/10 hover:border-cyan-500/50 hover:bg-[#0F172E] transition-all flex flex-col items-center gap-2 group"
            >
              <span className="text-2xl group-hover:scale-110 transition-transform">🧠</span>
              <span className="text-xs font-bold text-white">Memory Match</span>
              <span className="text-[10px] text-cyan-400">2–3 min</span>
            </Link>

            <Link
              href="/student/puzzles/pattern"
              className="p-4 rounded-2xl bg-[#070A14] border border-white/10 hover:border-purple-500/50 hover:bg-[#0F172E] transition-all flex flex-col items-center gap-2 group"
            >
              <span className="text-2xl group-hover:scale-110 transition-transform">🔢</span>
              <span className="text-xs font-bold text-white">Pattern Shift</span>
              <span className="text-[10px] text-purple-400">2–4 min</span>
            </Link>

            <Link
              href="/student/puzzles/word"
              className="p-4 rounded-2xl bg-[#070A14] border border-white/10 hover:border-emerald-500/50 hover:bg-[#0F172E] transition-all flex flex-col items-center gap-2 group"
            >
              <span className="text-2xl group-hover:scale-110 transition-transform">🔤</span>
              <span className="text-xs font-bold text-white">Word Scramble</span>
              <span className="text-[10px] text-emerald-400">2–3 min</span>
            </Link>

            <Link
              href="/student/puzzles/tiles"
              className="p-4 rounded-2xl bg-[#070A14] border border-white/10 hover:border-amber-500/50 hover:bg-[#0F172E] transition-all flex flex-col items-center gap-2 group"
            >
              <span className="text-2xl group-hover:scale-110 transition-transform">🧩</span>
              <span className="text-xs font-bold text-white">Tile Puzzle</span>
              <span className="text-[10px] text-amber-400">3–5 min</span>
            </Link>
          </div>

          {/* Action Row */}
          <div className="pt-6 border-t border-white/[0.08] flex items-center justify-center gap-4">
            <Link
              href="/student/puzzles"
              className="px-6 py-2.5 rounded-xl bg-cyan-500 hover:bg-cyan-400 text-black font-extrabold text-xs flex items-center gap-2 shadow-[0_0_20px_rgba(6,182,212,0.4)] transition-all"
            >
              Open Full Puzzle Lab <ArrowRight className="w-4 h-4" />
            </Link>
          </div>
        </div>
      </div>
    </RoleLayout>
  );
}
