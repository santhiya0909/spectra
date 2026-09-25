import React from "react";

interface ProgressBarProps {
  progress: number;
  label?: string;
  size?: "sm" | "md" | "lg";
  color?: "brand" | "emerald" | "amber" | "rose" | "purple";
  showValue?: boolean;
}

export const ProgressBar: React.FC<ProgressBarProps> = ({
  progress,
  label,
  size = "md",
  color = "brand",
  showValue = true,
}) => {
  const clamped = Math.max(0, Math.min(100, progress || 0));

  const heights = {
    sm: "h-1.5",
    md: "h-2.5",
    lg: "h-4",
  };

  const colors = {
    brand: "bg-brand-600",
    emerald: "bg-emerald-500",
    amber: "bg-amber-500",
    rose: "bg-rose-500",
    purple: "bg-purple-600",
  };

  return (
    <div className="w-full">
      {(label || showValue) && (
        <div className="mb-1.5 flex items-center justify-between text-xs">
          {label && <span className="font-medium text-slate-700">{label}</span>}
          {showValue && <span className="font-semibold text-slate-900">{clamped}%</span>}
        </div>
      )}
      <div className={`w-full overflow-hidden rounded-full bg-slate-100 ${heights[size]}`}>
        <div
          className={`${colors[color]} ${heights[size]} rounded-full transition-all duration-500 ease-out`}
          style={{ width: `${clamped}%` }}
        />
      </div>
    </div>
  );
};
