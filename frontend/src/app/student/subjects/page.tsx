"use client";

import React, { useState, useMemo } from "react";
import Link from "next/link";
import { useQuery } from "@tanstack/react-query";
import { subjectService, Subject } from "@/services/subject.service";
import { RoleLayout } from "@/components/layout/RoleLayout";
import { ProgressBar } from "@/components/common/ProgressBar";
import { Badge } from "@/components/common/Badge";
import {
  BookOpen,
  ArrowRight,
  AlertCircle,
  RefreshCw,
  GraduationCap,
  Search,
  Layers,
  Sparkles,
  Filter,
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

  const categories = [
    { label: "All Categories", value: "ALL" },
    { label: "Programming", value: "PROGRAMMING" },
    { label: "Data Engineering", value: "DATA_ENGINEERING" },
    { label: "Mathematics", value: "MATHEMATICS" },
    { label: "Business", value: "BUSINESS" },
  ];

  const difficulties = [
    { label: "All Levels", value: "ALL" },
    { label: "Beginner", value: "BEGINNER" },
    { label: "Intermediate", value: "INTERMEDIATE" },
    { label: "Advanced", value: "ADVANCED" },
  ];

  return (
    <RoleLayout allowedRoles={["STUDENT", "ADMIN"]}>
      <div className="space-y-6">
        {/* Header Banner */}
        <div className="rounded-3xl bg-gradient-to-r from-brand-600 via-brand-700 to-indigo-800 p-6 sm:p-8 text-white shadow-md">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
            <div>
              <div className="inline-flex items-center gap-1.5 rounded-full bg-white/10 px-3 py-1 text-xs font-semibold backdrop-blur-sm mb-3">
                <Sparkles className="h-3.5 w-3.5 text-brand-200" />
                <span>Structured Academic Curriculum</span>
              </div>
              <h1 className="text-2xl sm:text-3xl font-extrabold tracking-tight">Curriculum Subjects</h1>
              <p className="mt-1 text-sm text-brand-100 max-w-xl">
                Explore structured modules, comprehensive topics, and verified industry study resources tailored to master key concepts.
              </p>
            </div>

            <button
              onClick={() => refetch()}
              disabled={isFetching}
              className="inline-flex items-center gap-1.5 rounded-xl bg-white/10 hover:bg-white/20 border border-white/20 px-4 py-2.5 text-xs font-bold text-white shadow-sm backdrop-blur-sm transition disabled:opacity-50 self-start sm:self-center"
            >
              <RefreshCw className={`h-3.5 w-3.5 ${isFetching ? "animate-spin" : ""}`} />
              <span>Refresh</span>
            </button>
          </div>
        </div>

        {/* Search & Filter Toolbar */}
        <div className="flex flex-col md:flex-row items-stretch md:items-center justify-between gap-3 rounded-2xl border border-slate-200 bg-white p-3.5 shadow-sm">
          <div className="relative flex-1">
            <Search className="absolute left-3.5 top-1/2 -translate-y-1/2 h-4 w-4 text-slate-400" />
            <input
              type="text"
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              placeholder="Search subjects by name, code, or description..."
              className="w-full rounded-xl border border-slate-200 bg-slate-50 pl-10 pr-4 py-2 text-xs font-medium text-slate-900 placeholder:text-slate-400 focus:bg-white focus:border-brand-500 focus:outline-none focus:ring-1 focus:ring-brand-500 transition"
            />
          </div>

          <div className="flex items-center gap-2">
            <select
              value={categoryFilter}
              onChange={(e) => setCategoryFilter(e.target.value)}
              className="rounded-xl border border-slate-200 bg-slate-50 px-3 py-2 text-xs font-semibold text-slate-700 focus:bg-white focus:border-brand-500 focus:outline-none"
            >
              {categories.map((c) => (
                <option key={c.value} value={c.value}>
                  {c.label}
                </option>
              ))}
            </select>

            <select
              value={difficultyFilter}
              onChange={(e) => setDifficultyFilter(e.target.value)}
              className="rounded-xl border border-slate-200 bg-slate-50 px-3 py-2 text-xs font-semibold text-slate-700 focus:bg-white focus:border-brand-500 focus:outline-none"
            >
              {difficulties.map((d) => (
                <option key={d.value} value={d.value}>
                  {d.label}
                </option>
              ))}
            </select>
          </div>
        </div>

        {/* Content State */}
        {isLoading ? (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6 animate-pulse">
            {[1, 2, 3, 4].map((i) => (
              <div key={i} className="h-56 bg-slate-200 rounded-3xl" />
            ))}
          </div>
        ) : error ? (
          <div className="rounded-3xl border border-rose-200 bg-rose-50 p-8 text-center text-rose-700">
            <AlertCircle className="h-9 w-9 mx-auto mb-2 text-rose-600" />
            <h3 className="font-bold text-sm">Failed to load subjects</h3>
            <p className="text-xs text-rose-600 mt-1">{(error as any)?.message || "Please check your network and try again."}</p>
            <button
              onClick={() => refetch()}
              className="mt-4 inline-flex items-center gap-1.5 rounded-xl bg-rose-600 px-4 py-2 text-xs font-semibold text-white shadow hover:bg-rose-700"
            >
              <RefreshCw className="h-3.5 w-3.5" />
              <span>Retry</span>
            </button>
          </div>
        ) : subjects.length === 0 ? (
          <div className="rounded-3xl border border-slate-200 bg-white p-12 text-center shadow-sm">
            <div className="mx-auto flex h-14 w-14 items-center justify-center rounded-2xl bg-brand-50 text-brand-600 border border-brand-200 mb-4">
              <GraduationCap className="h-7 w-7" />
            </div>
            <h3 className="text-base font-bold text-slate-900">No subjects found</h3>
            <p className="text-xs text-slate-500 max-w-md mx-auto mt-1.5">
              {search || categoryFilter !== "ALL" || difficultyFilter !== "ALL"
                ? "No curriculum subjects matched your search or filters. Try adjusting your criteria."
                : "Default curriculum subjects are being prepared for your account. Click refresh to load."}
            </p>
            {(search || categoryFilter !== "ALL" || difficultyFilter !== "ALL") && (
              <button
                onClick={() => {
                  setSearch("");
                  setCategoryFilter("ALL");
                  setDifficultyFilter("ALL");
                }}
                className="mt-4 inline-flex items-center gap-1.5 rounded-xl bg-slate-100 hover:bg-slate-200 text-slate-700 px-4 py-2 text-xs font-semibold transition"
              >
                Clear Filters
              </button>
            )}
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {subjects.map((subj) => (
              <div
                key={subj.id}
                className="group relative flex flex-col justify-between rounded-3xl border border-slate-200 bg-white p-6 sm:p-7 shadow-sm transition-all duration-200 hover:shadow-md hover:border-brand-200"
              >
                <div>
                  <div className="flex items-center justify-between gap-2 mb-3">
                    <span className="rounded-lg bg-brand-50 px-2.5 py-1 text-xs font-bold text-brand-700 uppercase border border-brand-100">
                      {subj.code}
                    </span>
                    <div className="flex items-center gap-1.5">
                      {subj.category && (
                        <span className="rounded-md bg-slate-100 px-2 py-0.5 text-[10px] font-semibold text-slate-600 uppercase">
                          {subj.category.replace(/_/g, " ")}
                        </span>
                      )}
                      <Badge
                        variant={
                          subj.difficulty_level === "BEGINNER"
                            ? "emerald"
                            : subj.difficulty_level === "INTERMEDIATE"
                            ? "brand"
                            : "purple"
                        }
                        size="sm"
                      >
                        {subj.difficulty_level || "ALL LEVELS"}
                      </Badge>
                    </div>
                  </div>

                  <h3 className="text-xl font-bold text-slate-900 group-hover:text-brand-600 transition-colors">
                    {subj.name}
                  </h3>

                  <p className="mt-2 text-xs leading-relaxed text-slate-600 line-clamp-2">
                    {subj.description}
                  </p>

                  <div className="mt-4 flex flex-wrap items-center gap-4 text-xs font-semibold text-slate-500 border-t border-slate-100 pt-3">
                    <span className="flex items-center gap-1 text-slate-700">
                      <BookOpen className="h-3.5 w-3.5 text-brand-600" />
                      {subj.lessons_count} Modules / Lessons
                    </span>
                    <span className="flex items-center gap-1 text-slate-700">
                      <Layers className="h-3.5 w-3.5 text-indigo-600" />
                      {subj.topics?.length || 0} Core Topics
                    </span>
                  </div>

                  {subj.topics && subj.topics.length > 0 && (
                    <div className="mt-3 flex flex-wrap gap-1.5">
                      {subj.topics.slice(0, 3).map((t) => (
                        <span
                          key={t.id}
                          className="rounded-md bg-slate-50 border border-slate-200/60 px-2 py-0.5 text-[11px] font-medium text-slate-600"
                        >
                          {t.name}
                        </span>
                      ))}
                      {subj.topics.length > 3 && (
                        <span className="rounded-md bg-slate-50 border border-slate-200/60 px-2 py-0.5 text-[11px] font-medium text-slate-400">
                          +{subj.topics.length - 3} more
                        </span>
                      )}
                    </div>
                  )}
                </div>

                <div className="mt-6 pt-4 border-t border-slate-100 flex flex-col gap-3">
                  <ProgressBar
                    progress={subj.progress_percentage || 0}
                    label="Completion Progress"
                    color="brand"
                  />

                  <Link
                    href={`/student/subjects/${subj.id}`}
                    className="mt-1 flex items-center justify-between rounded-xl bg-slate-50 group-hover:bg-brand-50 border border-slate-200 group-hover:border-brand-200 px-4 py-2.5 text-xs font-bold text-slate-700 group-hover:text-brand-700 transition"
                  >
                    <span>View Structured Curriculum</span>
                    <ArrowRight className="h-4 w-4 transition-transform group-hover:translate-x-1" />
                  </Link>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </RoleLayout>
  );
}
