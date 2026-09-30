"use client";

import React from "react";
import Link from "next/link";
import { useQuery } from "@tanstack/react-query";
import { studentService, PerformanceHistory, TopicPerformance } from "@/services/student.service";
import { RoleLayout } from "@/components/layout/RoleLayout";
import { Badge } from "@/components/common/Badge";
import { ProgressBar } from "@/components/common/ProgressBar";
import { StatCard } from "@/components/common/StatCard";
import {
  TrendingUp,
  Award,
  BookOpen,
  CheckCircle2,
  AlertCircle,
  BarChart3,
  Flame,
  ArrowRight,
  ShieldCheck,
  AlertTriangle,
  RefreshCw
} from "lucide-react";
import {
  ResponsiveContainer,
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  BarChart,
  Bar
} from "recharts";

export default function StudentProgressPage() {
  const {
    data: overview,
    isLoading: overviewLoading,
    refetch: refetchOverview
  } = useQuery({
    queryKey: ["performanceOverview"],
    queryFn: studentService.getPerformanceOverview,
  });

  const {
    data: topicsData,
    isLoading: topicsLoading,
    refetch: refetchTopics
  } = useQuery<TopicPerformance[]>({
    queryKey: ["topicPerformances"],
    queryFn: studentService.getTopicPerformances,
  });

  const {
    data: history,
    isLoading: historyLoading,
    refetch: refetchHistory
  } = useQuery<PerformanceHistory>({
    queryKey: ["performanceHistory"],
    queryFn: studentService.getPerformanceHistory,
  });

  const rawTopics = topicsData as any;
  const topics: TopicPerformance[] = Array.isArray(rawTopics)
    ? rawTopics
    : Array.isArray(rawTopics?.topics)
    ? rawTopics.topics
    : [];

  const strongTopics: TopicPerformance[] = overview?.strong_topics || topics.filter(t => t.status === "MASTERED");
  const weakTopics: TopicPerformance[] = overview?.weak_topics || topics.filter(t => t.status === "WEAK");
  const inProgressTopics: TopicPerformance[] = topics.filter(t => t.status === "NEEDS_PRACTICE");

  const handleRefreshAll = () => {
    refetchOverview();
    refetchTopics();
    refetchHistory();
  };

  // Responsive chart grid color: light slate in light mode, subtle white in dark mode
  const isDark = typeof document !== "undefined" && document.documentElement.classList.contains("dark");
  const gridStroke = isDark ? "rgba(255,255,255,0.06)" : "#e2e8f0";

  return (
    <RoleLayout allowedRoles={["STUDENT", "ADMIN"]}>
      <div className="space-y-6">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div>
            <h1 className="text-2xl font-bold tracking-tight text-slate-900 dark:text-slate-100">Learning Analytics &amp; Progress</h1>
            <p className="mt-1 text-sm text-slate-500 dark:text-slate-400">
              Real-time analytics evaluating your cognitive mastery curve, performance trends, and knowledge retention.
            </p>
          </div>

          <button
            onClick={handleRefreshAll}
            className="inline-flex items-center gap-1.5 rounded-xl border border-slate-200 dark:border-white/[0.08] bg-white dark:bg-white/[0.04] px-3.5 py-2 text-xs font-semibold text-slate-700 dark:text-slate-200 shadow-sm hover:bg-slate-50 dark:hover:bg-white/[0.08] transition self-start sm:self-center"
          >
            <RefreshCw className="h-3.5 w-3.5 text-slate-500 dark:text-slate-400" />
            <span>Refresh Analytics</span>
          </button>
        </div>

        {/* Overview Stat Cards */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          <StatCard
            title="Curriculum Progress"
            value={`${overview?.overall_progress || 0}%`}
            subtitle={`${overview?.lessons_completed || 0} of ${overview?.total_lessons || 0} modules`}
            icon={TrendingUp}
            color="brand"
          />
          <StatCard
            title="Average Assessment Score"
            value={`${overview?.average_quiz_score || 0}%`}
            subtitle={`${overview?.total_quizzes_taken || 0} total assessments taken`}
            icon={Award}
            color="emerald"
          />
          <StatCard
            title="Mastered Topics"
            value={strongTopics.length}
            subtitle="Demonstrated high topic mastery"
            icon={ShieldCheck}
            color="cyan"
          />
          <StatCard
            title="Knowledge Gaps"
            value={weakTopics.length}
            subtitle="Topics prioritized for practice"
            icon={AlertTriangle}
            color="amber"
          />
        </div>

        {/* Strong & Weak Areas Classified */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {/* Strong Areas */}
          <div className="rounded-3xl border border-emerald-200/80 dark:border-emerald-500/20 bg-white dark:bg-[#0B1124]/85 dark:backdrop-blur-xl p-6 shadow-sm">
            <div className="flex items-center justify-between mb-4">
              <div className="flex items-center gap-2">
                <div className="flex h-8 w-8 items-center justify-center rounded-xl bg-emerald-50 dark:bg-emerald-500/10 text-emerald-600 border border-emerald-200 dark:border-emerald-500/20">
                  <ShieldCheck className="h-4 w-4" />
                </div>
                <div>
                  <h3 className="font-bold text-slate-900 dark:text-slate-100 text-sm">Strong Mastery Areas</h3>
                  <p className="text-xs text-slate-500 dark:text-slate-400">Topics where mastery exceeds 75%</p>
                </div>
              </div>
              <Badge variant="emerald" size="sm">
                {strongTopics.length} Topics
              </Badge>
            </div>

            {strongTopics.length > 0 ? (
              <div className="space-y-3">
                {strongTopics.map((item) => (
                  <div
                    key={item.topic_id}
                    className="flex items-center justify-between p-3.5 rounded-2xl border border-emerald-100 dark:border-emerald-500/10 bg-emerald-50/40 dark:bg-emerald-500/[0.06]"
                  >
                    <div>
                      <h4 className="text-xs font-bold text-slate-900 dark:text-slate-100">{item.topic_name}</h4>
                      <span className="text-[11px] text-slate-500 dark:text-slate-400">{item.subject_name}</span>
                    </div>
                    <div className="text-right">
                      <span className="text-xs font-bold text-emerald-700 dark:text-emerald-400">{item.mastery_score}% Mastery</span>
                      <span className="block text-[10px] text-slate-400 dark:text-slate-500">{item.accuracy}% Accuracy</span>
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <p className="text-xs text-slate-400 dark:text-slate-500 py-4 text-center">
                No topics mastered yet. Score 75% or higher on assessments to unlock strong areas!
              </p>
            )}
          </div>

          {/* Weak Areas */}
          <div className="rounded-3xl border border-amber-200/80 dark:border-amber-500/20 bg-white dark:bg-[#0B1124]/85 dark:backdrop-blur-xl p-6 shadow-sm">
            <div className="flex items-center justify-between mb-4">
              <div className="flex items-center gap-2">
                <div className="flex h-8 w-8 items-center justify-center rounded-xl bg-rose-50 dark:bg-rose-500/10 text-rose-600 border border-rose-200 dark:border-rose-500/20">
                  <AlertTriangle className="h-4 w-4" />
                </div>
                <div>
                  <h3 className="font-bold text-slate-900 dark:text-slate-100 text-sm">Identified Knowledge Gaps</h3>
                  <p className="text-xs text-slate-500 dark:text-slate-400">Topics below 60% needing targeted reinforcement</p>
                </div>
              </div>
              <Badge variant="rose" size="sm">
                {weakTopics.length} Gaps
              </Badge>
            </div>

            {weakTopics.length > 0 ? (
              <div className="space-y-3">
                {weakTopics.map((item) => (
                  <div
                    key={item.topic_id}
                    className="flex items-center justify-between p-3.5 rounded-2xl border border-rose-100 dark:border-rose-500/10 bg-rose-50/40 dark:bg-rose-500/[0.06]"
                  >
                    <div>
                      <h4 className="text-xs font-bold text-slate-900 dark:text-slate-100">{item.topic_name}</h4>
                      <span className="text-[11px] text-slate-500 dark:text-slate-400">{item.subject_name}</span>
                    </div>
                    <div className="flex items-center gap-3">
                      <div className="text-right">
                        <span className="text-xs font-bold text-rose-700 dark:text-rose-400">{item.mastery_score}%</span>
                        <span className="block text-[10px] text-slate-400 dark:text-slate-500">{item.accuracy}% Acc</span>
                      </div>
                      <Link
                        href="/student/quizzes/1"
                        className="rounded-lg bg-rose-600 px-2.5 py-1 text-[11px] font-bold text-white shadow-sm hover:bg-rose-700"
                      >
                        Practice
                      </Link>
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <p className="text-xs text-emerald-700 dark:text-emerald-400 py-4 text-center font-medium">
                No active knowledge gaps detected! Keep practicing to maintain mastery.
              </p>
            )}
          </div>
        </div>

        {/* Charts Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Chart 1: Performance Over Time */}
          <div className="rounded-3xl border border-slate-200 dark:border-white/[0.08] bg-white dark:bg-[#0B1124]/85 dark:backdrop-blur-xl p-6 shadow-sm">
            <div className="flex items-center justify-between mb-4">
              <div>
                <h3 className="font-bold text-slate-900 dark:text-slate-100">Performance Over Time</h3>
                <p className="text-xs text-slate-500 dark:text-slate-400">Assessment score progression trend</p>
              </div>
              <TrendingUp className="h-5 w-5 text-brand-600" />
            </div>

            <div className="h-64 w-full">
              {history && history.score_trends && history.score_trends.length > 0 ? (
                <ResponsiveContainer width="100%" height="100%">
                  <LineChart data={history.score_trends} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                    <CartesianGrid strokeDasharray="3 3" vertical={false} stroke={gridStroke} />
                    <XAxis dataKey="date" stroke="#94a3b8" fontSize={11} tickLine={false} />
                    <YAxis domain={[0, 100]} stroke="#94a3b8" fontSize={11} tickLine={false} />
                    <Tooltip
                      contentStyle={{
                        backgroundColor: "#0f172a",
                        borderRadius: "12px",
                        color: "#fff",
                        border: "none",
                        fontSize: "12px",
                      }}
                      formatter={(val: any) => [`${val}%`, "Score"]}
                    />
                    <Line
                      type="monotone"
                      dataKey="score"
                      stroke="#4f46e5"
                      strokeWidth={3}
                      dot={{ r: 4, fill: "#4f46e5" }}
                      activeDot={{ r: 6 }}
                    />
                  </LineChart>
                </ResponsiveContainer>
              ) : (
                <div className="flex h-full flex-col items-center justify-center text-center p-6 text-xs text-slate-400 dark:text-slate-500">
                  <Award className="h-8 w-8 text-slate-300 dark:text-slate-600 mb-2" />
                  <span>Take assessments to populate score progression trends.</span>
                </div>
              )}
            </div>
          </div>

          {/* Chart 2: Topic Mastery Comparison */}
          <div className="rounded-3xl border border-slate-200 dark:border-white/[0.08] bg-white dark:bg-[#0B1124]/85 dark:backdrop-blur-xl p-6 shadow-sm">
            <div className="flex items-center justify-between mb-4">
              <div>
                <h3 className="font-bold text-slate-900 dark:text-slate-100">Topic Mastery Distribution</h3>
                <p className="text-xs text-slate-500 dark:text-slate-400">Mastery score comparison across evaluated topics</p>
              </div>
              <BarChart3 className="h-5 w-5 text-secondary-600" />
            </div>

            <div className="h-64 w-full">
              {history && history.topic_mastery && history.topic_mastery.length > 0 ? (
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={history.topic_mastery} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                    <CartesianGrid strokeDasharray="3 3" vertical={false} stroke={gridStroke} />
                    <XAxis dataKey="topic" stroke="#94a3b8" fontSize={10} tickLine={false} interval={0} angle={-15} textAnchor="end" height={50} />
                    <YAxis domain={[0, 100]} stroke="#94a3b8" fontSize={11} tickLine={false} />
                    <Tooltip
                      contentStyle={{
                        backgroundColor: "#0f172a",
                        borderRadius: "12px",
                        color: "#fff",
                        border: "none",
                        fontSize: "12px",
                      }}
                      formatter={(val: any) => [`${val}%`, "Mastery"]}
                    />
                    <Bar dataKey="mastery" fill="#7c3aed" radius={[6, 6, 0, 0]} />
                  </BarChart>
                </ResponsiveContainer>
              ) : (
                <div className="flex h-full flex-col items-center justify-center text-center p-6 text-xs text-slate-400 dark:text-slate-500">
                  <BarChart3 className="h-8 w-8 text-slate-300 dark:text-slate-600 mb-2" />
                  <span>No topic performance evaluated yet. Complete quizzes to compare mastery.</span>
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Detailed Topic Mastery Table */}
        <div className="rounded-3xl border border-slate-200 dark:border-white/[0.08] bg-white dark:bg-[#0B1124]/85 dark:backdrop-blur-xl p-6 shadow-sm">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h3 className="font-bold text-slate-900 dark:text-slate-100">Detailed Topic Mastery Breakdown</h3>
              <p className="text-xs text-slate-500 dark:text-slate-400">Granular tracking of attempts, accuracy, and mastery weights</p>
            </div>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead className="border-b border-slate-200 dark:border-white/[0.06] bg-slate-50 dark:bg-white/[0.03] text-[11px] font-bold uppercase tracking-wider text-slate-400">
                <tr>
                  <th className="px-4 py-3">Topic Name</th>
                  <th className="px-4 py-3">Subject</th>
                  <th className="px-4 py-3">Accuracy</th>
                  <th className="px-4 py-3">Mastery Score</th>
                  <th className="px-4 py-3">Status</th>
                  <th className="px-4 py-3 text-right">Attempts</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100 dark:divide-white/[0.04]">
                {topicsLoading ? (
                  <tr>
                    <td colSpan={6} className="text-center py-8 text-slate-400 dark:text-slate-500">
                      Loading topic performances...
                    </td>
                  </tr>
                ) : topics.length > 0 ? (
                  topics.map((tp) => (
                    <tr key={tp.topic_id} className="hover:bg-slate-50 dark:hover:bg-white/[0.03] transition">
                      <td className="px-4 py-3 font-semibold text-slate-900 dark:text-slate-100">{tp.topic_name}</td>
                      <td className="px-4 py-3 text-slate-500 dark:text-slate-400">{tp.subject_name}</td>
                      <td className="px-4 py-3 font-bold dark:text-slate-200">{tp.accuracy}%</td>
                      <td className="px-4 py-3">
                        <div className="w-28">
                          <ProgressBar
                            progress={tp.mastery_score}
                            size="sm"
                            color={tp.mastery_score >= 70 ? "emerald" : tp.mastery_score >= 50 ? "amber" : "rose"}
                          />
                        </div>
                      </td>
                      <td className="px-4 py-3">
                        <Badge
                          variant={tp.status === "MASTERED" ? "emerald" : tp.status === "NEEDS_PRACTICE" ? "amber" : "rose"}
                          size="sm"
                        >
                          {tp.status === "WEAK" ? "Weak Area" : tp.status === "NEEDS_PRACTICE" ? "In Progress" : "Mastered"}
                        </Badge>
                      </td>
                      <td className="px-4 py-3 text-right font-medium text-slate-500 dark:text-slate-400">{tp.attempts}</td>
                    </tr>
                  ))
                ) : (
                  <tr>
                    <td colSpan={6} className="text-center py-8 text-slate-400 dark:text-slate-500">
                      No topic performance evaluations yet. Take a quiz to populate your diagnostic records!
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </RoleLayout>
  );
}
