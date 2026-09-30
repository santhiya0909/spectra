import React from "react";
import { LucideIcon } from "lucide-react";

interface StatCardProps {
  title: string;
  value: string | number;
  subtitle?: string;
  icon: LucideIcon;
  color?: "brand" | "emerald" | "amber" | "rose" | "purple" | "cyan";
  trend?: string;
  sparkline?: React.ReactNode;
}

export const StatCard: React.FC<StatCardProps> = ({
  title,
  value,
  subtitle,
  icon: Icon,
  color = "brand",
  trend,
  sparkline,
}) => {
  const colorMap = {
    brand: {
      iconBg: "bg-indigo-500/15 text-indigo-400 border-indigo-500/30",
      glowHover: "hover:border-indigo-500/40 hover:shadow-[0_0_25px_-5px_rgba(99,102,241,0.25)]",
      trendBg: "bg-indigo-500/15 text-indigo-300 border-indigo-500/20",
    },
    emerald: {
      iconBg: "bg-emerald-500/15 text-emerald-400 border-emerald-500/30",
      glowHover: "hover:border-emerald-500/40 hover:shadow-[0_0_25px_-5px_rgba(16,185,129,0.25)]",
      trendBg: "bg-emerald-500/15 text-emerald-300 border-emerald-500/20",
    },
    amber: {
      iconBg: "bg-amber-500/15 text-amber-400 border-amber-500/30",
      glowHover: "hover:border-amber-500/40 hover:shadow-[0_0_25px_-5px_rgba(245,158,11,0.25)]",
      trendBg: "bg-amber-500/15 text-amber-300 border-amber-500/20",
    },
    rose: {
      iconBg: "bg-rose-500/15 text-rose-400 border-rose-500/30",
      glowHover: "hover:border-rose-500/40 hover:shadow-[0_0_25px_-5px_rgba(244,63,94,0.25)]",
      trendBg: "bg-rose-500/15 text-rose-300 border-rose-500/20",
    },
    purple: {
      iconBg: "bg-purple-500/15 text-purple-400 border-purple-500/30",
      glowHover: "hover:border-purple-500/40 hover:shadow-[0_0_25px_-5px_rgba(168,85,247,0.25)]",
      trendBg: "bg-purple-500/15 text-purple-300 border-purple-500/20",
    },
    cyan: {
      iconBg: "bg-cyan-500/15 text-cyan-400 border-cyan-500/30",
      glowHover: "hover:border-cyan-500/40 hover:shadow-[0_0_25px_-5px_rgba(6,182,212,0.25)]",
      trendBg: "bg-cyan-500/15 text-cyan-300 border-cyan-500/20",
    },
  };

  const currentTheme = colorMap[color] || colorMap.brand;

  return (
    <div
      className={`group relative flex flex-col justify-between rounded-3xl border border-slate-200/90 dark:border-white/[0.08] bg-white/85 dark:bg-[#0B1124]/80 p-5 backdrop-blur-xl shadow-sm dark:shadow-[0_8px_32px_0_rgba(0,0,0,0.37)] transition-all duration-300 hover:-translate-y-1 ${currentTheme.glowHover}`}
    >
      <div className="flex items-center justify-between">
        <p className="text-[11px] font-bold uppercase tracking-wider text-slate-500 dark:text-slate-400">
          {title}
        </p>
        <div
          className={`flex h-11 w-11 items-center justify-center rounded-2xl border shadow-inner transition-transform group-hover:scale-105 ${currentTheme.iconBg}`}
        >
          <Icon className="h-5 w-5" />
        </div>
      </div>

      <div className="mt-4">
        <div className="flex items-baseline gap-2.5">
          <span className="text-3xl font-black tracking-tight text-slate-900 dark:text-white">
            {value}
          </span>
          {trend && (
            <span
              className={`text-[11px] font-bold px-2 py-0.5 rounded-full border ${currentTheme.trendBg}`}
            >
              {trend}
            </span>
          )}
        </div>
        {subtitle && (
          <p className="mt-1 text-xs text-slate-500 dark:text-slate-400 font-medium">{subtitle}</p>
        )}
      </div>

      {sparkline && <div className="mt-3">{sparkline}</div>}
    </div>
  );
};
