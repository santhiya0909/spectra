"use client";

import React, { useState } from "react";
import Link from "next/link";
import { useQuery } from "@tanstack/react-query";
import { subjectService, Subject } from "@/services/subject.service";
import { RoleLayout } from "@/components/layout/RoleLayout";
import { GlassCard } from "@/components/common/GlassCard";
import {
  BookOpen,
  ArrowRight,
  AlertCircle,
  RefreshCw,
  Search,
  Sparkles,
  PlayCircle,
  Code2,
  Terminal,
  Calculator,
  FlaskConical,
  Bot,
  Network,
  Cpu,
  Globe,
  GraduationCap,
  CheckCircle2,
  Layers,
  Database
} from "lucide-react";

export default function StudentSubjectsPage() {
  const [search, setSearch] = useState("");
  const [categoryFilter, setCategoryFilter] = useState("ALL");
  const [difficultyFilter, setDifficultyFilter] = useState("ALL");

  const { data, isLoading, error, refetch, isFetching } = useQuery<Subject[]>({
    queryKey: ["subjects", search, categoryFilter, difficultyFilter],
    queryFn: () =>
      subjectService.getSubjects({
        search: search || undefined,
        category: categoryFilter !== "ALL" ? categoryFilter : undefined,
        difficulty: difficultyFilter !== "ALL" ? difficultyFilter : undefined,
      }),
  });

  const rawData = data as any;
  const subjects: Subject[] = Array.isArray(rawData)
    ? rawData
    : Array.isArray(rawData?.subjects)
    ? rawData.subjects
    : Array.isArray(rawData?.data)
    ? rawData.data
    : [];

  const getSubjectIcon = (code: string, category?: string) => {
    switch (code) {
      case "JAVA":
        return <Code2 className="w-6 h-6 text-amber-400" />;
      case "PYTHON":
        return <Terminal className="w-6 h-6 text-cyan-400" />;
      case "MATH":
      case "MATH-201":
        return <Calculator className="w-6 h-6 text-cyan-400" />;
      case "CHEM":
        return <FlaskConical className="w-6 h-6 text-purple-400" />;
      case "AI":
        return <Bot className="w-6 h-6 text-rose-400" />;
      case "DSA":
        return <Network className="w-6 h-6 text-indigo-400" />;
      case "DBMS":
        return <Database className="w-6 h-6 text-cyan-400" />;
      case "ML":
        return <Cpu className="w-6 h-6 text-cyan-400" />;
      case "WEB":
        return <Globe className="w-6 h-6 text-amber-400" />;
      default:
        return <BookOpen className="w-6 h-6 text-cyan-400" />;
    }
  };

  return (
    <RoleLayout allowedRoles={["STUDENT", "ADMIN"]}>
      <div className="space-y-6 pb-14">
        {/* Header Banner */}
        <div className="relative overflow-hidden rounded-3xl bg-gradient-to-r from-[#0B1530] via-[#10103A] to-[#140C2C] p-6 sm:p-8 text-white shadow-xl shadow-cyan-950/20 border border-white/10">
          <div className="absolute -top-16 -right-16 w-72 h-72 bg-cyan-500/15 rounded-full blur-[100px] pointer-events-none" />
          <div className="absolute -bottom-16 -left-16 w-72 h-72 bg-purple-500/15 rounded-full blur-[100px] pointer-events-none" />

          <div className="relative z-10 flex flex-col sm:flex-row sm:items-center justify-between gap-4">
            <div>
              <div className="inline-flex items-center gap-1.5 rounded-full bg-cyan-500/15 px-3 py-1 text-xs font-bold text-cyan-300 border border-cyan-400/30 shadow-[0_0_12px_rgba(6,182,212,0.2)] mb-3">
                <Sparkles className="h-3.5 w-3.5 text-cyan-300" />
                <span>8 Structured Academic Tracks &bull; Integrated Video Remediation</span>
              </div>
              <h1 className="text-2xl sm:text-3xl font-black tracking-tight">Active Curriculum Subjects</h1>
              <p className="mt-1 text-sm text-slate-300 max-w-xl font-normal leading-relaxed">
                Master computer science, discrete mathematics, relational databases, and algorithms through sequential lessons and interactive concept puzzles.
              </p>
            </div>

            <button
              onClick={() => refetch()}
              disabled={isFetching}
              className="inline-flex items-center gap-1.5 rounded-xl bg-white/[0.05] hover:bg-white/10 border border-white/10 px-4 py-2.5 text-xs font-bold text-slate-300 hover:text-white shadow-sm backdrop-blur-sm transition disabled:opacity-50 self-start sm:self-center"
            >
              <RefreshCw className={`h-3.5 w-3.5 ${isFetching ? "animate-spin text-cyan-400" : ""}`} />
              <span>Refresh</span>
            </button>
          </div>
        </div>

        {/* Search & Filter Toolbar */}
        <div className="flex flex-col md:flex-row items-stretch md:items-center justify-between gap-3 rounded-2xl border border-slate-200/90 dark:border-white/[0.08] bg-white/90 dark:bg-[#0B1124]/90 p-3.5 backdrop-blur-xl shadow-lg">
          <div className="relative flex-1">
            <Search className="absolute left-3.5 top-1/2 -translate-y-1/2 h-4 w-4 text-slate-400" />
            <input
              type="text"
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              placeholder="Search by subject name, code, or description..."
              className="w-full rounded-xl border border-slate-200 dark:border-white/10 bg-slate-50 dark:bg-[#060913] pl-10 pr-4 py-2 text-xs font-medium text-slate-900 dark:text-white placeholder:text-slate-400 dark:placeholder:text-slate-500 focus:bg-white dark:focus:bg-[#080D1F] focus:border-cyan-500 focus:outline-none focus:ring-1 focus:ring-cyan-500/20 transition"
            />
          </div>

          <div className="flex items-center gap-2">
            <select
              value={difficultyFilter}
              onChange={(e) => setDifficultyFilter(e.target.value)}
              className="rounded-xl border border-slate-200 dark:border-white/10 bg-slate-50 dark:bg-[#060913] px-3 py-2 text-xs font-semibold text-slate-700 dark:text-slate-300 focus:border-cyan-500 focus:outline-none"
            >
              <option value="ALL">All Difficulties</option>
              <option value="BEGINNER">Beginner</option>
              <option value="INTERMEDIATE">Intermediate</option>
              <option value="ADVANCED">Advanced</option>
            </select>
          </div>
        </div>

        {/* Content Grid */}
        {isLoading ? (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 animate-pulse">
            {[1, 2, 3, 4, 5, 6].map((i) => (
              <div key={i} className="h-64 bg-slate-800/40 rounded-3xl border border-white/5" />
            ))}
          </div>
        ) : error ? (
          <GlassCard className="p-8 text-center border-rose-500/30 bg-rose-950/20 text-rose-300">
            <AlertCircle className="h-9 w-9 mx-auto mb-2 text-rose-400" />
            <h3 className="font-bold text-sm text-white">Failed to load subjects</h3>
            <p className="text-xs text-rose-300 mt-1">{(error as any)?.message || "Please check your network and try again."}</p>
          </GlassCard>
        ) : subjects.length === 0 ? (
          <GlassCard className="p-12 text-center">
            <GraduationCap className="h-10 w-10 text-slate-500 mx-auto mb-2" />
            <h3 className="text-base font-bold text-slate-900 dark:text-white">No subjects found</h3>
            <p className="text-xs text-slate-500 dark:text-slate-400 mt-1">Try adjusting your search terms or filters.</p>
          </GlassCard>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {subjects.map((subj) => {
              const totalLessons = subj.lessons_count || 10;
              const completedLessons = subj.completed_lessons_count || 0;
              const progressPct = subj.progress_percentage || Math.round((completedLessons / totalLessons) * 100);

              return (
                <div
                  key={subj.id}
                  className="group relative flex flex-col justify-between rounded-3xl border border-slate-200/90 dark:border-white/[0.08] bg-white/85 dark:bg-[#0B1124]/85 p-6 backdrop-blur-xl shadow-[0_8px_30px_rgb(0,0,0,0.04)] dark:shadow-lg hover:border-cyan-500/40 hover:shadow-[0_0_25px_-5px_rgba(6,182,212,0.2)] transition-all duration-300 hover:-translate-y-1"
                >
                  <div>
                    {/* Top Row: Icon + Code + Difficulty */}
                    <div className="flex items-center justify-between gap-2 mb-4">
                      <div className="w-12 h-12 rounded-2xl bg-slate-100 dark:bg-white/[0.04] border border-slate-200 dark:border-white/10 flex items-center justify-center shadow-inner group-hover:scale-105 transition-transform">
                        {getSubjectIcon(subj.code, subj.category)}
                      </div>
                      <div className="flex items-center gap-2">
                        <span className="text-[10px] font-extrabold uppercase px-2.5 py-1 rounded-lg bg-cyan-500/10 dark:bg-cyan-950/40 text-cyan-700 dark:text-cyan-300 border border-cyan-500/30 font-mono">
                          {subj.code}
                        </span>
                        <span className={`text-[10px] font-extrabold uppercase px-2 py-0.5 rounded-md border ${
                          subj.difficulty_level === "BEGINNER"
                            ? "bg-emerald-500/15 text-emerald-700 dark:text-emerald-300 border-emerald-500/30"
                            : subj.difficulty_level === "ADVANCED"
                            ? "bg-rose-500/15 text-rose-700 dark:text-rose-300 border-rose-500/30"
                            : "bg-amber-500/15 text-amber-700 dark:text-amber-300 border-amber-500/30"
                        }`}>
                          {subj.difficulty_level || "ALL LEVELS"}
                        </span>
                      </div>
                    </div>

                    {/* Subject Name & Description */}
                    <h3 className="text-base font-bold text-slate-900 dark:text-white group-hover:text-cyan-600 dark:group-hover:text-cyan-300 transition-colors">
                      {subj.name}
                    </h3>
                    <p className="mt-2 text-xs leading-relaxed text-slate-600 dark:text-slate-400 line-clamp-2">
                      {subj.description}
                    </p>

                    {/* Badges: Lessons & Topics */}
                    <div className="mt-4 flex flex-wrap items-center gap-2">
                      <span className="inline-flex items-center gap-1 text-[11px] font-semibold px-2.5 py-1 rounded-lg bg-slate-100 dark:bg-white/[0.03] border border-slate-200 dark:border-white/5 text-slate-700 dark:text-slate-300">
                        <BookOpen className="w-3.5 h-3.5 text-cyan-500 dark:text-cyan-400" />
                        {totalLessons} Lessons
                      </span>
                      <span className="inline-flex items-center gap-1 text-[11px] font-semibold px-2.5 py-1 rounded-lg bg-slate-100 dark:bg-white/[0.03] border border-slate-200 dark:border-white/5 text-slate-700 dark:text-slate-300">
                        <Layers className="w-3.5 h-3.5 text-purple-500 dark:text-purple-400" />
                        {subj.topics?.length || 2} Core Topics
                      </span>
                    </div>

                    {/* Current Lesson Indicator */}
                    {subj.current_lesson && (
                      <div className="mt-3 p-2.5 rounded-xl bg-cyan-500/10 dark:bg-cyan-950/20 border border-cyan-500/20 text-xs">
                        <span className="text-[10px] uppercase font-bold text-cyan-700 dark:text-cyan-300 tracking-wider block">
                          Current Lesson:
                        </span>
                        <span className="font-semibold text-slate-900 dark:text-white line-clamp-1">
                          {subj.current_lesson.title}
                        </span>
                      </div>
                    )}
                  </div>

                  {/* Progress & Continue Learning Footer */}
                  <div className="mt-6 pt-4 border-t border-slate-200 dark:border-white/[0.06] space-y-3">
                    <div className="space-y-1">
                      <div className="flex items-center justify-between text-xs font-semibold text-slate-500 dark:text-slate-400">
                        <span>{completedLessons} of {totalLessons} completed</span>
                        <span className="text-cyan-600 dark:text-cyan-400 font-bold font-mono">{progressPct}%</span>
                      </div>
                      <div className="w-full h-1.5 bg-slate-200 dark:bg-slate-800 rounded-full overflow-hidden border border-slate-300/60 dark:border-white/5">
                        <div
                          className="h-full bg-gradient-to-r from-cyan-500 to-indigo-500 rounded-full shadow-[0_0_10px_#06b6d4] transition-all duration-500"
                          style={{ width: `${progressPct}%` }}
                        />
                      </div>
                    </div>

                    <div className="flex items-center gap-2 pt-1">
                      <Link
                        href={`/student/subjects/${subj.id}`}
                        className="flex-1 py-2.5 px-4 rounded-xl bg-slate-100 hover:bg-slate-200 dark:bg-white/[0.04] dark:hover:bg-white/[0.08] border border-slate-200 dark:border-white/10 text-slate-700 hover:text-slate-900 dark:text-slate-300 dark:hover:text-white text-xs font-bold transition-all text-center flex items-center justify-center gap-1.5"
                      >
                        <span>Curriculum</span>
                        <ArrowRight className="w-3.5 h-3.5" />
                      </Link>

                      <Link
                        href={
                          subj.current_lesson
                            ? `/student/lessons/${subj.current_lesson.id}`
                            : `/student/subjects/${subj.id}`
                        }
                        className="flex-1 py-2.5 px-4 rounded-xl bg-cyan-500 hover:bg-cyan-400 text-black text-xs font-black shadow-[0_0_15px_rgba(6,182,212,0.3)] transition-all text-center flex items-center justify-center gap-1.5"
                      >
                        <PlayCircle className="w-3.5 h-3.5 text-black" />
                        <span>{completedLessons > 0 ? "Continue" : "Start"}</span>
                      </Link>
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        )}
      </div>
    </RoleLayout>
  );
}
