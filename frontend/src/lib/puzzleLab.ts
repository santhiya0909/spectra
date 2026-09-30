// Local storage and stats manager for SPECTRA Puzzle Lab

export interface GameStats {
  bestScore: number;
  bestTime: number; // in seconds
  bestMoves?: number;
  timesPlayed: number;
  lastPlayed?: string;
}

export interface PuzzleLabStats {
  totalSessions: number;
  totalXpEarned: number;
  currentStreak: number;
  lastActiveDate: string;
  games: {
    memory: GameStats;
    pattern: GameStats;
    word: GameStats;
    tiles: GameStats;
  };
}

const STORAGE_KEY = "spectra_puzzle_lab_stats_v1";

const DEFAULT_STATS: PuzzleLabStats = {
  totalSessions: 8,
  totalXpEarned: 160,
  currentStreak: 3,
  lastActiveDate: new Date().toISOString().split("T")[0],
  games: {
    memory: { bestScore: 920, bestTime: 54, bestMoves: 14, timesPlayed: 4 },
    pattern: { bestScore: 850, bestTime: 42, timesPlayed: 3 },
    word: { bestScore: 960, bestTime: 38, timesPlayed: 5 },
    tiles: { bestScore: 780, bestTime: 85, bestMoves: 26, timesPlayed: 2 },
  },
};

export function getPuzzleLabStats(): PuzzleLabStats {
  if (typeof window === "undefined") return DEFAULT_STATS;
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (!raw) {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(DEFAULT_STATS));
      return DEFAULT_STATS;
    }
    return JSON.parse(raw);
  } catch {
    return DEFAULT_STATS;
  }
}

export function recordGameCompletion(
  gameKey: "memory" | "pattern" | "word" | "tiles",
  score: number,
  timeSeconds: number,
  moves?: number
): { isNewBest: boolean; xpAwarded: number; updatedStats: PuzzleLabStats } {
  const stats = getPuzzleLabStats();
  const game = stats.games[gameKey] || { bestScore: 0, bestTime: 9999, timesPlayed: 0 };

  const isNewBest = score > game.bestScore;
  const bestScore = Math.max(game.bestScore, score);
  const bestTime = game.bestTime === 0 ? timeSeconds : Math.min(game.bestTime, timeSeconds);
  const bestMoves = moves
    ? game.bestMoves
      ? Math.min(game.bestMoves, moves)
      : moves
    : game.bestMoves;

  const xpAwarded = 20; // +20 XP casual reward
  stats.totalSessions += 1;
  stats.totalXpEarned += xpAwarded;

  // Streak calculation
  const today = new Date().toISOString().split("T")[0];
  if (stats.lastActiveDate !== today) {
    stats.currentStreak += 1;
    stats.lastActiveDate = today;
  }

  stats.games[gameKey] = {
    bestScore,
    bestTime,
    bestMoves,
    timesPlayed: game.timesPlayed + 1,
    lastPlayed: new Date().toISOString(),
  };

  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(stats));
  } catch (e) {
    console.error("Failed to save puzzle lab stats:", e);
  }

  return { isNewBest, xpAwarded, updatedStats: stats };
}

export const RELAXATION_QUOTES = [
  "Nice break! Your mind just got a quick cognitive workout.",
  "Great focus. Stepping back keeps your learning sharp and refreshed.",
  "Quick reset complete. Ready whenever you are.",
  "Neuroplasticity in action. Short breaks boost retention.",
  "Well played! Relaxed minds solve complex problems faster.",
];

export function getRandomRelaxationQuote(): string {
  return RELAXATION_QUOTES[Math.floor(Math.random() * RELAXATION_QUOTES.length)];
}
