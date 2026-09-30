import React from "react";

interface BadgeProps {
  children: React.ReactNode;
  variant?: "brand" | "emerald" | "amber" | "rose" | "purple" | "slate" | "cyan";
  size?: "sm" | "md";
}

export const Badge: React.FC<BadgeProps> = ({
  children,
  variant = "cyan",
  size = "md",
}) => {
  const variantStyles = {
    brand: "bg-indigo-500/15 text-indigo-700 dark:text-indigo-300 border-indigo-500/30",
    emerald: "bg-emerald-500/15 text-emerald-700 dark:text-emerald-300 border-emerald-500/30",
    amber: "bg-amber-500/15 text-amber-700 dark:text-amber-300 border-amber-500/30",
    rose: "bg-rose-500/15 text-rose-700 dark:text-rose-300 border-rose-500/30",
    purple: "bg-purple-500/15 text-purple-700 dark:text-purple-300 border-purple-500/30",
    slate: "bg-slate-200 dark:bg-slate-800/60 text-slate-700 dark:text-slate-300 border-slate-300 dark:border-slate-700/60",
    cyan: "bg-cyan-500/15 text-cyan-700 dark:text-cyan-300 border-cyan-500/30",
  };

  const sizeStyles = {
    sm: "px-2 py-0.5 text-[10px]",
    md: "px-2.5 py-1 text-xs",
  };

  return (
    <span
      className={`inline-flex items-center font-semibold rounded-full border backdrop-blur-md ${variantStyles[variant]} ${sizeStyles[size]}`}
    >
      {children}
    </span>
  );
};
