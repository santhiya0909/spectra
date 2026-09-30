import type { Config } from "tailwindcss";

const config: Config = {
  darkMode: "class",
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        brand: {
          50: "#eef2ff",
          100: "#e0e7ff",
          200: "#c7d2fe",
          300: "#a5b4fc",
          400: "#818cf8",
          500: "#6366f1",
          600: "#4f46e5",
          700: "#4338ca",
          800: "#3730a3",
          900: "#312e81",
        },
        secondary: {
          400: "#a78bfa",
          500: "#8b5cf6",
          600: "#7c3aed",
          700: "#6d28d9",
        },
        accent: {
          400: "#22d3ee",
          500: "#06b6d4",
          600: "#0891b2",
        },
        cosmic: {
          950: "#050811",
          900: "#080C1A",
          850: "#0B1124",
          800: "#0F172E",
          750: "#141E3C",
          700: "#1C2950",
          600: "#27396D",
        },
      },
      boxShadow: {
        "glow-cyan": "0 0 25px -3px rgba(6, 182, 212, 0.35)",
        "glow-purple": "0 0 25px -3px rgba(139, 92, 246, 0.35)",
        "glow-amber": "0 0 25px -3px rgba(245, 158, 11, 0.35)",
        "glow-emerald": "0 0 25px -3px rgba(16, 185, 129, 0.35)",
        "glass": "0 8px 32px 0 rgba(0, 0, 0, 0.45)",
        "glass-sm": "0 4px 16px 0 rgba(0, 0, 0, 0.3)",
      },
      backgroundImage: {
        "radial-gradient": "radial-gradient(circle at 50% 0%, var(--tw-gradient-stops))",
      },
    },
  },
  plugins: [],
};
export default config;
