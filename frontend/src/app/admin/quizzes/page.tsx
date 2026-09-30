"use client";

import React, { useState } from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { adminService } from "@/services/admin.service";
import { RoleLayout } from "@/components/layout/RoleLayout";
import { Badge } from "@/components/common/Badge";
import { Plus, HelpCircle, FolderKanban, Loader2 } from "lucide-react";

export default function AdminQuizzesPage() {
  const queryClient = useQueryClient();

  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [quizType, setQuizType] = useState("TOPIC_ASSESSMENT");
  const [difficulty, setDifficulty] = useState("MEDIUM");
  const [questionCount, setQuestionCount] = useState(5);
  const [subjectId, setSubjectId] = useState<number | undefined>();
  const [showAddModal, setShowAddModal] = useState(false);

  const { data: quizzes, isLoading } = useQuery({
    queryKey: ["adminQuizzes"],
    queryFn: adminService.getQuizzes,
  });

  const { data: subjects } = useQuery({
    queryKey: ["adminSubjects"],
    queryFn: adminService.getSubjects,
  });

  const createMutation = useMutation({
    mutationFn: () =>
      adminService.createQuiz({
        subject_id: subjectId || (subjects && subjects[0]?.id) || 1,
        title,
        description,
        quiz_type: quizType,
        difficulty,
        question_count: Number(questionCount),
      }),
    onSuccess: () => {
      setShowAddModal(false);
      setTitle("");
      setDescription("");
      queryClient.invalidateQueries({ queryKey: ["adminQuizzes"] });
      queryClient.invalidateQueries({ queryKey: ["adminDashboard"] });
    },
  });

  return (
    <RoleLayout allowedRoles={["ADMIN"]}>
      <div className="space-y-6">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold tracking-tight text-slate-900 dark:text-white">Quiz &amp; Assessment Catalog</h1>
            <p className="mt-1 text-sm text-slate-500 dark:text-slate-400">
              Publish structured and adaptive diagnostics mapped to curriculum subjects.
            </p>
          </div>
          <button
            onClick={() => setShowAddModal(true)}
            className="inline-flex items-center gap-2 rounded-xl bg-brand-600 px-4 py-2 text-xs font-bold text-white shadow hover:bg-brand-700"
          >
            <Plus className="h-4 w-4" />
            <span>Create Quiz</span>
          </button>
        </div>

        {/* Quizzes Table */}
        <div className="rounded-3xl border border-slate-200 dark:border-white/[0.08] bg-white dark:bg-[#0B1124]/85 p-6 shadow-sm">
          {isLoading ? (
            <div className="space-y-3 animate-pulse">
              {[1, 2, 3].map((i) => (
                <div key={i} className="h-16 bg-slate-100 dark:bg-white/[0.04] rounded-xl" />
              ))}
            </div>
          ) : quizzes && quizzes.length > 0 ? (
            <div className="overflow-x-auto">
              <table className="w-full text-left text-xs">
                <thead className="border-b border-slate-200 dark:border-white/[0.06] bg-slate-50 dark:bg-white/[0.03] text-[11px] font-bold uppercase tracking-wider text-slate-400 dark:text-slate-500">
                  <tr>
                    <th className="px-4 py-3">Quiz ID</th>
                    <th className="px-4 py-3">Subject</th>
                    <th className="px-4 py-3">Title</th>
                    <th className="px-4 py-3">Type</th>
                    <th className="px-4 py-3">Questions</th>
                    <th className="px-4 py-3 text-right">Difficulty</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-100 dark:divide-white/[0.04]">
                  {quizzes.map((q: any) => (
                    <tr key={q.id} className="hover:bg-slate-50 dark:hover:bg-white/[0.03] transition">
                      <td className="px-4 py-3.5 font-mono text-slate-400">#{q.id}</td>
                      <td className="px-4 py-3.5 text-slate-500 dark:text-slate-400">{q.subject_name}</td>
                      <td className="px-4 py-3.5 font-bold text-slate-900 dark:text-white">{q.title}</td>
                      <td className="px-4 py-3.5">
                        <Badge variant={q.quiz_type === "ADAPTIVE" ? "cyan" : "brand"} size="sm">
                          {q.quiz_type}
                        </Badge>
                      </td>
                      <td className="px-4 py-3.5 font-semibold text-slate-700 dark:text-slate-300">{q.question_count}</td>
                      <td className="px-4 py-3.5 text-right">
                        <Badge
                          variant={q.difficulty === "EASY" ? "emerald" : q.difficulty === "MEDIUM" ? "brand" : "purple"}
                          size="sm"
                        >
                          {q.difficulty}
                        </Badge>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          ) : (
            <p className="text-xs text-slate-400 py-6 text-center">No quizzes configured yet.</p>
          )}
        </div>

        {/* Create Modal */}
        {showAddModal && (
          <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/50 dark:bg-black/60 backdrop-blur-sm p-4">
            <div className="w-full max-w-md rounded-3xl bg-white dark:bg-[#0B1124] p-6 shadow-xl border border-slate-200 dark:border-white/[0.08]">
              <h3 className="text-lg font-bold text-slate-900 dark:text-white mb-4">Create Assessment Quiz</h3>

              <div className="space-y-3 text-xs">
                <div>
                  <label className="block font-semibold text-slate-700 dark:text-slate-300 mb-1">Subject</label>
                  <select
                    value={subjectId}
                    onChange={(e) => setSubjectId(Number(e.target.value))}
                    className="w-full rounded-xl border border-slate-200 dark:border-white/[0.08] bg-white dark:bg-white/[0.06] text-slate-900 dark:text-white p-2.5 text-xs outline-none focus:border-brand-500 dark:focus:border-cyan-500"
                  >
                    {subjects?.map((s: any) => (
                      <option key={s.id} value={s.id}>{s.name}</option>
                    ))}
                  </select>
                </div>

                <div>
                  <label className="block font-semibold text-slate-700 dark:text-slate-300 mb-1">Quiz Title</label>
                  <input
                    type="text"
                    value={title}
                    onChange={(e) => setTitle(e.target.value)}
                    placeholder="e.g. Java Arrays & Collections Checkpoint"
                    className="w-full rounded-xl border border-slate-200 dark:border-white/[0.08] bg-white dark:bg-white/[0.06] text-slate-900 dark:text-white p-2.5 text-xs outline-none focus:border-brand-500 dark:focus:border-cyan-500 placeholder:text-slate-400 dark:placeholder:text-slate-500"
                  />
                </div>

                <div className="grid grid-cols-2 gap-3">
                  <div>
                    <label className="block font-semibold text-slate-700 dark:text-slate-300 mb-1">Quiz Type</label>
                    <select
                      value={quizType}
                      onChange={(e) => setQuizType(e.target.value)}
                      className="w-full rounded-xl border border-slate-200 dark:border-white/[0.08] bg-white dark:bg-white/[0.06] text-slate-900 dark:text-white p-2 text-xs outline-none"
                    >
                      <option value="TOPIC_ASSESSMENT">TOPIC_ASSESSMENT</option>
                      <option value="ADAPTIVE">ADAPTIVE</option>
                      <option value="PRACTICE">PRACTICE</option>
                    </select>
                  </div>
                  <div>
                    <label className="block font-semibold text-slate-700 dark:text-slate-300 mb-1">Question Count</label>
                    <input
                      type="number"
                      value={questionCount}
                      min={1}
                      max={50}
                      onChange={(e) => setQuestionCount(Number(e.target.value))}
                      className="w-full rounded-xl border border-slate-200 dark:border-white/[0.08] bg-white dark:bg-white/[0.06] text-slate-900 dark:text-white p-2 text-xs outline-none"
                    />
                  </div>
                </div>

                <div>
                  <label className="block font-semibold text-slate-700 dark:text-slate-300 mb-1">Difficulty</label>
                  <select
                    value={difficulty}
                    onChange={(e) => setDifficulty(e.target.value)}
                    className="w-full rounded-xl border border-slate-200 dark:border-white/[0.08] bg-white dark:bg-white/[0.06] text-slate-900 dark:text-white p-2 text-xs outline-none"
                  >
                    <option value="EASY">EASY</option>
                    <option value="MEDIUM">MEDIUM</option>
                    <option value="HARD">HARD</option>
                  </select>
                </div>

                <div>
                  <label className="block font-semibold text-slate-700 dark:text-slate-300 mb-1">Description</label>
                  <textarea
                    value={description}
                    onChange={(e) => setDescription(e.target.value)}
                    rows={2}
                    className="w-full rounded-xl border border-slate-200 dark:border-white/[0.08] bg-white dark:bg-white/[0.06] text-slate-900 dark:text-white p-2 text-xs outline-none"
                  />
                </div>

                <div className="flex items-center justify-end gap-3 pt-3">
                  <button
                    type="button"
                    onClick={() => setShowAddModal(false)}
                    className="rounded-xl border border-slate-200 dark:border-white/[0.08] px-4 py-2 font-semibold text-slate-700 dark:text-slate-300 hover:bg-slate-50 dark:hover:bg-white/[0.06]"
                  >
                    Cancel
                  </button>
                  <button
                    type="button"
                    onClick={() => createMutation.mutate()}
                    disabled={createMutation.isPending || !title}
                    className="rounded-xl bg-brand-600 px-5 py-2 font-bold text-white shadow hover:bg-brand-700 disabled:opacity-50"
                  >
                    {createMutation.isPending ? "Creating..." : "Create Quiz"}
                  </button>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </RoleLayout>
  );
}
