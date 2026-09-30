import React from "react";

interface ProgressBarProps {
  progress: number;
  label?: string;
  size?: "sm" | "md" | "lg";
  color?: "brand" | "emerald" | "amber" | "rose" | "purple" | "cyan";
  showValue?: boolean;
}

export const ProgressBar: React.FC<ProgressBarProps> = ({
  progress,
  label,
  size = "md",
  color = "cyan",
  showValue = true,
}) => {
  const clamped = Math.max(0, Math.min(100, progress || 0));

  const heights = {
    sm: "h-1.5",
    md: "h-2.5",
    lg: "h-3.5",
  };

  const gradients = {
    brand: "bg-gradient-to-r from-indigo-500 to-indigo-400 shadow-[0_0_12px_rgba(99,102,241,0.5)]",
    cyan: "bg-gradient-to-r from-cyan-500 via-sky-400 to-blue-500 shadow-[0_0_12px_rgba(6,182,212,0.5)]",
    emerald: "bg-gradient-to-r from-emerald-500 to-teal-400 shadow-[0_0_12px_rgba(16,185,129,0.5)]",
    amber: "bg-gradient-to-r from-amber-500 to-yellow-400 shadow-[0_0_12px_rgba(245,158,11,0.5)]",
    rose: "bg-gradient-to-r from-rose-500 to-pink-500 shadow-[0_0_12px_rgba(244,63,94,0.5)]",
    purple: "bg-gradient-to-r from-purple-500 via-violet-400 to-indigo-500 shadow-[0_0_12px_rgba(168,85,247,0.5)]",
  };

  return (
    <div className="w-full">
      {(label || showValue) && (
        <div className="mb-1.5 flex items-center justify-between text-xs">
          {label && <span className="font-semibold text-slate-600 dark:text-slate-300">{label}</span>}
          {showValue && <span className="font-bold text-slate-900 dark:text-white font-mono">{clamped}%</span>}
        </div>
      )}
      <div className={`w-full overflow-hidden rounded-full bg-slate-200 dark:bg-slate-800/80 border border-slate-300/50 dark:border-white/5 ${heights[size]}`}>
        <div
          className={`${gradients[color]} ${heights[size]} rounded-full transition-all duration-700 ease-out`}
          style={{ width: `${clamped}%` }}
        />
      </div>
    </div>
  );
};
