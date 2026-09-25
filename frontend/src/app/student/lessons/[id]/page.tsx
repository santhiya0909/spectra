"use client";

import React, { useState } from "react";
import Link from "next/link";
import { useParams, useRouter } from "next/navigation";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { subjectService, Lesson, StudyResource } from "@/services/subject.service";
import { RoleLayout } from "@/components/layout/RoleLayout";
import { Badge } from "@/components/common/Badge";
import {
  ArrowLeft,
  CheckCircle2,
  Clock,
  Sparkles,
  Bot,
  HelpCircle,
  BookOpen,
  Loader2,
  ExternalLink,
  FileText,
  Video,
  Code,
  Layers,
  GraduationCap,
  Globe,
} from "lucide-react";

export default function LessonViewerPage() {
  const params = useParams();
  const router = useRouter();
  const queryClient = useQueryClient();
  const lessonId = Number(params?.id);

  const { data: lesson, isLoading } = useQuery<Lesson>({
    queryKey: ["lesson", lessonId],
    queryFn: () => subjectService.getLesson(lessonId),
    enabled: !!lessonId,
  });

  const [completed, setCompleted] = useState(false);

  const progressMutation = useMutation({
    mutationFn: () =>
      subjectService.updateLessonProgress(lessonId, "COMPLETED", 100.0),
    onSuccess: () => {
      setCompleted(true);
      queryClient.invalidateQueries({ queryKey: ["lesson", lessonId] });
      queryClient.invalidateQueries({ queryKey: ["studentDashboard"] });
      queryClient.invalidateQueries({ queryKey: ["subject", lesson?.subject_id] });
    },
  });

  const getResourceIcon = (type: string) => {
    switch (type.toUpperCase()) {
      case "DOCUMENTATION":
        return <BookOpen className="h-4 w-4 text-brand-600" />;
      case "TUTORIAL":
        return <GraduationCap className="h-4 w-4 text-emerald-600" />;
      case "ARTICLE":
        return <FileText className="h-4 w-4 text-indigo-600" />;
      case "VIDEO":
        return <Video className="h-4 w-4 text-rose-600" />;
      case "PRACTICE":
        return <Code className="h-4 w-4 text-amber-600" />;
      default:
        return <Globe className="h-4 w-4 text-slate-600" />;
    }
  };

  const isLessonCompleted = completed || lesson?.status === "COMPLETED";

  return (
    <RoleLayout allowedRoles={["STUDENT", "ADMIN"]}>
      <div className="mx-auto max-w-4xl space-y-6">
        {/* Navigation Top Bar */}
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
          <Link
            href={`/student/subjects/${lesson?.subject_id || ""}`}
            className="inline-flex items-center gap-1.5 text-xs font-semibold text-slate-500 hover:text-slate-800 transition"
          >
            <ArrowLeft className="h-4 w-4" />
            <span>Back to {lesson?.subject_name ? `${lesson.subject_name} Curriculum` : "Curriculum"}</span>
          </Link>

          <Link
            href={`/student/ai-tutor?topic=${lesson?.topic_id || ""}`}
            className="inline-flex items-center gap-1.5 rounded-xl border border-brand-200 bg-brand-50 px-3.5 py-1.5 text-xs font-bold text-brand-700 hover:bg-brand-100 transition shadow-sm self-start sm:self-center"
          >
            <Bot className="h-4 w-4 text-brand-600" />
            <span>Ask AI Tutor about this</span>
          </Link>
        </div>

        {isLoading ? (
          <div className="space-y-6 animate-pulse">
            <div className="h-48 bg-slate-200 rounded-3xl" />
            <div className="h-96 bg-slate-200 rounded-3xl" />
          </div>
        ) : lesson ? (
          <div className="space-y-6">
            {/* Header Card */}
            <div className="rounded-3xl border border-slate-200 bg-white p-6 sm:p-8 shadow-sm">
              <div className="flex flex-wrap items-center gap-2 mb-3">
                <span className="text-xs font-bold text-slate-400 uppercase tracking-wider">
                  {lesson.subject_name} &bull; Module {lesson.lesson_order}
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
              </div>

              <h1 className="text-2xl sm:text-3xl font-extrabold text-slate-900 tracking-tight">
                {lesson.title}
              </h1>

              {lesson.short_description && (
                <p className="mt-2 text-sm text-slate-600 leading-relaxed">
                  {lesson.short_description}
                </p>
              )}

              {/* Topics Covered */}
              {lesson.topics && lesson.topics.length > 0 && (
                <div className="mt-4 flex flex-wrap items-center gap-2">
                  <span className="text-xs font-semibold text-slate-500">Core Topics:</span>
                  {lesson.topics.map((t) => (
                    <span
                      key={t.id}
                      className="rounded-lg bg-slate-100 border border-slate-200 px-2.5 py-1 text-xs font-medium text-slate-700"
                    >
                      {t.name}
                    </span>
                  ))}
                </div>
              )}

              {/* Lesson Metadata Bar */}
              <div className="mt-5 flex flex-wrap items-center gap-4 text-xs font-semibold text-slate-500 border-t border-slate-100 pt-4">
                <span className="flex items-center gap-1.5">
                  <Clock className="h-4 w-4 text-slate-400" />
                  Estimated: {lesson.estimated_duration || lesson.estimated_minutes || 15} minutes
                </span>

                {isLessonCompleted ? (
                  <span className="flex items-center gap-1 text-emerald-600 font-bold bg-emerald-50 px-2.5 py-0.5 rounded-full border border-emerald-200">
                    <CheckCircle2 className="h-3.5 w-3.5" />
                    Completed
                  </span>
                ) : (
                  <span className="flex items-center gap-1 text-amber-600 font-bold bg-amber-50 px-2.5 py-0.5 rounded-full border border-amber-200">
                    <BookOpen className="h-3.5 w-3.5" />
                    In Progress
                  </span>
                )}
              </div>
            </div>

            {/* Verified External Study Resources Section */}
            {lesson.study_resources && lesson.study_resources.length > 0 && (
              <div className="rounded-3xl border border-brand-100 bg-gradient-to-br from-brand-50/50 via-white to-indigo-50/40 p-6 sm:p-8 shadow-sm">
                <div className="flex items-center justify-between mb-4">
                  <div className="flex items-center gap-2">
                    <div className="flex h-8 w-8 items-center justify-center rounded-xl bg-brand-600 text-white shadow-sm">
                      <Sparkles className="h-4 w-4" />
                    </div>
                    <div>
                      <h2 className="text-base font-bold text-slate-900">Verified Learning Resources</h2>
                      <p className="text-xs text-slate-500">Official documentation, interactive tutorials, and deep-dive articles.</p>
                    </div>
                  </div>
                  <span className="rounded-full bg-brand-100 text-brand-800 font-bold text-xs px-2.5 py-0.5">
                    {lesson.study_resources.length} Links
                  </span>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-3.5 mt-4">
                  {lesson.study_resources.map((res) => (
                    <div
                      key={res.id}
                      className="group flex flex-col justify-between rounded-2xl border border-slate-200 bg-white p-4 shadow-xs hover:border-brand-300 hover:shadow-sm transition duration-200"
                    >
                      <div>
                        <div className="flex items-center justify-between gap-2 mb-2">
                          <span className="inline-flex items-center gap-1 rounded-md bg-slate-100 px-2 py-0.5 text-[10px] font-bold uppercase tracking-wider text-slate-700">
                            {getResourceIcon(res.resource_type)}
                            <span>{res.resource_type}</span>
                          </span>
                          <span className="text-[11px] font-semibold text-brand-600 bg-brand-50 px-2 py-0.5 rounded border border-brand-100">
                            {res.provider}
                          </span>
                        </div>

                        <h3 className="text-sm font-bold text-slate-900 group-hover:text-brand-600 transition">
                          {res.title}
                        </h3>

                        {res.description && (
                          <p className="mt-1 text-xs text-slate-500 leading-relaxed line-clamp-2">
                            {res.description}
                          </p>
                        )}
                      </div>

                      <div className="mt-3 pt-2.5 border-t border-slate-100 flex items-center justify-end">
                        <a
                          href={res.url}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="inline-flex items-center gap-1.5 rounded-lg bg-slate-50 group-hover:bg-brand-600 group-hover:text-white px-3 py-1.5 text-xs font-bold text-slate-700 transition shadow-xs"
                        >
                          <span>Open Resource</span>
                          <ExternalLink className="h-3.5 w-3.5" />
                        </a>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Lesson Body Content */}
            <article className="rounded-3xl border border-slate-200 bg-white p-6 sm:p-10 shadow-sm leading-relaxed">
              <div className="flex items-center gap-2 mb-6 pb-3 border-b border-slate-100 text-xs font-bold uppercase tracking-wider text-slate-400">
                <BookOpen className="h-4 w-4 text-brand-600" />
                <span>Lesson Curriculum Guide & Code Notes</span>
              </div>
              <div className="whitespace-pre-wrap font-sans text-sm sm:text-base text-slate-700 space-y-4">
                {lesson.content}
              </div>
            </article>

            {/* Bottom Actions Card */}
            <div className="flex flex-col sm:flex-row items-center justify-between gap-4 rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
              <div>
                <h4 className="text-sm font-bold text-slate-900">Finished reviewing this concept?</h4>
                <p className="text-xs text-slate-500">Record your progress to advance your curriculum completion.</p>
              </div>

              <div className="flex items-center gap-3">
                <button
                  onClick={() => progressMutation.mutate()}
                  disabled={progressMutation.isPending || isLessonCompleted}
                  className={`inline-flex items-center gap-2 rounded-xl px-5 py-2.5 text-xs font-bold transition shadow-sm ${
                    isLessonCompleted
                      ? "bg-emerald-50 text-emerald-700 border border-emerald-200 cursor-default"
                      : "bg-brand-600 text-white hover:bg-brand-700"
                  }`}
                >
                  {progressMutation.isPending ? (
                    <Loader2 className="h-4 w-4 animate-spin" />
                  ) : (
                    <CheckCircle2 className="h-4 w-4" />
                  )}
                  <span>{isLessonCompleted ? "Completed" : "Mark as Completed"}</span>
                </button>

                <Link
                  href="/student/quizzes"
                  className="inline-flex items-center gap-1.5 rounded-xl border border-slate-200 bg-slate-50 px-4 py-2.5 text-xs font-bold text-slate-700 hover:bg-slate-100 transition"
                >
                  <HelpCircle className="h-4 w-4 text-brand-600" />
                  <span>Test Mastery</span>
                </Link>
              </div>
            </div>
          </div>
        ) : (
          <div className="rounded-2xl border border-dashed border-slate-300 p-8 text-center text-slate-500">
            Lesson not found or unavailable.
          </div>
        )}
      </div>
    </RoleLayout>
  );
}
