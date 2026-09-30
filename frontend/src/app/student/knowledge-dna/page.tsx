"use client";

import React, { useState } from "react";
import Link from "next/link";
import { useQuery } from "@tanstack/react-query";
import { RoleLayout } from "@/components/layout/RoleLayout";
import {
  knowledgeDnaService,
  KnowledgeDNAResponse,
  KnowledgeDNANode,
  TopicKnowledgeDNADetail,
} from "@/services/knowledge-dna.service";
import { subjectService, Subject } from "@/services/subject.service";
import { GlassCard } from "@/components/common/GlassCard";
import {
  Dna,
  Sparkles,
  ArrowRight,
  CheckCircle2,
  AlertCircle,
  HelpCircle,
  Clock,
  ExternalLink,
  Play,
  RotateCcw,
  BookOpen,
  Layers,
  ChevronRight,
  TrendingUp,
  AlertTriangle,
  Lock,
  Compass,
  ArrowDown,
  RefreshCw,
  Zap,
  Puzzle,
} from "lucide-react";

export default function KnowledgeDNAPage() {
  const [selectedSubjectId, setSelectedSubjectId] = useState<number | undefined>(undefined);
  const [selectedTopicId, setSelectedTopicId] = useState<number | null>(null);

  // 1. Fetch available curriculum subjects for the switcher
  const { data: subjects } = useQuery<Subject[]>({
    queryKey: ["subjectsList"],
    queryFn: () => subjectService.getSubjects(),
  });

  // 2. Fetch full Knowledge DNA graph for the active or selected subject
  const {
    data: dnaData,
    isLoading: dnaLoading,
    error: dnaError,
    refetch: refetchDNA,
    isFetching: dnaFetching,
  } = useQuery<KnowledgeDNAResponse>({
    queryKey: ["knowledgeDNA", selectedSubjectId],
    queryFn: () => knowledgeDnaService.getKnowledgeDNA(selectedSubjectId),
  });

  // Default active topic is the recommended focus topic, or the first topic
  const activeTopicId = selectedTopicId ?? dnaData?.recommended_focus?.topic_id ?? dnaData?.nodes[0]?.id ?? null;

  // 3. Fetch detailed view for the active topic (including YouTube recommendations)
  const {
    data: topicDetail,
    isLoading: topicLoading,
  } = useQuery<TopicKnowledgeDNADetail>({
    queryKey: ["topicDNADetail", activeTopicId],
    queryFn: () => knowledgeDnaService.getTopicDNADetail(activeTopicId!),
    enabled: !!activeTopicId,
  });

  const getStatusColor = (state: string) => {
    switch (state) {
      case "MASTERED":
        return {
          bg: "bg-emerald-500",
          lightBg: "bg-emerald-950/20",
          border: "border-emerald-500/30",
          text: "text-emerald-400",
          pill: "bg-emerald-500/15 text-emerald-300 border-emerald-500/30",
          dot: "bg-emerald-400 shadow-[0_0_8px_#34d399]",
          label: "Mastered",
        };
      case "DEVELOPING":
        return {
          bg: "bg-amber-500",
          lightBg: "bg-amber-950/20",
          border: "border-amber-500/30",
          text: "text-amber-400",
          pill: "bg-amber-500/15 text-amber-300 border-amber-500/30",
          dot: "bg-amber-400 shadow-[0_0_8px_#fbbf24]",
          label: "Developing",
        };
      case "WEAK":
        return {
          bg: "bg-rose-500",
          lightBg: "bg-rose-950/20",
          border: "border-rose-500/30",
          text: "text-rose-400",
          pill: "bg-rose-500/15 text-rose-300 border-rose-500/30",
          dot: "bg-rose-400 shadow-[0_0_8px_#f43f5e]",
          label: "Needs Attention",
        };
      case "LOCKED":
        return {
          bg: "bg-slate-700",
          lightBg: "bg-slate-900/30",
          border: "border-slate-800",
          text: "text-slate-400",
          pill: "bg-slate-800 text-slate-400 border-slate-700",
          dot: "bg-slate-500",
          label: "Locked",
        };
      default:
        return {
          bg: "bg-slate-700",
          lightBg: "bg-slate-900/30",
          border: "border-slate-800",
          text: "text-slate-400",
          pill: "bg-slate-800 text-slate-400 border-slate-700",
          dot: "bg-slate-500",
          label: "Not Started",
        };
    }
  };

  const selectedNode = dnaData?.nodes.find((n) => n.id === activeTopicId);

  return (
    <RoleLayout allowedRoles={["STUDENT", "ADMIN"]}>
      <div className="space-y-8 pb-16">
        {/* HERO SECTION */}
        <div className="relative overflow-hidden rounded-3xl bg-gradient-to-r from-[#0B1530] via-[#10103A] to-[#140C2C] p-6 sm:p-8 text-white shadow-xl shadow-cyan-950/20 border border-white/10">
          {/* Ambient glow effects */}
          <div className="absolute -top-16 -right-16 w-72 h-72 bg-cyan-500/15 rounded-full blur-[100px] pointer-events-none" />
          <div className="absolute -bottom-16 -left-16 w-72 h-72 bg-purple-500/15 rounded-full blur-[100px] pointer-events-none" />

          <div className="relative z-10 flex flex-col lg:flex-row lg:items-center justify-between gap-6">
            <div className="space-y-3 max-w-2xl">
              <div className="inline-flex items-center gap-2 rounded-full bg-cyan-500/10 px-3 py-1 text-xs font-bold text-cyan-300 backdrop-blur-md border border-cyan-500/30 shadow-[0_0_15px_rgba(6,182,212,0.2)]">
                <Dna className="w-4 h-4 text-cyan-400 animate-pulse" />
                <span>SPECTRA AI Cognitive Assessment Engine</span>
              </div>
              <h1 className="text-2xl sm:text-4xl font-black text-white tracking-tight">
                Your Knowledge DNA
              </h1>
              <p className="text-sm sm:text-base text-slate-300 leading-relaxed">
                A live map of what you know, what you&apos;re developing, and where SPECTRA recommends you focus next.
              </p>

              {/* Subject Switcher */}
              <div className="pt-2 flex flex-wrap items-center gap-2">
                <span className="text-xs font-bold text-slate-400">Curriculum Track:</span>
                {subjects && subjects.length > 0 ? (
                  subjects.map((s) => (
                    <button
                      key={s.id}
                      onClick={() => {
                        setSelectedSubjectId(s.id);
                        setSelectedTopicId(null);
                      }}
                      className={`px-3 py-1.5 rounded-xl text-xs font-bold transition-all ${
                        (selectedSubjectId ?? dnaData?.subject_id) === s.id
                          ? "bg-cyan-500 text-black shadow-[0_0_15px_rgba(6,182,212,0.4)]"
                          : "bg-white/[0.05] hover:bg-white/10 text-slate-300 border border-white/10"
                      }`}
                    >
                      {s.code || s.name}
                    </button>
                  ))
                ) : (
                  <span className="text-xs text-cyan-300 font-mono">
                    {dnaData?.subject_name || "Mathematics for Computing"}
                  </span>
                )}
              </div>
            </div>

            {/* Quick Metrics Bar */}
            <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 bg-[#080D1F]/80 backdrop-blur-xl rounded-2xl p-4 border border-white/10 shrink-0">
              <div className="text-center p-2">
                <span className="text-[10px] uppercase font-bold text-slate-400 block">Overall Mastery</span>
                <span className="text-2xl sm:text-3xl font-black text-white font-mono">
                  {dnaData?.overall_mastery ?? 0}%
                </span>
              </div>
              <div className="text-center p-2 border-l border-white/10">
                <span className="text-[10px] uppercase font-bold text-emerald-400 block">🟢 Mastered</span>
                <span className="text-2xl sm:text-3xl font-black text-emerald-400 font-mono">
                  {dnaData?.mastered_count ?? 0}
                </span>
              </div>
              <div className="text-center p-2 border-l border-white/10">
                <span className="text-[10px] uppercase font-bold text-amber-400 block">🟡 Developing</span>
                <span className="text-2xl sm:text-3xl font-black text-amber-400 font-mono">
                  {dnaData?.developing_count ?? 0}
                </span>
              </div>
              <div className="text-center p-2 border-l border-white/10">
                <span className="text-[10px] uppercase font-bold text-rose-400 block">🔴 Needs Attention</span>
                <span className="text-2xl sm:text-3xl font-black text-rose-400 font-mono">
                  {dnaData?.weak_count ?? 0}
                </span>
              </div>
            </div>
          </div>
        </div>

        {/* LOADING & ERROR STATES */}
        {dnaLoading ? (
          <GlassCard className="p-12 text-center space-y-4 shadow-sm animate-pulse">
            <RefreshCw className="w-8 h-8 text-cyan-400 animate-spin mx-auto" />
            <p className="text-sm font-semibold text-slate-200">Synthesizing your Knowledge DNA graph...</p>
            <p className="text-xs text-slate-400">Evaluating quiz performance, accuracy trends, and prerequisite linkages.</p>
          </GlassCard>
        ) : dnaError ? (
          <GlassCard className="p-8 text-center text-rose-400 space-y-3 border-rose-500/30 bg-rose-950/20">
            <AlertCircle className="w-8 h-8 text-rose-400 mx-auto" />
            <h3 className="font-bold text-base text-white">Unable to load Knowledge DNA</h3>
            <p className="text-xs text-rose-300 max-w-md mx-auto">
              {(dnaError as any)?.message || "A network or server error occurred while retrieving cognitive analytics."}
            </p>
            <button
              onClick={() => refetchDNA()}
              className="mt-2 inline-flex items-center gap-1.5 px-4 py-2 rounded-xl bg-rose-600 hover:bg-rose-500 text-white font-bold text-xs shadow-sm transition"
            >
              <RefreshCw className="w-3.5 h-3.5" />
              <span>Retry</span>
            </button>
          </GlassCard>
        ) : dnaData ? (
          <>
            {/* SPECTRA RECOMMENDS FOCUS BANNER */}
            {dnaData.recommended_focus && (
              <div className="rounded-3xl border border-cyan-500/40 bg-gradient-to-r from-[#0B1530] via-[#101436] to-[#150D2E] p-6 shadow-[0_0_30px_rgba(6,182,212,0.15)] backdrop-blur-2xl">
                <div className="flex flex-col md:flex-row md:items-center justify-between gap-6">
                  <div className="space-y-2 max-w-2xl">
                    <div className="flex items-center gap-2">
                      <div className="w-7 h-7 rounded-xl bg-cyan-500 text-black flex items-center justify-center font-bold shadow-[0_0_12px_#22d3ee]">
                        <Sparkles className="w-4 h-4" />
                      </div>
                      <span className="text-xs uppercase font-extrabold tracking-wider text-cyan-300">
                        SPECTRA Recommends Highest Leverage Focus
                      </span>
                    </div>

                    <h2 className="text-xl sm:text-2xl font-black text-white">
                      Focus on {dnaData.recommended_focus.topic_name}
                    </h2>

                    <p className="text-xs sm:text-sm text-slate-300 leading-relaxed font-normal">
                      {dnaData.recommended_focus.reason}
                    </p>

                    {dnaData.recommended_focus.prerequisite_impact && (
                      <p className="text-xs text-amber-300 font-semibold flex items-center gap-1.5">
                        <AlertTriangle className="w-3.5 h-3.5 text-amber-400 shrink-0" />
                        <span>{dnaData.recommended_focus.prerequisite_impact}</span>
                      </p>
                    )}
                  </div>

                  <div className="flex flex-col sm:flex-row items-stretch sm:items-center gap-3 shrink-0">
                    <button
                      onClick={() => setSelectedTopicId(dnaData.recommended_focus!.topic_id)}
                      className="px-4 py-2.5 rounded-xl border border-white/10 bg-white/[0.05] hover:bg-white/10 text-cyan-300 text-xs font-bold transition shadow-sm"
                    >
                      Inspect in Graph
                    </button>

                    {dnaData.recommended_focus.lesson_id ? (
                      <Link
                        href={`/student/lessons/${dnaData.recommended_focus.lesson_id}`}
                        className="px-5 py-2.5 rounded-xl bg-gradient-to-r from-cyan-500 to-indigo-600 hover:from-cyan-400 hover:to-indigo-500 text-black text-xs font-black shadow-[0_0_20px_rgba(6,182,212,0.3)] flex items-center justify-center gap-2 transition"
                      >
                        <span>Start Learning</span>
                        <ArrowRight className="w-4 h-4 text-black" />
                      </Link>
                    ) : (
                      <Link
                        href={`/student/subjects/${dnaData.subject_id}`}
                        className="px-5 py-2.5 rounded-xl bg-gradient-to-r from-cyan-500 to-indigo-600 hover:from-cyan-400 hover:to-indigo-500 text-black text-xs font-black shadow-[0_0_20px_rgba(6,182,212,0.3)] flex items-center justify-center gap-2 transition"
                      >
                        <span>Open Curriculum Track</span>
                        <ArrowRight className="w-4 h-4 text-black" />
                      </Link>
                    )}
                  </div>
                </div>
              </div>
            )}

            {/* MAIN INTERACTIVE KNOWLEDGE DNA SECTION: GRAPH + DETAIL PANEL */}
            <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
              {/* LEFT/MAIN: INTERACTIVE KNOWLEDGE GRAPH (7 COLS) */}
              <div className="lg:col-span-7 space-y-4">
                <div className="flex items-center justify-between">
                  <div>
                    <h3 className="text-lg font-bold text-slate-900 dark:text-white flex items-center gap-2">
                      <Compass className="w-5 h-5 text-cyan-500 dark:text-cyan-400" />
                      <span>Knowledge DNA Map</span>
                    </h3>
                    <p className="text-xs text-slate-600 dark:text-slate-400 mt-0.5">
                      Click any topic node to inspect cognitive evidence, root causes, and curated videos.
                    </p>
                  </div>

                  <button
                    onClick={() => refetchDNA()}
                    disabled={dnaFetching}
                    className="p-2 rounded-xl border border-slate-200 dark:border-white/10 hover:bg-slate-100 dark:hover:bg-white/5 text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white text-xs transition"
                    title="Refresh Knowledge DNA"
                  >
                    <RefreshCw className={`w-4 h-4 ${dnaFetching ? "animate-spin text-cyan-400" : ""}`} />
                  </button>
                </div>

                {/* GRAPH CANVAS / FLOW DIAGRAM */}
                <GlassCard className="p-5 sm:p-7 space-y-4">
                  {/* Legend */}
                  <div className="flex flex-wrap items-center justify-center gap-4 pb-4 border-b border-slate-200 dark:border-white/[0.06] text-[11px] font-semibold text-slate-600 dark:text-slate-400">
                    <span className="inline-flex items-center gap-1.5 text-emerald-600 dark:text-emerald-300">
                      <span className="w-2.5 h-2.5 rounded-full bg-emerald-400 shadow-[0_0_8px_#34d399]" /> Mastered (80%+)
                    </span>
                    <span className="inline-flex items-center gap-1.5 text-amber-600 dark:text-amber-300">
                      <span className="w-2.5 h-2.5 rounded-full bg-amber-400 shadow-[0_0_8px_#fbbf24]" /> Developing (50–79%)
                    </span>
                    <span className="inline-flex items-center gap-1.5 text-rose-600 dark:text-rose-300">
                      <span className="w-2.5 h-2.5 rounded-full bg-rose-400 shadow-[0_0_8px_#f43f5e]" /> Needs Attention (&lt;50%)
                    </span>
                    <span className="inline-flex items-center gap-1.5 text-slate-500 dark:text-slate-400">
                      <span className="w-2.5 h-2.5 rounded-full bg-slate-400 dark:bg-slate-600" /> Not Started / Locked
                    </span>
                  </div>

                  {/* Sequential Prerequisite Chain Nodes */}
                  <div className="space-y-3 pt-2">
                    {dnaData.nodes.map((node, idx) => {
                      const colors = getStatusColor(node.mastery_state);
                      const isSelected = node.id === activeTopicId;
                      const hasGap = node.prerequisite_gap;

                      return (
                        <React.Fragment key={node.id}>
                          {idx > 0 && (
                            <div className="flex items-center justify-center py-0.5">
                              <div className="flex items-center gap-1.5 px-2.5 py-0.5 rounded-full bg-slate-100 dark:bg-[#080D1F] border border-slate-200 dark:border-white/10 text-[10px] font-bold text-slate-600 dark:text-slate-400">
                                <ArrowDown className="w-3 h-3 text-cyan-500 dark:text-cyan-400" />
                                <span>Prerequisite Link</span>
                              </div>
                            </div>
                          )}

                          <div
                            onClick={() => setSelectedTopicId(node.id)}
                            className={`group relative cursor-pointer rounded-2xl border-2 p-4 transition-all duration-200 ${
                              isSelected
                                ? "border-cyan-500 dark:border-cyan-400 bg-cyan-50 dark:bg-cyan-950/30 ring-4 ring-cyan-500/20 shadow-[0_0_25px_rgba(6,182,212,0.25)] scale-[1.01]"
                                : `${colors.border} bg-white/90 dark:bg-[#090E20]/90 border-slate-200 dark:border-white/[0.08] hover:border-cyan-500/40 hover:shadow-md`
                            }`}
                          >
                            <div className="flex items-center justify-between gap-4">
                              <div className="flex items-center gap-3.5 flex-1 min-w-0">
                                {/* Mastery Indicator Pill */}
                                <div
                                  className={`w-10 h-10 rounded-2xl flex items-center justify-center font-black text-xs text-white shadow-sm shrink-0 ${colors.bg}`}
                                >
                                  {node.mastery_state === "LOCKED" ? (
                                    <Lock className="w-4 h-4 text-white" />
                                  ) : node.mastery_state === "MASTERED" ? (
                                    <CheckCircle2 className="w-5 h-5 text-white" />
                                  ) : (
                                    `${Math.round(node.mastery_score)}%`
                                  )}
                                </div>

                                <div className="flex-1 min-w-0">
                                  <div className="flex items-center gap-2 flex-wrap">
                                    <span className="text-[10px] uppercase font-bold text-slate-500 dark:text-slate-400 tracking-wider">
                                      Lesson {node.lesson_order}
                                    </span>
                                    <span className={`text-[10px] font-extrabold uppercase px-2 py-0.5 rounded-md border ${colors.pill}`}>
                                      {colors.label}
                                    </span>
                                    {hasGap && (
                                      <span className="text-[10px] font-bold px-2 py-0.5 rounded-md bg-rose-500/15 text-rose-600 dark:text-rose-300 border border-rose-500/30 flex items-center gap-1">
                                        <AlertTriangle className="w-3 h-3 text-rose-500 shrink-0" /> Gap Detected
                                      </span>
                                    )}
                                  </div>

                                  <h4 className="text-sm font-bold text-slate-900 dark:text-white truncate mt-0.5 group-hover:text-cyan-600 dark:group-hover:text-cyan-300 transition-colors">
                                    {node.name}
                                  </h4>

                                  {node.description && (
                                    <p className="text-[11px] text-slate-500 dark:text-slate-400 line-clamp-1 mt-0.5">
                                      {node.description}
                                    </p>
                                  )}
                                </div>
                              </div>

                              <div className="flex items-center gap-2 shrink-0">
                                <div className="text-right hidden sm:block">
                                  <span className="text-xs font-black text-slate-900 dark:text-white font-mono block">
                                    {node.mastery_score}%
                                  </span>
                                  <span className="text-[10px] text-slate-500 dark:text-slate-400">
                                    {node.attempts_count} quiz attempts
                                  </span>
                                </div>
                                <ChevronRight className={`w-4 h-4 text-slate-400 transition-transform ${isSelected ? "rotate-90 text-cyan-500 dark:text-cyan-400" : "group-hover:translate-x-0.5"}`} />
                              </div>
                            </div>
                          </div>
                        </React.Fragment>
                      );
                    })}
                  </div>
                </GlassCard>
              </div>

              {/* RIGHT: TOPIC DETAIL PANEL (5 COLS) */}
              <div className="lg:col-span-5 space-y-6 sticky top-20">
                {selectedNode ? (
                  <GlassCard className="p-6 space-y-5">
                    {/* Header */}
                    <div className="space-y-2 border-b border-slate-200 dark:border-white/[0.08] pb-4">
                      <div className="flex items-center justify-between gap-2">
                        <span className="text-[10px] uppercase font-bold tracking-wider text-slate-500 dark:text-slate-400">
                          Topic Cognitive Profile
                        </span>
                        <span className={`text-xs font-bold px-2.5 py-0.5 rounded-full border ${getStatusColor(selectedNode.mastery_state).pill}`}>
                          {getStatusColor(selectedNode.mastery_state).label}
                        </span>
                      </div>

                      <h3 className="text-lg font-bold text-slate-900 dark:text-white leading-tight">
                        {selectedNode.name}
                      </h3>

                      {selectedNode.description && (
                        <p className="text-xs text-slate-600 dark:text-slate-300 leading-relaxed">
                          {selectedNode.description}
                        </p>
                      )}
                    </div>

                    {/* Cognitive Evidence Stats Grid (Quiz, Puzzle, Lessons) */}
                    <div className="space-y-2">
                      <span className="text-[10px] uppercase font-bold tracking-wider text-slate-500 dark:text-slate-400 block">
                        Cognitive Evidence &amp; Mastery Breakdown
                      </span>
                      <div className="grid grid-cols-3 gap-2.5">
                        {/* Mastery Score */}
                        <div className="p-3 rounded-2xl bg-slate-50 dark:bg-[#090E20] border border-slate-200/90 dark:border-white/[0.08] flex flex-col justify-between">
                          <span className="text-[10px] uppercase font-bold text-slate-500 dark:text-slate-400 block truncate">Track Mastery</span>
                          <span className="text-lg font-black text-slate-900 dark:text-white font-mono mt-1 block">{selectedNode.mastery_score}%</span>
                          <div className="w-full h-1.5 bg-slate-200 dark:bg-slate-800 rounded-full mt-2 overflow-hidden">
                            <div
                              className={`h-full rounded-full ${getStatusColor(selectedNode.mastery_state).bg}`}
                              style={{ width: `${selectedNode.mastery_score}%` }}
                            />
                          </div>
                        </div>

                        {/* Quiz Score & Accuracy */}
                        <div className="p-3 rounded-2xl bg-slate-50 dark:bg-[#090E20] border border-slate-200/90 dark:border-white/[0.08] flex flex-col justify-between">
                          <span className="text-[10px] uppercase font-bold text-slate-500 dark:text-slate-400 block truncate">Quiz Accuracy</span>
                          <span className="text-lg font-black text-slate-900 dark:text-white font-mono mt-1 block">
                            {selectedNode.recent_quiz_score !== null && selectedNode.recent_quiz_score !== undefined
                              ? `${selectedNode.recent_quiz_score}%`
                              : "—"}
                          </span>
                          <span className="text-[10px] text-slate-500 dark:text-slate-400 mt-1 block truncate">
                            {selectedNode.attempts_count} {selectedNode.attempts_count === 1 ? "attempt" : "attempts"}
                          </span>
                        </div>

                        {/* Puzzle Accuracy & Solves */}
                        <div className="p-3 rounded-2xl bg-purple-500/10 dark:bg-purple-950/20 border border-purple-500/30 flex flex-col justify-between">
                          <span className="text-[10px] uppercase font-bold text-purple-700 dark:text-purple-300 block truncate flex items-center gap-1">
                            <Puzzle className="w-3 h-3 text-purple-500 dark:text-purple-400 shrink-0" />
                            <span>Puzzle Accuracy</span>
                          </span>
                          <span className="text-lg font-black text-purple-700 dark:text-purple-300 font-mono mt-1 block">
                            {topicDetail?.puzzle_accuracy !== null && topicDetail?.puzzle_accuracy !== undefined
                              ? `${topicDetail.puzzle_accuracy}%`
                              : topicDetail?.puzzle_solved_count && topicDetail.puzzle_solved_count > 0
                              ? "100%"
                              : "—"}
                          </span>
                          <span className="text-[10px] text-purple-600 dark:text-purple-400 font-semibold mt-1 block truncate">
                            {topicDetail?.puzzle_solved_count ?? 0}/{topicDetail?.puzzle_total_count ?? 0} solved
                          </span>
                        </div>
                      </div>
                    </div>

                    {/* "WHY IS THIS WEAK?" EXPLANATION CARD */}
                    {selectedNode.why_weak_explanation && (
                      <div className={`p-4 rounded-2xl border text-xs space-y-1.5 ${
                        selectedNode.mastery_state === "WEAK"
                          ? "bg-rose-950/30 border-rose-500/30 text-rose-200"
                          : selectedNode.mastery_state === "DEVELOPING"
                          ? "bg-amber-950/30 border-amber-500/30 text-amber-200"
                          : "bg-slate-900/50 border-white/10 text-slate-300"
                      }`}>
                        <div className="flex items-center gap-1.5 font-bold uppercase tracking-wider text-[11px]">
                          <AlertCircle className="w-4 h-4 text-rose-400 shrink-0" />
                          <span>Why is this topic {selectedNode.mastery_state.toLowerCase()}?</span>
                        </div>
                        <p className="leading-relaxed">
                          {selectedNode.why_weak_explanation}
                        </p>
                      </div>
                    )}

                    {/* PREREQUISITES LIST */}
                    {selectedNode.prerequisite_names.length > 0 && (
                      <div className="space-y-2 pt-1 border-t border-slate-200 dark:border-white/[0.08]">
                        <span className="text-xs font-bold text-slate-900 dark:text-white block">
                          Prerequisites for this Topic:
                        </span>
                        <div className="space-y-1.5">
                          {topicDetail?.prerequisites && topicDetail.prerequisites.length > 0 ? (
                            topicDetail.prerequisites.map((p) => {
                              const pCol = getStatusColor(p.mastery_state);
                              return (
                                <div
                                  key={p.topic_id}
                                  onClick={() => setSelectedTopicId(p.topic_id)}
                                  className="flex items-center justify-between p-2.5 rounded-xl border border-slate-200 dark:border-white/10 hover:border-cyan-500/40 hover:bg-slate-50 dark:hover:bg-white/[0.04] cursor-pointer text-xs transition"
                                >
                                  <span className="font-semibold text-slate-800 dark:text-slate-200">{p.name}</span>
                                  <span className={`text-[10px] font-bold px-2 py-0.5 rounded-md border ${pCol.pill}`}>
                                    {p.mastery_score}% {pCol.label}
                                  </span>
                                </div>
                              );
                            })
                          ) : (
                            selectedNode.prerequisite_names.map((pName, i) => (
                              <div
                                key={i}
                                className="flex items-center justify-between p-2 rounded-xl bg-slate-100 dark:bg-white/[0.03] text-xs font-semibold text-slate-700 dark:text-slate-300"
                              >
                                <span>{pName}</span>
                                <span className="text-[10px] text-slate-500 dark:text-slate-400">Required</span>
                              </div>
                            ))
                          )}
                        </div>
                      </div>
                    )}

                    {/* ACTION PLAN */}
                    {selectedNode.recommended_action && (
                      <div className="p-4 rounded-2xl bg-cyan-500/10 dark:bg-cyan-950/20 border border-cyan-500/30 space-y-1.5">
                        <span className="text-[10px] uppercase font-bold text-cyan-700 dark:text-cyan-300 tracking-wider block">
                          Recommended Action Path
                        </span>
                        <p className="text-xs font-semibold text-slate-900 dark:text-white">
                          {selectedNode.recommended_action}
                        </p>
                      </div>
                    )}

                    {/* ACTION BUTTON */}
                    {selectedNode.lesson_id ? (
                      <Link
                        href={`/student/lessons/${selectedNode.lesson_id}`}
                        className="w-full py-3 px-4 rounded-2xl bg-gradient-to-r from-cyan-500 to-indigo-600 hover:from-cyan-400 hover:to-indigo-500 text-black font-extrabold text-xs shadow-[0_0_20px_rgba(6,182,212,0.3)] flex items-center justify-center gap-2 transition"
                      >
                        <BookOpen className="w-4 h-4 text-black" />
                        <span>Start Recommended Learning</span>
                      </Link>
                    ) : (
                      <Link
                        href={`/student/subjects/${dnaData.subject_id}`}
                        className="w-full py-3 px-4 rounded-2xl bg-gradient-to-r from-cyan-500 to-indigo-600 hover:from-cyan-400 hover:to-indigo-500 text-black font-extrabold text-xs shadow-[0_0_20px_rgba(6,182,212,0.3)] flex items-center justify-center gap-2 transition"
                      >
                        <BookOpen className="w-4 h-4 text-black" />
                        <span>Open Subject Curriculum</span>
                      </Link>
                    )}

                    {/* LEARN THIS CONCEPT: INTEGRATED YOUTUBE RECOMMENDATIONS */}
                    {topicDetail?.youtube_videos && topicDetail.youtube_videos.length > 0 && (
                      <div className="pt-4 border-t border-slate-200 dark:border-white/[0.08] space-y-3">
                        <div className="flex items-center justify-between">
                          <span className="text-xs font-bold text-slate-900 dark:text-white flex items-center gap-1.5">
                            <Play className="w-3.5 h-3.5 text-rose-500 fill-rose-500" />
                            <span>Recommended Video Explanations</span>
                          </span>
                          <span className="text-[10px] text-slate-500 dark:text-slate-400 font-semibold">Curated</span>
                        </div>

                        <div className="space-y-2.5">
                          {topicDetail.youtube_videos.map((vid) => (
                            <a
                              key={vid.video_id}
                              href={vid.url}
                              target="_blank"
                              rel="noopener noreferrer"
                              className="group p-2.5 rounded-2xl border border-slate-200 dark:border-white/10 hover:border-rose-400/40 hover:bg-rose-500/10 flex items-center gap-3 transition"
                            >
                              <div className="relative w-16 h-11 rounded-lg bg-slate-900 overflow-hidden shrink-0">
                                {vid.thumbnail_url ? (
                                  <img
                                    src={vid.thumbnail_url}
                                    alt={vid.title}
                                    className="w-full h-full object-cover group-hover:scale-105 transition"
                                    loading="lazy"
                                  />
                                ) : (
                                  <div className="w-full h-full flex items-center justify-center text-white">
                                    <Play className="w-4 h-4 fill-white" />
                                  </div>
                                )}
                              </div>
                              <div className="flex-1 min-w-0">
                                <h5 className="text-[11px] font-bold text-slate-900 dark:text-white truncate group-hover:text-rose-500 dark:group-hover:text-rose-400 transition">
                                  {vid.title}
                                </h5>
                                <p className="text-[10px] text-slate-500 dark:text-slate-400 mt-0.5">
                                  {vid.channel_name} &bull; {vid.duration || "Visual Guide"}
                                </p>
                              </div>
                              <ExternalLink className="w-3.5 h-3.5 text-slate-400 group-hover:text-rose-500 dark:group-hover:text-rose-400 shrink-0" />
                            </a>
                          ))}
                        </div>
                      </div>
                    )}
                  </GlassCard>
                ) : (
                  <GlassCard className="p-8 text-center text-slate-400">
                    <Compass className="w-8 h-8 text-slate-500 mx-auto mb-2" />
                    <p className="text-xs font-semibold">Select a topic node from the graph to inspect cognitive evidence.</p>
                  </GlassCard>
                )}
              </div>
            </div>

            {/* KNOWLEDGE DNA PROFILE SUMMARY CARDS (3 COLUMNS) */}
            <div className="space-y-4 pt-4 border-t border-slate-200 dark:border-white/[0.08]">
              <div>
                <h3 className="text-lg font-bold text-slate-900 dark:text-white flex items-center gap-2">
                  <Layers className="w-5 h-5 text-cyan-500 dark:text-cyan-400" />
                  <span>Your Knowledge Profile Breakdown</span>
                </h3>
                <p className="text-xs text-slate-600 dark:text-slate-400 mt-0.5">
                  Click any topic card to highlight it within the Knowledge DNA map and view its action plan.
                </p>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                {/* 1. Strong Areas */}
                <div className="rounded-3xl border border-emerald-500/30 bg-emerald-500/10 dark:bg-emerald-950/15 p-5 space-y-3 backdrop-blur-xl">
                  <div className="flex items-center justify-between">
                    <span className="text-xs font-bold text-emerald-700 dark:text-emerald-300 flex items-center gap-1.5">
                      <span className="w-2.5 h-2.5 rounded-full bg-emerald-400 shadow-[0_0_8px_#34d399]" />
                      <span>Strong Areas ({dnaData.strong_areas.length})</span>
                    </span>
                    <span className="text-[11px] font-extrabold text-emerald-700 dark:text-emerald-300 bg-emerald-500/20 border border-emerald-500/30 px-2 py-0.5 rounded-full font-mono">
                      80%+ Mastery
                    </span>
                  </div>

                  <div className="space-y-2">
                    {dnaData.strong_areas.length > 0 ? (
                      dnaData.strong_areas.map((node) => (
                        <div
                          key={node.id}
                          onClick={() => setSelectedTopicId(node.id)}
                          className={`p-3 rounded-2xl border transition-all cursor-pointer ${
                            activeTopicId === node.id
                              ? "border-emerald-500 dark:border-emerald-400 bg-emerald-100/60 dark:bg-emerald-950/40 shadow-sm ring-2 ring-emerald-400/20"
                              : "border-slate-200/80 dark:border-white/10 bg-white/90 dark:bg-[#090E20]/90 hover:border-emerald-400/50"
                          }`}
                        >
                          <div className="flex items-center justify-between">
                            <span className="text-xs font-bold text-slate-900 dark:text-white">{node.name}</span>
                            <span className="text-xs font-black text-emerald-600 dark:text-emerald-400 font-mono">{node.mastery_score}%</span>
                          </div>
                          <span className="text-[10px] text-slate-500 dark:text-slate-400 block mt-0.5">
                            {node.attempts_count} quiz attempts &bull; Lesson {node.lesson_order}
                          </span>
                        </div>
                      ))
                    ) : (
                      <p className="text-xs text-slate-500 dark:text-slate-400 py-3 text-center">No topics mastered yet. Score 80%+ on quizzes to add topics here.</p>
                    )}
                  </div>
                </div>

                {/* 2. Developing */}
                <div className="rounded-3xl border border-amber-500/30 bg-amber-500/10 dark:bg-amber-950/15 p-5 space-y-3 backdrop-blur-xl">
                  <div className="flex items-center justify-between">
                    <span className="text-xs font-bold text-amber-700 dark:text-amber-300 flex items-center gap-1.5">
                      <span className="w-2.5 h-2.5 rounded-full bg-amber-400 shadow-[0_0_8px_#fbbf24]" />
                      <span>Developing ({dnaData.developing_areas.length})</span>
                    </span>
                    <span className="text-[11px] font-extrabold text-amber-700 dark:text-amber-300 bg-amber-500/20 border border-amber-500/30 px-2 py-0.5 rounded-full font-mono">
                      50–79% Mastery
                    </span>
                  </div>

                  <div className="space-y-2">
                    {dnaData.developing_areas.length > 0 ? (
                      dnaData.developing_areas.map((node) => (
                        <div
                          key={node.id}
                          onClick={() => setSelectedTopicId(node.id)}
                          className={`p-3 rounded-2xl border transition-all cursor-pointer ${
                            activeTopicId === node.id
                              ? "border-amber-500 dark:border-amber-400 bg-amber-100/60 dark:bg-amber-950/40 shadow-sm ring-2 ring-amber-400/20"
                              : "border-slate-200/80 dark:border-white/10 bg-white/90 dark:bg-[#090E20]/90 hover:border-amber-400/50"
                          }`}
                        >
                          <div className="flex items-center justify-between">
                            <span className="text-xs font-bold text-slate-900 dark:text-white">{node.name}</span>
                            <span className="text-xs font-black text-amber-600 dark:text-amber-400 font-mono">{node.mastery_score}%</span>
                          </div>
                          <span className="text-[10px] text-slate-500 dark:text-slate-400 block mt-0.5">
                            In progress &bull; Lesson {node.lesson_order}
                          </span>
                        </div>
                      ))
                    ) : (
                      <p className="text-xs text-slate-500 dark:text-slate-400 py-3 text-center">No developing topics.</p>
                    )}
                  </div>
                </div>

                {/* 3. Needs Attention */}
                <div className="rounded-3xl border border-rose-500/30 bg-rose-500/10 dark:bg-rose-950/15 p-5 space-y-3 backdrop-blur-xl">
                  <div className="flex items-center justify-between">
                    <span className="text-xs font-bold text-rose-700 dark:text-rose-300 flex items-center gap-1.5">
                      <span className="w-2.5 h-2.5 rounded-full bg-rose-400 shadow-[0_0_8px_#f43f5e]" />
                      <span>Needs Attention ({dnaData.weak_areas.length})</span>
                    </span>
                    <span className="text-[11px] font-extrabold text-rose-700 dark:text-rose-300 bg-rose-500/20 border border-rose-500/30 px-2 py-0.5 rounded-full font-mono">
                      &lt;50% Mastery
                    </span>
                  </div>

                  <div className="space-y-2">
                    {dnaData.weak_areas.length > 0 ? (
                      dnaData.weak_areas.map((node) => (
                        <div
                          key={node.id}
                          onClick={() => setSelectedTopicId(node.id)}
                          className={`p-3 rounded-2xl border transition-all cursor-pointer ${
                            activeTopicId === node.id
                              ? "border-rose-500 dark:border-rose-400 bg-rose-100/60 dark:bg-rose-950/40 shadow-sm ring-2 ring-rose-400/20"
                              : "border-slate-200/80 dark:border-white/10 bg-white/90 dark:bg-[#090E20]/90 hover:border-rose-400/50"
                          }`}
                        >
                          <div className="flex items-center justify-between">
                            <span className="text-xs font-bold text-slate-900 dark:text-white">{node.name}</span>
                            <span className="text-xs font-black text-rose-600 dark:text-rose-400 font-mono">{node.mastery_score}%</span>
                          </div>
                          <span className="text-[10px] text-rose-600 dark:text-rose-400 font-semibold block mt-0.5">
                            {node.prerequisite_gap ? "Prerequisite Gap Detected" : "Low Quiz Accuracy"}
                          </span>
                        </div>
                      ))
                    ) : (
                      <p className="text-xs text-slate-500 dark:text-slate-400 py-3 text-center">No weak topics! Great job maintaining mastery.</p>
                    )}
                  </div>
                </div>
              </div>
            </div>
          </>
        ) : null}
      </div>
    </RoleLayout>
  );
}
