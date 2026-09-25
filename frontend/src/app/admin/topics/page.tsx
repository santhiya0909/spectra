"use client";

import React, { useState } from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { adminService } from "@/services/admin.service";
import { subjectService } from "@/services/subject.service";
import { RoleLayout } from "@/components/layout/RoleLayout";
import { Badge } from "@/components/common/Badge";
import { Plus, Layers, Loader2 } from "lucide-react";

export default function AdminTopicsPage() {
  const queryClient = useQueryClient();

  const [name, setName] = useState("");
  const [description, setDescription] = useState("");
  const [difficultyLevel, setDifficultyLevel] = useState("MEDIUM");
  const [subjectId, setSubjectId] = useState<number | undefined>();
  const [showAddModal, setShowAddModal] = useState(false);

  const { data: topics, isLoading } = useQuery({
    queryKey: ["adminTopics"],
    queryFn: adminService.getTopics,
  });

  const { data: subjects } = useQuery({
    queryKey: ["adminSubjects"],
    queryFn: adminService.getSubjects,
  });

  const createMutation = useMutation({
    mutationFn: () =>
      adminService.createTopic({
        name,
        description,
        difficulty_level: difficultyLevel,
        subject_id: subjectId || (subjects && subjects[0]?.id) || 1,
      }),
    onSuccess: () => {
      setShowAddModal(false);
      setName("");
      setDescription("");
      queryClient.invalidateQueries({ queryKey: ["adminTopics"] });
    },
  });

  return (
    <RoleLayout allowedRoles={["ADMIN"]}>
      <div className="space-y-6">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold tracking-tight text-slate-900">Curriculum Topics</h1>
            <p className="mt-1 text-sm text-slate-500">
              Granular topic nodes monitored for knowledge gap diagnosis.
            </p>
          </div>

          <button
            onClick={() => setShowAddModal(true)}
            className="inline-flex items-center gap-2 rounded-xl bg-brand-600 px-4 py-2 text-xs font-bold text-white shadow hover:bg-brand-700"
          >
            <Plus className="h-4 w-4" />
            <span>Add Topic</span>
          </button>
        </div>

        <div className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
          {isLoading ? (
            <div className="space-y-3 animate-pulse">
              {[1, 2, 3].map((i) => (
                <div key={i} className="h-14 bg-slate-100 rounded-xl" />
              ))}
            </div>
          ) : topics && topics.length > 0 ? (
            <div className="overflow-x-auto">
              <table className="w-full text-left text-xs">
                <thead className="border-b border-slate-200 bg-slate-50 text-[11px] font-bold uppercase tracking-wider text-slate-400">
                  <tr>
                    <th className="px-4 py-3">Topic ID</th>
                    <th className="px-4 py-3">Topic Name</th>
                    <th className="px-4 py-3">Description</th>
                    <th className="px-4 py-3 text-right">Difficulty</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-100">
                  {topics.map((t: any) => (
                    <tr key={t.id} className="hover:bg-slate-50 transition">
                      <td className="px-4 py-3.5 font-mono text-slate-400">#{t.id}</td>
                      <td className="px-4 py-3.5 font-bold text-slate-900">{t.name}</td>
                      <td className="px-4 py-3.5 text-slate-500 max-w-sm truncate">{t.description}</td>
                      <td className="px-4 py-3.5 text-right">
                        <Badge
                          variant={t.difficulty_level === "EASY" ? "emerald" : t.difficulty_level === "MEDIUM" ? "brand" : "purple"}
                          size="sm"
                        >
                          {t.difficulty_level}
                        </Badge>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          ) : (
            <p className="text-xs text-slate-400 py-6 text-center">No topics configured yet.</p>
          )}
        </div>

        {/* Add Modal */}
        {showAddModal && (
          <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/50 backdrop-blur-sm p-4">
            <div className="w-full max-w-md rounded-3xl bg-white p-6 shadow-xl border border-slate-200">
              <h3 className="text-lg font-bold text-slate-900 mb-4">Add Curriculum Topic</h3>

              <div className="space-y-4">
                <div>
                  <label className="block text-xs font-semibold text-slate-700 mb-1">Subject</label>
                  <select
                    value={subjectId}
                    onChange={(e) => setSubjectId(Number(e.target.value))}
                    className="w-full rounded-xl border border-slate-200 p-2.5 text-sm outline-none focus:border-brand-500"
                  >
                    {subjects?.map((s: any) => (
                      <option key={s.id} value={s.id}>
                        {s.name} ({s.code})
                      </option>
                    ))}
                  </select>
                </div>

                <div>
                  <label className="block text-xs font-semibold text-slate-700 mb-1">Topic Name</label>
                  <input
                    type="text"
                    value={name}
                    onChange={(e) => setName(e.target.value)}
                    placeholder="e.g. Memory Garbage Collection"
                    className="w-full rounded-xl border border-slate-200 p-2.5 text-sm outline-none focus:border-brand-500"
                  />
                </div>

                <div>
                  <label className="block text-xs font-semibold text-slate-700 mb-1">Difficulty</label>
                  <select
                    value={difficultyLevel}
                    onChange={(e) => setDifficultyLevel(e.target.value)}
                    className="w-full rounded-xl border border-slate-200 p-2.5 text-sm outline-none focus:border-brand-500"
                  >
                    <option value="EASY">EASY</option>
                    <option value="MEDIUM">MEDIUM</option>
                    <option value="HARD">HARD</option>
                  </select>
                </div>

                <div>
                  <label className="block text-xs font-semibold text-slate-700 mb-1">Description</label>
                  <textarea
                    value={description}
                    onChange={(e) => setDescription(e.target.value)}
                    rows={2}
                    className="w-full rounded-xl border border-slate-200 p-2.5 text-sm outline-none focus:border-brand-500"
                  />
                </div>

                <div className="flex items-center justify-end gap-3 pt-2">
                  <button
                    type="button"
                    onClick={() => setShowAddModal(false)}
                    className="rounded-xl border border-slate-200 px-4 py-2 text-xs font-semibold text-slate-700 hover:bg-slate-50"
                  >
                    Cancel
                  </button>
                  <button
                    type="button"
                    onClick={() => createMutation.mutate()}
                    disabled={createMutation.isPending || !name}
                    className="rounded-xl bg-brand-600 px-5 py-2 text-xs font-bold text-white shadow hover:bg-brand-700 disabled:opacity-50"
                  >
                    {createMutation.isPending ? "Saving..." : "Create Topic"}
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
