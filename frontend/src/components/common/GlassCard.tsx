import React from "react";
import clsx from "clsx";

interface GlassCardProps extends React.HTMLAttributes<HTMLDivElement> {
  children: React.ReactNode;
  className?: string;
  glow?: "cyan" | "purple" | "amber" | "emerald" | "none";
  interactive?: boolean;
  gradientBorder?: boolean;
}

export const GlassCard: React.FC<GlassCardProps> = ({
  children,
  className,
  glow = "none",
  interactive = false,
  gradientBorder = false,
  ...props
}) => {
  const glowStyles = {
    none: "",
    cyan: "hover:border-cyan-500/40 hover:shadow-[0_0_30px_-5px_rgba(6,182,212,0.25)]",
    purple: "hover:border-purple-500/40 hover:shadow-[0_0_30px_-5px_rgba(139,92,246,0.25)]",
    amber: "hover:border-amber-500/40 hover:shadow-[0_0_30px_-5px_rgba(245,158,11,0.25)]",
    emerald: "hover:border-emerald-500/40 hover:shadow-[0_0_30px_-5px_rgba(16,185,129,0.25)]",
  };

  return (
    <div
      className={clsx(
        "relative rounded-3xl backdrop-blur-xl transition-all duration-300",
        "bg-white/85 dark:bg-[#0B1124]/75 border border-slate-200/90 dark:border-white/[0.08] text-slate-900 dark:text-slate-100 shadow-[0_4px_20px_0_rgba(0,0,0,0.06)] dark:shadow-[0_8px_32px_0_rgba(0,0,0,0.37)]",
        interactive && "cursor-pointer hover:-translate-y-1",
        glowStyles[glow],
        gradientBorder && "before:absolute before:inset-0 before:-z-10 before:rounded-3xl before:p-[1px] before:bg-gradient-to-r before:from-cyan-500/20 before:via-purple-500/20 before:to-pink-500/20",
        className
      )}
      {...props}
    >
      {children}
    </div>
  );
};
