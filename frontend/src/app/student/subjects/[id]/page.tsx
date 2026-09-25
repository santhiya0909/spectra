"use client";

import React from "react";
import Link from "next/link";
import { useParams } from "next/navigation";
import { useQuery } from "@tanstack/react-query";
import { subjectService, Subject, Lesson } from "@/services/subject.service";
import { RoleLayout } from "@/components/layout/RoleLayout";
import { Badge } from "@/components/common/Badge";
import { ProgressBar } from "@/components/common/ProgressBar";
import {
  ArrowLeft,
  BookOpen,
  CheckCircle2,
  Clock,
  HelpCircle,
  PlayCircle,
  AlertCircle,
  RefreshCw,
  Layers,
  ExternalLink,
  ChevronRight,
  Sparkles,
} from "lucide-react";

export default function SubjectDetailPage() {
  const params = useParams();
  const subjectId = Number(params?.id);

  const {
    data: subject,
    isLoading: subjectLoading,
    error: subjectError,
    refetch: refetchSubject,
  } = useQuery<Subject>({
    queryKey: ["subject", subjectId],
    queryFn: () => subjectService.getSubject(subjectId),
    enabled: !!subjectId,
  });

  const lessons: Lesson[] = subject?.lessons || [];

  return (
    <RoleLayout allowedRoles={["STUDENT", "ADMIN"]}>
      <div className="space-y-6">
        {/* Navigation Breadcrumb */}
        <Link
          href="/student/subjects"
          className="inline-flex items-center gap-1.5 text-xs font-semibold text-slate-500 hover:text-slate-800 transition"
        >
          <ArrowLeft className="h-4 w-4" />
          <span>Back to Subjects</span>
        </Link>

        {/* Subject Header Banner */}
        {subjectLoading ? (
          <div className="h-44 bg-slate-200 rounded-3xl animate-pulse" />
        ) : subjectError ? (
          <div className="rounded-3xl border border-rose-200 bg-rose-50 p-6 text-center text-rose-700">
            <AlertCircle className="h-8 w-8 mx-auto mb-2 text-rose-600" />
            <h3 className="font-bold text-sm">Failed to load subject details</h3>
            <p className="text-xs text-rose-600 mt-1">{(subjectError as any)?.message || "Please try again."}</p>
            <button
              onClick={() => refetchSubject()}
              className="mt-4 inline-flex items-center gap-1.5 rounded-xl bg-rose-600 px-4 py-2 text-xs font-semibold text-white shadow hover:bg-rose-700"
            >
              <RefreshCw className="h-3.5 w-3.5" />
              <span>Retry</span>
            </button>
          </div>
        ) : subject ? (
          <div className="rounded-3xl border border-slate-200 bg-white p-6 sm:p-8 shadow-sm">
            <div className="flex flex-col md:flex-row md:items-center justify-between gap-6">
              <div className="space-y-2">
                <div className="flex flex-wrap items-center gap-2">
                  <span className="rounded-lg bg-brand-50 px-2.5 py-1 text-xs font-bold text-brand-700 uppercase border border-brand-100">
                    {subject.code}
                  </span>
                  {subject.category && (
                    <span className="rounded-md bg-slate-100 px-2 py-0.5 text-[11px] font-semibold text-slate-600 uppercase">
                      {subject.category.replace(/_/g, " ")}
                    </span>
                  )}
                  <Badge
                    variant={
                      subject.difficulty_level === "BEGINNER"
                        ? "emerald"
                        : subject.difficulty_level === "INTERMEDIATE"
                        ? "brand"
                        : "purple"
                    }
                    size="sm"
                  >
                    {subject.difficulty_level || "ALL LEVELS"}
                  </Badge>
                </div>

                <h1 className="text-2xl sm:text-3xl font-extrabold text-slate-900 tracking-tight">
                  {subject.name}
                </h1>
                <p className="text-xs sm:text-sm text-slate-600 max-w-2xl leading-relaxed">
                  {subject.description}
                </p>

                <div className="flex items-center gap-4 text-xs font-semibold text-slate-500 pt-2">
                  <span className="flex items-center gap-1.5">
                    <BookOpen className="h-3.5 w-3.5 text-brand-600" />
                    {lessons.length} Modules
                  </span>
                  <span className="flex items-center gap-1.5">
                    <Layers className="h-3.5 w-3.5 text-indigo-600" />
                    {subject.topics?.length || 0} Topics
                  </span>
                </div>
              </div>

              <div className="w-full md:w-72 rounded-2xl bg-slate-50 border border-slate-200 p-4">
                <ProgressBar
                  progress={subject.progress_percentage || 0}
                  label="Curriculum Mastery"
                  color="brand"
                />
                <div className="mt-3 flex items-center justify-between text-[11px] font-semibold text-slate-500">
                  <span>
                    {lessons.filter((l) => l.status === "COMPLETED").length} of {lessons.length} Completed
                  </span>
                  <span>{subject.progress_percentage || 0}%</span>
                </div>
              </div>
            </div>
          </div>
        ) : null}

        {/* Modules & Deep Lesson Curriculum */}
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <div>
              <h2 className="text-lg font-bold text-slate-900">Learning Roadmap & Modules</h2>
              <p className="text-xs text-slate-500">
                Complete modules sequentially to build strong conceptual fundamentals.
              </p>
            </div>
            <span className="rounded-full bg-slate-100 px-3 py-1 text-xs font-bold text-slate-600">
              {lessons.length} Modules Available
            </span>
          </div>

          {lessons.length === 0 ? (
            <div className="rounded-3xl border border-slate-200 bg-white p-12 text-center shadow-sm">
              <BookOpen className="h-10 w-10 mx-auto text-slate-300 mb-3" />
              <h3 className="text-sm font-bold text-slate-900">No modules published yet</h3>
              <p className="text-xs text-slate-500 mt-1">
                Lessons and resources for this subject are currently being prepared.
              </p>
            </div>
          ) : (
            <div className="space-y-4">
              {lessons.map((lesson, idx) => {
                const isCompleted = lesson.status === "COMPLETED";
                const isInProgress = lesson.status === "IN_PROGRESS";
                const resourceCount = lesson.study_resources?.length || 0;
                const topicCount = lesson.topics?.length || 0;

                return (
                  <div
                    key={lesson.id}
                    className={`rounded-2xl border transition-all duration-200 bg-white p-5 sm:p-6 shadow-sm hover:shadow-md ${
                      isCompleted
                        ? "border-emerald-200 hover:border-emerald-300"
                        : isInProgress
                        ? "border-amber-200 hover:border-brand-300"
                        : "border-slate-200 hover:border-brand-200"
                    }`}
                  >
                    <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
                      <div className="flex items-start gap-4">
                        <div
                          className={`flex h-10 w-10 shrink-0 items-center justify-center rounded-xl font-extrabold text-sm ${
                            isCompleted
                              ? "bg-emerald-50 text-emerald-700 border border-emerald-200"
                              : isInProgress
                              ? "bg-amber-50 text-amber-700 border border-amber-200"
                              : "bg-slate-100 text-slate-700 border border-slate-200"
                          }`}
                        >
                          {isCompleted ? <CheckCircle2 className="h-5 w-5" /> : idx + 1}
                        </div>

                        <div className="space-y-1">
                          <div className="flex flex-wrap items-center gap-2">
                            <span className="text-[11px] font-bold text-slate-400 uppercase tracking-wider">
                              Module {lesson.lesson_order || idx + 1}
                            </span>
                            <Badge
                              variant={
                                lesson.difficulty === "EASY"
                                  ? "emerald"
                                  : lesson.difficulty === "MEDIUM"
                                  ? "brand"
                                  : "purple"
                              }
                              size="sm"
                            >
                              {lesson.difficulty_level || lesson.difficulty || "MEDIUM"}
                            </Badge>
                            <span className="flex items-center gap-1 text-[11px] text-slate-500 font-medium">
                              <Clock className="h-3.5 w-3.5 text-slate-400" />
                              {lesson.estimated_duration || lesson.estimated_minutes || 15} mins
                            </span>
                          </div>

                          <h3 className="text-base font-bold text-slate-900 hover:text-brand-600 transition-colors">
                            {lesson.title}
                          </h3>

                          <p className="text-xs text-slate-600 max-w-2xl leading-relaxed">
                            {lesson.short_description || lesson.description}
                          </p>

                          {/* Topics & Resources Summary Badges */}
                          <div className="flex flex-wrap items-center gap-2 pt-2">
                            {lesson.topics && lesson.topics.length > 0 && (
                              <div className="flex items-center gap-1 text-[11px] text-slate-500">
                                <span className="font-semibold text-slate-700">Topics:</span>
                                {lesson.topics.map((t) => (
                                  <span
                                    key={t.id}
                                    className="rounded bg-slate-100 px-1.5 py-0.5 text-[10px] font-medium text-slate-600"
                                  >
                                    {t.name}
                                  </span>
                                ))}
                              </div>
                            )}

                            {resourceCount > 0 && (
                              <span className="rounded-md bg-brand-50 border border-brand-100 px-2 py-0.5 text-[10px] font-bold text-brand-700 flex items-center gap-1">
                                <Sparkles className="h-3 w-3" />
                                {resourceCount} Verified {resourceCount === 1 ? "Resource" : "Resources"}
                              </span>
                            )}
                          </div>
                        </div>
                      </div>

                      {/* Action Button */}
                      <div className="flex items-center gap-3 shrink-0 self-end md:self-center">
                        <Link
                          href={`/student/lessons/${lesson.id}`}
                          className={`inline-flex items-center gap-2 rounded-xl px-4 py-2.5 text-xs font-bold transition shadow-sm ${
                            isCompleted
                              ? "bg-slate-100 hover:bg-slate-200 text-slate-700"
                              : isInProgress
                              ? "bg-brand-600 hover:bg-brand-700 text-white"
                              : "bg-brand-600 hover:bg-brand-700 text-white"
                          }`}
                        >
                          <PlayCircle className="h-4 w-4" />
                          <span>{isCompleted ? "Review Module" : isInProgress ? "Continue Module" : "Start Module"}</span>
                          <ChevronRight className="h-3.5 w-3.5" />
                        </Link>
                      </div>
                    </div>
                  </div>
                );
              })}
            </div>
          )}
        </div>
      </div>
    </RoleLayout>
  );
}
