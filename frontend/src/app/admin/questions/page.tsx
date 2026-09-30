"use client";

import React, { useState } from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { adminService } from "@/services/admin.service";
import { RoleLayout } from "@/components/layout/RoleLayout";
import { Badge } from "@/components/common/Badge";
import { Plus, Trash2, FileQuestion, Loader2 } from "lucide-react";

export default function AdminQuestionsPage() {
  const queryClient = useQueryClient();

  const [questionText, setQuestionText] = useState("");
  const [optA, setOptA] = useState("");
  const [optB, setOptB] = useState("");
  const [optC, setOptC] = useState("");
  const [optD, setOptD] = useState("");
  const [correctAnswer, setCorrectAnswer] = useState("");
  const [explanation, setExplanation] = useState("");
  const [difficulty, setDifficulty] = useState("MEDIUM");
  const [topicId, setTopicId] = useState<number | undefined>();
  const [subjectId, setSubjectId] = useState<number | undefined>();
  const [showAddModal, setShowAddModal] = useState(false);

  const { data: questions, isLoading } = useQuery({
    queryKey: ["adminQuestions"],
    queryFn: adminService.getQuestions,
  });

  const { data: topics } = useQuery({
    queryKey: ["adminTopics"],
    queryFn: adminService.getTopics,
  });

  const { data: subjects } = useQuery({
    queryKey: ["adminSubjects"],
    queryFn: adminService.getSubjects,
  });

  const createMutation = useMutation({
    mutationFn: () => {
      const options = [
        `A) ${optA}`,
        `B) ${optB}`,
        `C) ${optC}`,
        `D) ${optD}`,
      ];
      return adminService.createQuestion({
        subject_id: subjectId || (subjects && subjects[0]?.id) || 1,
        topic_id: topicId || (topics && topics[0]?.id) || 1,
        question_text: questionText,
        question_type: "MCQ",
        options,
        correct_answer: correctAnswer,
        explanation,
        difficulty,
      });
    },
    onSuccess: () => {
      setShowAddModal(false);
      setQuestionText("");
      setOptA("");
      setOptB("");
      setOptC("");
      setOptD("");
      setCorrectAnswer("");
      setExplanation("");
      queryClient.invalidateQueries({ queryKey: ["adminQuestions"] });
      queryClient.invalidateQueries({ queryKey: ["adminDashboard"] });
    },
  });

  const deleteMutation = useMutation({
    mutationFn: (id: number) => adminService.deleteQuestion(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["adminQuestions"] });
      queryClient.invalidateQueries({ queryKey: ["adminDashboard"] });
    },
  });

  return (
    <RoleLayout allowedRoles={["ADMIN"]}>
      <div className="space-y-6">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold tracking-tight text-slate-900 dark:text-white">Question Bank Repository</h1>
            <p className="mt-1 text-sm text-slate-500 dark:text-slate-400">
              Curate diagnostic and adaptive multiple choice assessment items with targeted explanations.
            </p>
          </div>
          <button
            onClick={() => setShowAddModal(true)}
            className="inline-flex items-center gap-2 rounded-xl bg-brand-600 px-4 py-2 text-xs font-bold text-white shadow hover:bg-brand-700"
          >
            <Plus className="h-4 w-4" />
            <span>Add Question</span>
          </button>
        </div>

        {/* Questions Table */}
        <div className="rounded-3xl border border-slate-200 dark:border-white/[0.08] bg-white dark:bg-[#0B1124]/85 p-6 shadow-sm">
          {isLoading ? (
            <div className="space-y-3 animate-pulse">
              {[1, 2, 3].map((i) => (
                <div key={i} className="h-16 bg-slate-100 dark:bg-white/[0.04] rounded-xl" />
              ))}
            </div>
          ) : questions && questions.length > 0 ? (
            <div className="overflow-x-auto">
              <table className="w-full text-left text-xs">
                <thead className="border-b border-slate-200 dark:border-white/[0.06] bg-slate-50 dark:bg-white/[0.03] text-[11px] font-bold uppercase tracking-wider text-slate-400 dark:text-slate-500">
                  <tr>
                    <th className="px-4 py-3">ID</th>
                    <th className="px-4 py-3">Topic</th>
                    <th className="px-4 py-3">Question Stem</th>
                    <th className="px-4 py-3">Difficulty</th>
                    <th className="px-4 py-3 text-right">Delete</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-100 dark:divide-white/[0.04]">
                  {questions.map((q: any) => (
                    <tr key={q.id} className="hover:bg-slate-50 dark:hover:bg-white/[0.03] transition">
                      <td className="px-4 py-3.5 font-mono text-slate-400">#{q.id}</td>
                      <td className="px-4 py-3.5 font-semibold text-slate-900 dark:text-white">{q.topic_name}</td>
                      <td className="px-4 py-3.5 text-slate-700 dark:text-slate-300 max-w-md truncate">{q.question_text}</td>
                      <td className="px-4 py-3.5">
                        <Badge
                          variant={q.difficulty === "EASY" ? "emerald" : q.difficulty === "MEDIUM" ? "brand" : "purple"}
                          size="sm"
                        >
                          {q.difficulty}
                        </Badge>
                      </td>
                      <td className="px-4 py-3.5 text-right">
                        <button
                          onClick={() => {
                            if (confirm("Delete this question from question bank?")) {
                              deleteMutation.mutate(q.id);
                            }
                          }}
                          className="rounded-lg p-1.5 text-slate-400 hover:bg-rose-50 dark:hover:bg-rose-950/20 hover:text-rose-600 dark:hover:text-rose-400 transition"
                        >
                          <Trash2 className="h-4 w-4" />
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          ) : (
            <p className="text-xs text-slate-400 py-6 text-center">No questions in question bank.</p>
          )}
        </div>

        {/* Add Modal */}
        {showAddModal && (
          <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/50 dark:bg-black/60 backdrop-blur-sm p-4 overflow-y-auto">
            <div className="w-full max-w-lg rounded-3xl bg-white dark:bg-[#0B1124] p-6 shadow-xl border border-slate-200 dark:border-white/[0.08] my-8">
              <h3 className="text-lg font-bold text-slate-900 dark:text-white mb-4">Add Diagnostic Question</h3>

              <div className="space-y-3 text-xs">
                <div className="grid grid-cols-2 gap-3">
                  <div>
                    <label className="block font-semibold text-slate-700 dark:text-slate-300 mb-1">Subject</label>
                    <select
                      value={subjectId}
                      onChange={(e) => setSubjectId(Number(e.target.value))}
                      className="w-full rounded-xl border border-slate-200 dark:border-white/[0.08] bg-white dark:bg-white/[0.06] text-slate-900 dark:text-white p-2 text-xs outline-none"
                    >
                      {subjects?.map((s: any) => (
                        <option key={s.id} value={s.id}>{s.name}</option>
                      ))}
                    </select>
                  </div>
                  <div>
                    <label className="block font-semibold text-slate-700 dark:text-slate-300 mb-1">Topic</label>
                    <select
                      value={topicId}
                      onChange={(e) => setTopicId(Number(e.target.value))}
                      className="w-full rounded-xl border border-slate-200 dark:border-white/[0.08] bg-white dark:bg-white/[0.06] text-slate-900 dark:text-white p-2 text-xs outline-none"
                    >
                      {topics?.map((t: any) => (
                        <option key={t.id} value={t.id}>{t.name}</option>
                      ))}
                    </select>
                  </div>
                </div>

                <div>
                  <label className="block font-semibold text-slate-700 dark:text-slate-300 mb-1">Question Text</label>
                  <textarea
                    value={questionText}
                    onChange={(e) => setQuestionText(e.target.value)}
                    rows={2}
                    placeholder="Enter question stem..."
                    className="w-full rounded-xl border border-slate-200 dark:border-white/[0.08] bg-white dark:bg-white/[0.06] text-slate-900 dark:text-white p-2 text-xs outline-none placeholder:text-slate-400 dark:placeholder:text-slate-500"
                  />
                </div>

                <div className="grid grid-cols-2 gap-2">
                  {[
                    { val: optA, set: setOptA, label: "Option A" },
                    { val: optB, set: setOptB, label: "Option B" },
                    { val: optC, set: setOptC, label: "Option C" },
                    { val: optD, set: setOptD, label: "Option D" },
                  ].map(({ val, set, label }) => (
                    <input
                      key={label}
                      type="text"
                      value={val}
                      onChange={(e) => set(e.target.value)}
                      placeholder={label}
                      className="rounded-xl border border-slate-200 dark:border-white/[0.08] bg-white dark:bg-white/[0.06] text-slate-900 dark:text-white p-2 text-xs outline-none placeholder:text-slate-400 dark:placeholder:text-slate-500"
                    />
                  ))}
                </div>

                <div>
                  <label className="block font-semibold text-slate-700 dark:text-slate-300 mb-1">Correct Answer (e.g. &apos;B&apos; or exact option string)</label>
                  <input
                    type="text"
                    value={correctAnswer}
                    onChange={(e) => setCorrectAnswer(e.target.value)}
                    placeholder="e.g. B) The caller's variable remains unchanged"
                    className="w-full rounded-xl border border-slate-200 dark:border-white/[0.08] bg-white dark:bg-white/[0.06] text-slate-900 dark:text-white p-2 text-xs outline-none placeholder:text-slate-400 dark:placeholder:text-slate-500"
                  />
                </div>

                <div>
                  <label className="block font-semibold text-slate-700 dark:text-slate-300 mb-1">Explanation for Student</label>
                  <textarea
                    value={explanation}
                    onChange={(e) => setExplanation(e.target.value)}
                    rows={2}
                    placeholder="Explains why this answer is correct..."
                    className="w-full rounded-xl border border-slate-200 dark:border-white/[0.08] bg-white dark:bg-white/[0.06] text-slate-900 dark:text-white p-2 text-xs outline-none placeholder:text-slate-400 dark:placeholder:text-slate-500"
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
                    disabled={createMutation.isPending || !questionText || !correctAnswer}
                    className="rounded-xl bg-brand-600 px-5 py-2 font-bold text-white shadow hover:bg-brand-700 disabled:opacity-50"
                  >
                    {createMutation.isPending ? "Saving..." : "Save Question"}
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
