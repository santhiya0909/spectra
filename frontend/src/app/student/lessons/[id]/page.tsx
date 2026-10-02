"use client";

import React, { useState } from "react";
import Link from "next/link";
import { useParams, useRouter } from "next/navigation";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { subjectService, Lesson, StudyResource, LessonYouTubeResponse } from "@/services/subject.service";
import { puzzleService, Puzzle, PuzzleSubmissionResult } from "@/services/puzzle.service";
import { RoleLayout } from "@/components/layout/RoleLayout";
import { GlassCard } from "@/components/common/GlassCard";
import { Badge } from "@/components/common/Badge";
import PuzzlePlayer from "@/components/puzzles/PuzzlePlayer";
import TopicPracticeModal from "@/components/practice/TopicPracticeModal";
import {
  ArrowLeft,
  ArrowRight,
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
  Zap,
  PlayCircle,
  Check,
  ChevronRight,
  ListOrdered,
  Award,
  ChevronLeft,
  Share2,
  Youtube,
  Play,
  AlertCircle,
  RefreshCw,
  Tv,
} from "lucide-react";

export default function LessonViewerPage() {
  const params = useParams();
  const router = useRouter();
  const queryClient = useQueryClient();
  const lessonId = Number(params?.id);

  const [activePracticeTopic, setActivePracticeTopic] = useState<{ id: number; name: string } | null>(null);
  const [readCompleted, setReadCompleted] = useState(false);

  // 1. Fetch current lesson
  const { data: lesson, isLoading: lessonLoading } = useQuery<Lesson>({
    queryKey: ["lesson", lessonId],
    queryFn: () => subjectService.getLesson(lessonId),
    enabled: !!lessonId,
  });

  // 2. Fetch subject details to get sibling lessons for left sidebar
  const { data: subject } = useQuery({
    queryKey: ["subject", lesson?.subject_id],
    queryFn: () => subjectService.getSubject(lesson!.subject_id),
    enabled: !!lesson?.subject_id,
  });

  // 3. Fetch interactive puzzles for this lesson
  const { data: puzzles, refetch: refetchPuzzles } = useQuery<Puzzle[]>({
    queryKey: ["lessonPuzzles", lessonId],
    queryFn: () => puzzleService.getLessonPuzzles(lessonId),
    enabled: !!lessonId,
  });

  // 4. Fetch quiz for this lesson
  const { data: lessonQuiz } = useQuery({
    queryKey: ["lessonQuiz", lessonId],
    queryFn: () => puzzleService.getLessonQuiz(lessonId),
    enabled: !!lessonId,
  });

  // 5. Fetch recommended YouTube educational videos for this lesson
  const {
    data: youtubeData,
    isLoading: youtubeLoading,
    isError: youtubeError,
    refetch: refetchYouTube,
  } = useQuery<LessonYouTubeResponse>({
    queryKey: ["lessonYouTube", lessonId],
    queryFn: () => subjectService.getLessonYouTubeRecommendations(lessonId),
    enabled: !!lessonId,
  });

  const progressMutation = useMutation({
    mutationFn: () =>
      subjectService.updateLessonProgress(lessonId, "COMPLETED", 100.0),
    onSuccess: () => {
      setReadCompleted(true);
      queryClient.invalidateQueries({ queryKey: ["lesson", lessonId] });
      queryClient.invalidateQueries({ queryKey: ["studentDashboard"] });
      queryClient.invalidateQueries({ queryKey: ["subject", lesson?.subject_id] });
    },
  });

  const siblingLessons = subject?.lessons || [];
  const currentIdx = siblingLessons.findIndex((l) => l.id === lessonId);
  const prevLesson = currentIdx > 0 ? siblingLessons[currentIdx - 1] : null;
  const nextLesson = currentIdx >= 0 && currentIdx < siblingLessons.length - 1 ? siblingLessons[currentIdx + 1] : null;

  const handlePuzzleSolved = (res: PuzzleSubmissionResult) => {
    refetchPuzzles();
    queryClient.invalidateQueries({ queryKey: ["lesson", lessonId] });
    queryClient.invalidateQueries({ queryKey: ["studentDashboard"] });
  };

  const isCompleted = lesson?.status === "COMPLETED" || readCompleted;
  const puzzle = puzzles && puzzles.length > 0 ? puzzles[0] : null;

  return (
    <RoleLayout allowedRoles={["STUDENT", "ADMIN"]}>
      <div className="space-y-6 pb-20">
        {/* Navigation Breadcrumb Bar */}
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-white/[0.08] pb-4">
          <div className="flex items-center gap-2 text-xs font-semibold text-slate-400">
            <Link
              href={`/student/subjects/${lesson?.subject_id || ""}`}
              className="hover:text-cyan-300 transition flex items-center gap-1"
            >
              <ArrowLeft className="h-4 w-4" />
              <span>{lesson?.subject_name || "Curriculum"}</span>
            </Link>
            <span>/</span>
            <span className="text-white font-bold truncate max-w-xs">
              {lesson?.title || "Lesson"}
            </span>
          </div>

          <div className="flex items-center gap-2">
            <Link
              href={`/student/ai-tutor?topic=${lesson?.topic_id || ""}&lesson=${lessonId}`}
              className="inline-flex items-center gap-1.5 rounded-xl border border-cyan-500/30 bg-cyan-950/40 px-3.5 py-1.5 text-xs font-bold text-cyan-300 hover:bg-cyan-900/40 transition shadow-[0_0_12px_rgba(6,182,212,0.2)]"
            >
              <Bot className="h-4 w-4 text-cyan-400" />
              <span>Explain with AI Tutor</span>
            </Link>
          </div>
        </div>

        {lessonLoading ? (
          <div className="grid grid-cols-1 lg:grid-cols-4 gap-6 animate-pulse">
            <div className="h-96 bg-slate-800/40 rounded-3xl border border-white/5" />
            <div className="lg:col-span-2 h-96 bg-slate-800/40 rounded-3xl border border-white/5" />
            <div className="h-96 bg-slate-800/40 rounded-3xl border border-white/5" />
          </div>
        ) : lesson ? (
          /* 3-COLUMN MODERN LEARNING LAYOUT */
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
            {/* COLUMN 1: LEFT CURRICULUM NAV (3 COLS) */}
            <div className="hidden lg:block lg:col-span-3 space-y-4 sticky top-20">
              <GlassCard className="p-5">
                <div className="flex items-center justify-between pb-3 border-b border-white/[0.08] mb-3">
                  <span className="text-[10px] font-extrabold uppercase tracking-widest text-slate-400">
                    Track Lessons
                  </span>
                  <span className="text-xs font-bold text-cyan-400 font-mono">
                    {siblingLessons.filter(l => l.status === "COMPLETED").length}/{siblingLessons.length}
                  </span>
                </div>

                <div className="space-y-1.5 max-h-[70vh] overflow-y-auto pr-1">
                  {siblingLessons.map((item, idx) => {
                    const isSelected = item.id === lessonId;
                    const itemDone = item.status === "COMPLETED";

                    return (
                      <Link
                        key={item.id}
                        href={`/student/lessons/${item.id}`}
                        className={`flex items-center gap-3 p-2.5 rounded-xl text-xs font-semibold transition-all ${
                          isSelected
                            ? "bg-cyan-500 text-black font-extrabold shadow-[0_0_15px_rgba(6,182,212,0.4)]"
                            : itemDone
                            ? "bg-emerald-950/20 text-emerald-300 hover:bg-emerald-900/30 border border-emerald-500/20"
                            : "text-slate-400 hover:bg-white/[0.04] hover:text-white"
                        }`}
                      >
                        <div className={`w-6 h-6 rounded-lg flex items-center justify-center text-[10px] font-bold shrink-0 ${
                          isSelected
                            ? "bg-black text-cyan-400"
                            : itemDone
                            ? "bg-emerald-500 text-black shadow-[0_0_8px_#10b981]"
                            : "bg-slate-800 text-slate-400"
                        }`}>
                          {itemDone ? <Check className="w-3.5 h-3.5 stroke-[3]" /> : idx + 1}
                        </div>
                        <span className="truncate flex-1">{item.title}</span>
                      </Link>
                    );
                  })}
                </div>
              </GlassCard>
            </div>

            {/* COLUMN 2: CENTER MAIN LESSON CONTENT (6 COLS) */}
            <div className="lg:col-span-6 space-y-8">
              {/* Lesson Hero Header */}
              <div className="relative overflow-hidden rounded-3xl bg-gradient-to-r from-[#0B1530] via-[#10103A] to-[#140C2C] p-6 sm:p-8 text-white shadow-xl shadow-cyan-950/20 border border-white/10">
                <div className="flex flex-wrap items-center gap-2 mb-3">
                  <span className="text-xs font-extrabold uppercase px-2.5 py-0.5 rounded-md bg-cyan-950/50 text-cyan-300 border border-cyan-500/30 font-mono">
                    Lesson {currentIdx >= 0 ? currentIdx + 1 : 1}
                  </span>
                  <span className="text-xs font-semibold px-2.5 py-0.5 rounded-md bg-white/10 text-slate-300 border border-white/10">
                    {lesson.difficulty || "MEDIUM"}
                  </span>
                  <span className="flex items-center gap-1 text-xs text-slate-400">
                    <Clock className="w-3.5 h-3.5" />
                    {lesson.estimated_minutes || 15} mins
                  </span>
                  <span className="inline-flex items-center gap-1 text-xs font-bold text-amber-300 bg-amber-500/15 px-2.5 py-0.5 rounded-md border border-amber-500/25 font-mono">
                    <Sparkles className="w-3.5 h-3.5 text-amber-400" />
                    +30 XP Completion
                  </span>
                </div>

                <h1 className="text-2xl sm:text-3xl font-black text-white tracking-tight">
                  {lesson.title}
                </h1>
                <p className="mt-2 text-sm text-slate-300 leading-relaxed font-normal">
                  {lesson.short_description || lesson.description}
                </p>

                {/* Topics covered */}
                {lesson.topics && lesson.topics.length > 0 && (
                  <div className="mt-4 pt-4 border-t border-white/10 flex flex-wrap items-center gap-2">
                    <span className="text-xs text-slate-400 font-semibold">Topics:</span>
                    {lesson.topics.map((t) => (
                      <button
                        key={t.id}
                        type="button"
                        onClick={() => setActivePracticeTopic({ id: t.id, name: t.name })}
                        className="inline-flex items-center gap-1 text-xs font-semibold px-2.5 py-1 rounded-lg bg-white/[0.05] hover:bg-white/10 text-cyan-300 transition border border-white/10"
                      >
                        <Zap className="w-3 h-3 text-amber-400" />
                        <span>{t.name} (Practice +10 XP)</span>
                      </button>
                    ))}
                  </div>
                )}
              </div>

              {/* Main Educational Text / Markdown Content */}
              <GlassCard className="p-6 sm:p-8">
                <div 
                  className="space-y-4 text-slate-300 leading-relaxed text-sm sm:text-base font-normal whitespace-pre-line"
                >
                  {lesson.content || (
                    <div className="space-y-4">
                      <p>
                        Welcome to this comprehensive lesson module. Review the concepts below, inspect the syntax patterns, and test your understanding with the interactive puzzle.
                      </p>
                      <h3 className="text-lg font-bold text-white pt-2">Core Objectives</h3>
                      <ul className="list-disc list-inside space-y-1 text-slate-300">
                        <li>Master the fundamental syntax and operational semantics.</li>
                        <li>Understand common edge cases, performance trade-offs, and memory implications.</li>
                        <li>Apply logic solving skills to pass the checkpoint puzzle and quiz.</li>
                      </ul>
                    </div>
                  )}
                </div>

                {/* Mark as Read Button */}
                <div className="mt-8 pt-6 border-t border-white/[0.08] flex items-center justify-between">
                  <span className="text-xs font-semibold text-slate-400">
                    Finished reading the core concept material?
                  </span>
                  <button
                    type="button"
                    onClick={() => progressMutation.mutate()}
                    disabled={isCompleted || progressMutation.isPending}
                    className={`px-4 py-2 rounded-xl text-xs font-bold transition-all flex items-center gap-1.5 ${
                      isCompleted
                        ? "bg-emerald-500/20 text-emerald-300 border border-emerald-500/30"
                        : "bg-cyan-500 hover:bg-cyan-400 text-black font-extrabold shadow-[0_0_12px_rgba(6,182,212,0.3)]"
                    }`}
                  >
                    <CheckCircle2 className="w-4 h-4" />
                    <span>{isCompleted ? "Reading Completed ✓" : "Mark as Read (+5 XP)"}</span>
                  </button>
                </div>
              </GlassCard>

              {/* EMBEDDED INTERACTIVE PUZZLE */}
              {puzzle ? (
                <div className="space-y-3">
                  <div className="flex items-center justify-between">
                    <h3 className="text-lg font-bold text-white flex items-center gap-2">
                      <Zap className="w-5 h-5 text-cyan-400" />
                      <span>Interactive Lesson Puzzle</span>
                    </h3>
                    <span className="text-xs font-semibold text-amber-400 font-mono">
                      Solve to earn +10 XP
                    </span>
                  </div>
                  <PuzzlePlayer puzzle={puzzle} onSolved={handlePuzzleSolved} />
                </div>
              ) : null}

              {/* Study Resources / Further Reading */}
              {lesson.study_resources && lesson.study_resources.length > 0 && (
                <GlassCard className="p-6 space-y-4">
                  <h3 className="text-base font-bold text-white flex items-center gap-2">
                    <BookOpen className="w-5 h-5 text-cyan-400" />
                    <span>Verified Study Resources &amp; Documentation</span>
                  </h3>
                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                    {lesson.study_resources.map((res) => (
                      <a
                        key={res.id}
                        href={res.url}
                        target="_blank"
                        rel="noreferrer"
                        className="p-3.5 rounded-2xl border border-white/[0.08] hover:border-cyan-500/40 bg-white/[0.02] hover:bg-white/[0.05] transition-all flex items-start gap-3 group"
                      >
                        <div className="w-8 h-8 rounded-xl bg-cyan-500/10 group-hover:bg-cyan-500/20 flex items-center justify-center text-cyan-400 shrink-0">
                          <ExternalLink className="w-4 h-4" />
                        </div>
                        <div className="flex-1">
                          <h4 className="text-xs font-bold text-white group-hover:text-cyan-300 line-clamp-1">
                            {res.title}
                          </h4>
                          <p className="text-[11px] text-slate-400 line-clamp-1 mt-0.5">
                            {res.provider} &bull; {res.resource_type}
                          </p>
                        </div>
                      </a>
                    ))}
                  </div>
                </GlassCard>
              )}

              {/* 📺 Recommended for this lesson (YouTube Video Recommendations) */}
              <GlassCard className="p-6 space-y-5">
                <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-white/[0.08] pb-4">
                  <div className="flex items-center gap-2.5">
                    <div className="w-9 h-9 rounded-2xl bg-rose-500/15 flex items-center justify-center text-rose-400 shadow-sm border border-rose-500/30">
                      <Youtube className="w-5 h-5 fill-rose-500 text-black" />
                    </div>
                    <div>
                      <h3 className="text-base font-bold text-white flex items-center gap-2">
                        Recommended for this lesson
                        <span className="text-[10px] font-extrabold uppercase px-2 py-0.5 rounded-full bg-rose-500/20 text-rose-300 border border-rose-500/30">
                          Curated Videos
                        </span>
                      </h3>
                      <p className="text-xs text-slate-400 mt-0.5">
                        Visual explanations and deep dives matched to this lesson
                      </p>
                    </div>
                  </div>
                  {youtubeData?.query_used && (
                    <span className="text-[11px] text-slate-500 font-mono hidden md:inline-block">
                      query: {youtubeData.query_used}
                    </span>
                  )}
                </div>

                {/* SKELETON LOADING STATE */}
                {youtubeLoading && (
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                    {[1, 2, 3].map((n) => (
                      <div
                        key={n}
                        className="rounded-2xl border border-white/5 bg-slate-900/40 p-3 space-y-3 animate-pulse"
                      >
                        <div className="w-full aspect-video bg-slate-800 rounded-xl" />
                        <div className="space-y-2">
                          <div className="h-4 bg-slate-800 rounded w-5/6" />
                          <div className="h-3 bg-slate-800 rounded w-1/2" />
                          <div className="h-3 bg-slate-800/60 rounded w-full" />
                        </div>
                      </div>
                    ))}
                  </div>
                )}

                {/* ERROR STATE */}
                {!youtubeLoading && youtubeError && (
                  <div className="p-4 rounded-2xl bg-rose-950/20 border border-rose-500/30 flex items-center justify-between gap-3 text-rose-300 text-xs">
                    <div className="flex items-center gap-2">
                      <AlertCircle className="w-4 h-4 shrink-0 text-rose-400" />
                      <span>Video recommendations are temporarily unavailable.</span>
                    </div>
                    <button
                      onClick={() => refetchYouTube()}
                      className="px-3 py-1.5 rounded-xl bg-white/[0.05] border border-rose-500/30 text-rose-300 font-semibold text-xs hover:bg-rose-500/20 transition-colors flex items-center gap-1.5 shadow-sm"
                    >
                      <RefreshCw className="w-3.5 h-3.5" />
                      <span>Retry</span>
                    </button>
                  </div>
                )}

                {/* EMPTY STATE */}
                {!youtubeLoading && !youtubeError && (!youtubeData?.videos || youtubeData.videos.length === 0) && (
                  <div className="p-8 text-center rounded-2xl bg-white/[0.02] border border-dashed border-white/10">
                    <Tv className="w-8 h-8 text-slate-500 mx-auto mb-2" />
                    <p className="text-xs font-semibold text-slate-300">No video recommendations found</p>
                    <p className="text-[11px] text-slate-500 mt-1">Check back later for curated visual content on this topic.</p>
                  </div>
                )}

                {/* VIDEO CARDS GRID */}
                {!youtubeLoading && !youtubeError && youtubeData?.videos && youtubeData.videos.length > 0 && (
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                    {youtubeData.videos.map((vid, idx) => (
                      <div
                        key={vid.video_id || idx}
                        className="group flex flex-col justify-between rounded-2xl border border-white/[0.08] bg-[#090E20]/90 hover:border-rose-500/40 hover:shadow-[0_0_20px_rgba(244,63,94,0.15)] transition-all overflow-hidden"
                      >
                        {/* Thumbnail with duration badge and play hover */}
                        <div className="relative aspect-video w-full bg-slate-900 overflow-hidden">
                          {vid.thumbnail_url ? (
                            <img
                              src={vid.thumbnail_url}
                              alt={vid.title}
                              className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
                              loading="lazy"
                            />
                          ) : (
                            <div className="w-full h-full flex items-center justify-center bg-slate-800 text-slate-400">
                              <Play className="w-8 h-8" />
                            </div>
                          )}

                          {/* Hover Play Button Overlay */}
                          <div className="absolute inset-0 bg-black/40 opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center">
                            <div className="w-11 h-11 rounded-full bg-rose-600 text-white flex items-center justify-center shadow-lg group-hover:scale-110 transition-transform">
                              <Play className="w-5 h-5 fill-white ml-0.5" />
                            </div>
                          </div>

                          {/* Duration Badge */}
                          {vid.duration && (
                            <span className="absolute bottom-2 right-2 px-2 py-0.5 rounded-md bg-black/80 backdrop-blur-sm text-white text-[10px] font-semibold flex items-center gap-1 font-mono">
                              <Clock className="w-3 h-3 text-slate-300" />
                              {vid.duration}
                            </span>
                          )}
                        </div>

                        {/* Card Content */}
                        <div className="p-4 flex-1 flex flex-col justify-between space-y-3">
                          <div className="space-y-1.5">
                            <div className="flex items-center gap-1.5 text-[10px] font-semibold text-rose-400">
                              <span className="truncate max-w-[170px]">{vid.channel_name}</span>
                              <span className="text-slate-500">&bull;</span>
                              <span className="text-slate-400">YouTube</span>
                            </div>

                            <h4
                              className="text-xs font-bold text-white group-hover:text-rose-300 transition-colors line-clamp-2 leading-relaxed"
                              title={vid.title}
                            >
                              {vid.title}
                            </h4>

                            {vid.description && (
                              <p className="text-[11px] text-slate-400 line-clamp-2 leading-normal">
                                {vid.description}
                              </p>
                            )}
                          </div>

                          {/* Action Button */}
                          <a
                            href={vid.url}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="mt-2 w-full py-2 px-3 rounded-xl bg-white/[0.04] hover:bg-rose-500/10 border border-white/10 hover:border-rose-500/30 text-slate-300 hover:text-rose-300 text-xs font-bold transition-all flex items-center justify-center gap-1.5"
                          >
                            <span>Watch on YouTube</span>
                            <ExternalLink className="w-3.5 h-3.5" />
                          </a>
                        </div>
                      </div>
                    ))}
                  </div>
                )}
              </GlassCard>

              {/* Take a Quick Mental Break? CTA */}
              <div className="rounded-3xl border border-cyan-500/40 bg-gradient-to-r from-[#0B1530] via-[#101436] to-[#150D2E] p-6 sm:p-7 shadow-[0_0_30px_rgba(6,182,212,0.15)] flex flex-col sm:flex-row sm:items-center justify-between gap-5 backdrop-blur-2xl">
                <div className="space-y-1.5 flex-1">
                  <span className="text-[10px] font-extrabold uppercase tracking-widest text-cyan-300 bg-cyan-950/50 px-2.5 py-0.5 rounded-full border border-cyan-500/30 inline-block">
                    🎮 Need a Mental Break?
                  </span>
                  <h4 className="text-base sm:text-lg font-black text-white">
                    Step into the SPECTRA Puzzle Lab
                  </h4>
                  <p className="text-xs text-slate-300 max-w-xl leading-relaxed">
                    Play a quick 2–3 minute interactive mini-game (Memory Match, Pattern Shift, or Word Scramble) to relax and recharge your mind.
                  </p>
                </div>
                <Link
                  href="/student/puzzles"
                  className="px-6 py-3.5 rounded-2xl bg-cyan-500 hover:bg-cyan-400 text-black font-black text-xs sm:text-sm shadow-[0_0_20px_rgba(6,182,212,0.4)] transition-all flex items-center justify-center gap-2 shrink-0 self-start sm:self-auto hover:scale-[1.02] active:scale-[0.98]"
                >
                  <span>Play Mini-Game &rarr;</span>
                  <ArrowRight className="w-4 h-4 text-black" />
                </Link>
              </div>

              {/* Bottom Next/Prev Pagination */}
              <div className="flex items-center justify-between pt-4 border-t border-white/[0.08]">
                {prevLesson ? (
                  <Link
                    href={`/student/lessons/${prevLesson.id}`}
                    className="inline-flex items-center gap-2 px-4 py-2.5 rounded-xl border border-white/10 bg-[#0B1124] hover:bg-white/[0.08] text-slate-300 text-xs font-bold shadow-sm"
                  >
                    <ChevronLeft className="w-4 h-4" />
                    <span>Previous: {prevLesson.title}</span>
                  </Link>
                ) : <div />}

                {nextLesson ? (
                  <Link
                    href={`/student/lessons/${nextLesson.id}`}
                    className="inline-flex items-center gap-2 px-5 py-2.5 rounded-xl bg-cyan-500 hover:bg-cyan-400 text-black text-xs font-black shadow-[0_0_15px_rgba(6,182,212,0.3)]"
                  >
                    <span>Next: {nextLesson.title}</span>
                    <ChevronRight className="w-4 h-4" />
                  </Link>
                ) : (
                  <Link
                    href={`/student/subjects/${lesson.subject_id}`}
                    className="inline-flex items-center gap-2 px-5 py-2.5 rounded-xl bg-emerald-500 hover:bg-emerald-400 text-black text-xs font-black shadow-[0_0_15px_rgba(16,185,129,0.3)]"
                  >
                    <span>Complete Track</span>
                    <Award className="w-4 h-4" />
                  </Link>
                )}
              </div>
            </div>

            {/* COLUMN 3: RIGHT SIDEBAR PROGRESS OUTLINE (3 COLS) */}
            <div className="lg:col-span-3 space-y-6 sticky top-20">
              {/* Learning Progress Card */}
              <GlassCard className="p-6 space-y-5">
                <div className="flex items-center justify-between">
                  <h3 className="text-sm font-bold text-white">
                    Lesson Journey
                  </h3>
                  <span className="text-xs font-bold text-cyan-300 bg-cyan-950/40 px-2 py-0.5 rounded-full border border-cyan-500/30 font-mono">
                    {lesson.completion_percentage || 0}% Complete
                  </span>
                </div>

                <div className="space-y-3">
                  {/* Step 1: Read */}
                  <div className="flex items-center justify-between text-xs p-2.5 rounded-xl bg-white/[0.03] border border-white/5">
                    <span className="flex items-center gap-2 text-slate-300 font-medium">
                      <BookOpen className="w-4 h-4 text-cyan-400" /> Read Content
                    </span>
                    <span className="font-bold text-slate-400 font-mono">
                      {isCompleted ? "✓ Done" : "+5 XP"}
                    </span>
                  </div>

                  {/* Step 2: Puzzle Lab */}
                  <Link
                    href="/student/puzzles"
                    className="flex items-center justify-between text-xs p-2.5 rounded-xl bg-purple-950/30 hover:bg-purple-900/40 border border-purple-500/30 text-purple-200 transition-colors"
                  >
                    <span className="flex items-center gap-2 font-bold">
                      <Zap className="w-4 h-4 text-purple-400" /> Puzzle Lab Break
                    </span>
                    <span className="font-extrabold text-purple-300 font-mono">
                      +20 XP &rarr;
                    </span>
                  </Link>

                  {/* Step 3: Practice */}
                  <div className="flex items-center justify-between text-xs p-2.5 rounded-xl bg-white/[0.03] border border-white/5">
                    <span className="flex items-center gap-2 text-slate-300 font-medium">
                      <Code className="w-4 h-4 text-amber-400" /> Topic Practice
                    </span>
                    <span className="font-bold text-amber-400 font-mono">
                      +10 XP
                    </span>
                  </div>

                  {/* Step 4: Quiz */}
                  {lessonQuiz ? (
                    <Link
                      href={`/student/quizzes/${lessonQuiz.quiz_id || (lessonQuiz as any).id}`}
                      className="flex items-center justify-between text-xs p-2.5 rounded-xl bg-emerald-950/30 hover:bg-emerald-900/40 border border-emerald-500/30 text-emerald-200 transition-colors"
                    >
                      <span className="flex items-center gap-2 font-bold">
                        <HelpCircle className="w-4 h-4 text-emerald-400" /> Lesson Quiz
                      </span>
                      <span className="font-extrabold text-emerald-300 font-mono">
                        +25 XP &rarr;
                      </span>
                    </Link>
                  ) : (
                    <div className="flex items-center justify-between text-xs p-2.5 rounded-xl bg-white/[0.03] border border-white/5 opacity-60">
                      <span className="flex items-center gap-2 text-slate-300 font-medium">
                        <HelpCircle className="w-4 h-4 text-emerald-400" /> Lesson Quiz
                      </span>
                      <span className="font-bold text-slate-500 font-mono">
                        N/A
                      </span>
                    </div>
                  )}
                </div>

                <div className="pt-2 border-t border-white/[0.08]">
                  <Link
                    href={`/student/ai-tutor?topic=${lesson.topic_id || ""}&lesson=${lessonId}`}
                    className="w-full py-2.5 px-3 rounded-xl bg-white/[0.05] hover:bg-white/10 text-cyan-300 font-bold text-xs flex items-center justify-center gap-2 border border-white/10 transition"
                  >
                    <Bot className="w-4 h-4 text-cyan-400" />
                    <span>Ask Socratic Tutor</span>
                  </Link>
                </div>
              </GlassCard>
            </div>
          </div>
        ) : null}

        {/* Modal for topic practice */}
        {activePracticeTopic && (
          <TopicPracticeModal
            isOpen={true}
            topicId={activePracticeTopic.id}
            topicName={activePracticeTopic.name}
            onClose={() => setActivePracticeTopic(null)}
            onCompleted={(xp) => {
              queryClient.invalidateQueries({ queryKey: ["lesson", lessonId] });
              queryClient.invalidateQueries({ queryKey: ["studentDashboard"] });
            }}
          />
        )}
      </div>
    </RoleLayout>
  );
}
