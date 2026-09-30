"use client";

import React, { useEffect, useState } from "react";
import { useTheme } from "@/lib/theme";
import { Sun, Moon } from "lucide-react";

interface ThemeToggleProps {
  className?: string;
  showLabel?: boolean;
}

export const ThemeToggle: React.FC<ThemeToggleProps> = ({
  className = "",
  showLabel = false,
}) => {
  const { theme, toggleTheme } = useTheme();
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
  }, []);

  if (!mounted) {
    // Render placeholder with same dimensions to avoid layout shift
    return (
      <div className={`h-9 w-9 rounded-xl border border-white/10 bg-white/5 ${className}`} />
    );
  }

  const isDark = theme === "dark";

  return (
    <button
      onClick={toggleTheme}
      type="button"
      aria-label={isDark ? "Switch to Light Mode" : "Switch to Dark Mode"}
      title={isDark ? "Switch to Light Mode" : "Switch to Dark Mode"}
      className={`group relative flex items-center justify-center rounded-xl p-2 transition-all duration-300 ${
        isDark
          ? "bg-[#0B1124] hover:bg-[#121B35] text-amber-400 border border-white/10 hover:border-amber-400/40 shadow-[0_0_15px_rgba(245,158,11,0.15)]"
          : "bg-white hover:bg-slate-100 text-indigo-600 border border-slate-200/90 hover:border-indigo-500/40 shadow-sm"
      } ${className}`}
    >
      <div className="relative flex items-center justify-center w-5 h-5">
        {/* Sun Icon (shown when dark, click to switch to light) */}
        <Sun
          className={`absolute w-4 h-4 transition-all duration-500 ${
            isDark
              ? "rotate-0 scale-100 opacity-100 text-amber-400"
              : "-rotate-90 scale-0 opacity-0"
          }`}
        />

        {/* Moon Icon (shown when light, click to switch to dark) */}
        <Moon
          className={`absolute w-4 h-4 transition-all duration-500 ${
            isDark
              ? "rotate-90 scale-0 opacity-0"
              : "rotate-0 scale-100 opacity-100 text-indigo-600"
          }`}
        />
      </div>

      {showLabel && (
        <span className="ml-2 text-xs font-bold capitalize select-none text-slate-700 dark:text-slate-200">
          {isDark ? "Light" : "Dark"}
        </span>
      )}
    </button>
  );
};
