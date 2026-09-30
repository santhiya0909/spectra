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
  Grid,
  HelpCircle
} from "lucide-react";

type Board = (number | null)[];

const SOLVED_BOARD: Board = [1, 2, 3, 4, 5, 6, 7, 8, null];

// Helper to get valid neighbor indices for a given index in a 3x3 grid
function getValidNeighbors(idx: number): number[] {
  const row = Math.floor(idx / 3);
  const col = idx % 3;
  const neighbors: number[] = [];

  if (row > 0) neighbors.push(idx - 3); // Up
  if (row < 2) neighbors.push(idx + 3); // Down
  if (col > 0) neighbors.push(idx - 1); // Left
  if (col < 2) neighbors.push(idx + 1); // Right

  return neighbors;
}

// Generate guaranteed solvable board by simulating random valid moves from solved state
function createSolvableBoard(steps = 45): Board {
  let board = [...SOLVED_BOARD];
  let emptyIdx = 8;
  let lastMovedIdx = -1;

  for (let s = 0; s < steps; s++) {
    const validMoves = getValidNeighbors(emptyIdx).filter((n) => n !== lastMovedIdx);
    const chosen = validMoves[Math.floor(Math.random() * validMoves.length)];

    // Swap empty with chosen
    board[emptyIdx] = board[chosen];
    board[chosen] = null;
    lastMovedIdx = emptyIdx;
    emptyIdx = chosen;
  }

  // Ensure it's not already solved
  if (checkIsSolved(board)) {
    return createSolvableBoard(steps + 5);
  }

  return board;
}

function checkIsSolved(board: Board): boolean {
  for (let i = 0; i < 8; i++) {
    if (board[i] !== i + 1) return false;
  }
  return board[8] === null;
}

export default function TilePuzzlePage() {
  const [board, setBoard] = useState<Board>(SOLVED_BOARD);
  const [moves, setMoves] = useState(0);
  const [seconds, setSeconds] = useState(0);
  const [isPlaying, setIsPlaying] = useState(false);
  const [isCompleted, setIsCompleted] = useState(false);
  const [score, setScore] = useState(0);
  const [isNewBest, setIsNewBest] = useState(false);
  const [bestStats, setBestStats] = useState({ bestScore: 0, bestMoves: 0, bestTime: 0 });

  const timerRef = useRef<NodeJS.Timeout | null>(null);

  const initGame = () => {
    const newBoard = createSolvableBoard(40);
    setBoard(newBoard);
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
    if (stats.games.tiles) {
      setBestStats({
        bestScore: stats.games.tiles.bestScore,
        bestMoves: stats.games.tiles.bestMoves || 0,
        bestTime: stats.games.tiles.bestTime,
      });
    }
    initGame();

    return () => {
      if (timerRef.current) clearInterval(timerRef.current);
    };
  }, []);

  const emptyIndex = board.indexOf(null);
  const movableNeighbors = getValidNeighbors(emptyIndex);

  const handleTileClick = (idx: number) => {
    if (!isPlaying || isCompleted) return;

    if (movableNeighbors.includes(idx)) {
      // Valid move -> swap tile with empty slot
      const nextBoard = [...board];
      nextBoard[emptyIndex] = board[idx];
      nextBoard[idx] = null;
      setBoard(nextBoard);

      const nextMoves = moves + 1;
      setMoves(nextMoves);

      // Check win condition
      if (checkIsSolved(nextBoard)) {
        handleGameComplete(nextMoves);
      }
    }
  };

  const handleGameComplete = (finalMoves: number) => {
    if (timerRef.current) clearInterval(timerRef.current);
    setIsPlaying(false);

    // Score based on efficiency (base 1000 - moves - time)
    const timePenalty = Math.min(300, seconds * 4);
    const movePenalty = Math.max(0, (finalMoves - 20) * 15);
    const calculatedScore = Math.max(300, 1000 - timePenalty - movePenalty);

    setScore(calculatedScore);

    const { isNewBest: newBestRecord } = recordGameCompletion("tiles", calculatedScore, seconds, finalMoves);
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
                <span className="text-xs font-semibold text-slate-400">&bull; 3–5 min logic slider</span>
              </div>
              <h1 className="text-xl sm:text-2xl font-black text-white mt-0.5 flex items-center gap-2">
                <span>🧩</span> Tile Puzzle
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
              New Shuffle
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
              <span className="text-lg font-black text-purple-300 font-mono">{moves}</span>
            </div>
          </div>

          <div className="p-3.5 rounded-2xl bg-[#0B1124]/80 border border-white/[0.08] backdrop-blur-xl flex items-center gap-3">
            <div className="w-9 h-9 rounded-xl bg-emerald-500/10 border border-emerald-500/20 flex items-center justify-center text-emerald-400 shrink-0">
              <CheckCircle2 className="w-4 h-4" />
            </div>
            <div>
              <span className="text-[10px] font-bold text-slate-400 uppercase block tracking-wider">Best Moves</span>
              <span className="text-lg font-black text-emerald-400 font-mono">
                {bestStats.bestMoves ? `${bestStats.bestMoves}` : "—"}
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
                {bestStats.bestScore || 780}
              </span>
            </div>
          </div>
        </div>

        {/* Sliding Grid Canvas */}
        <div className="relative p-6 sm:p-10 rounded-3xl bg-[#0B1124]/90 border border-white/[0.08] shadow-2xl backdrop-blur-2xl">
          <div className="text-center mb-6">
            <span className="text-xs font-black tracking-widest text-cyan-400 uppercase">
              ✦ Arrange in Sequential Order ✦
            </span>
            <p className="text-xs text-slate-400 mt-0.5">
              Click any highlighted tile adjacent to the empty slot to slide it.
            </p>
          </div>

          {/* 3x3 Tile Grid */}
          <div className="w-full max-w-xs sm:max-w-sm mx-auto aspect-square p-3 sm:p-4 rounded-3xl bg-[#070A14] border border-white/10 shadow-inner grid grid-cols-3 gap-2.5 sm:gap-3">
            {board.map((val, idx) => {
              const isMovable = movableNeighbors.includes(idx);
              const isEmpty = val === null;

              if (isEmpty) {
                return (
                  <div
                    key={idx}
                    className="w-full h-full rounded-2xl border border-dashed border-white/10 bg-transparent flex items-center justify-center"
                  >
                    <span className="text-[10px] text-slate-600 font-mono select-none">EMPTY</span>
                  </div>
                );
              }

              return (
                <button
                  key={idx}
                  onClick={() => handleTileClick(idx)}
                  disabled={!isMovable}
                  className={`w-full h-full rounded-2xl border transition-all duration-200 flex flex-col items-center justify-center text-2xl sm:text-3xl font-black font-mono select-none shadow-md ${
                    isMovable
                      ? "bg-gradient-to-br from-[#121B35] to-[#0F172E] border-cyan-500/40 text-cyan-300 hover:border-cyan-400 hover:scale-105 hover:shadow-[0_0_20px_rgba(6,182,212,0.35)] cursor-pointer active:scale-95"
                      : "bg-[#090D1C] border-white/[0.06] text-slate-400 cursor-default"
                  }`}
                >
                  <span>{val}</span>
                  {isMovable && (
                    <span className="text-[9px] font-sans font-semibold text-cyan-400/80 mt-0.5 hidden sm:block">
                      SLIDE
                    </span>
                  )}
                </button>
              );
            })}
          </div>

          {/* Target Preview */}
          <div className="mt-8 flex items-center justify-center gap-3 text-xs text-slate-400">
            <span className="font-semibold text-slate-400">Goal Pattern:</span>
            <div className="inline-flex items-center gap-1 font-mono text-[11px] bg-[#070A14] px-3 py-1 rounded-xl border border-white/10 text-cyan-300">
              [ 1 2 3 &bull; 4 5 6 &bull; 7 8 _ ]
            </div>
          </div>
        </div>

        {/* Completion Modal */}
        <GameCompletionModal
          isOpen={isCompleted}
          gameTitle="Tile Puzzle"
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
