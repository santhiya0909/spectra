"use client";

import React, { useState } from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { adminService } from "@/services/admin.service";
import { Subject, Lesson, Topic, StudyResource } from "@/services/subject.service";
import { RoleLayout } from "@/components/layout/RoleLayout";
import { Badge } from "@/components/common/Badge";
import {
  Plus,
  Trash2,
  Edit2,
  BookOpen,
  Layers,
  Sparkles,
  ArrowLeft,
  ArrowUp,
  ArrowDown,
  ExternalLink,
  ChevronDown,
  ChevronRight,
  Search,
  CheckCircle2,
  XCircle,
  Clock,
  Loader2,
  Globe,
  FileText,
  Video,
  Code,
  GraduationCap,
} from "lucide-react";

export default function AdminSubjectsPage() {
  const queryClient = useQueryClient();

  // Search & Filters for subjects
  const [search, setSearch] = useState("");
  const [categoryFilter, setCategoryFilter] = useState("ALL");
  const [difficultyFilter, setDifficultyFilter] = useState("ALL");
  const [statusFilter, setStatusFilter] = useState<string>("ALL");

  // Selected subject for deep drill-down curriculum management
  const [selectedSubjectId, setSelectedSubjectId] = useState<number | null>(null);

  // Modals state
  const [showSubjectModal, setShowSubjectModal] = useState(false);
  const [editingSubject, setEditingSubject] = useState<Subject | null>(null);

  const [showLessonModal, setShowLessonModal] = useState(false);
  const [editingLesson, setEditingLesson] = useState<Lesson | null>(null);

  const [showTopicModal, setShowTopicModal] = useState(false);
  const [editingTopic, setEditingTopic] = useState<Topic | null>(null);
  const [targetLessonIdForTopic, setTargetLessonIdForTopic] = useState<number | null>(null);

  const [showResourceModal, setShowResourceModal] = useState(false);
  const [editingResource, setEditingResource] = useState<StudyResource | null>(null);
  const [targetLessonIdForResource, setTargetLessonIdForResource] = useState<number | null>(null);

  // Form states - Subject
  const [subName, setSubName] = useState("");
  const [subCode, setSubCode] = useState("");
  const [subDesc, setSubDesc] = useState("");
  const [subCategory, setSubCategory] = useState("PROGRAMMING");
  const [subDifficulty, setSubDifficulty] = useState("BEGINNER");
  const [subIsActive, setSubIsActive] = useState(true);

  // Form states - Lesson
  const [lesTitle, setLesTitle] = useState("");
  const [lesShortDesc, setLesShortDesc] = useState("");
  const [lesContent, setLesContent] = useState("");
  const [lesDifficulty, setLesDifficulty] = useState("MEDIUM");
  const [lesDuration, setLesDuration] = useState(15);
  const [lesIsActive, setLesIsActive] = useState(true);

  // Form states - Topic
  const [topName, setTopName] = useState("");
  const [topDesc, setTopDesc] = useState("");
  const [topDifficulty, setTopDifficulty] = useState("MEDIUM");
  const [topIsActive, setTopIsActive] = useState(true);

  // Form states - Study Resource
  const [resTitle, setResTitle] = useState("");
  const [resDesc, setResDesc] = useState("");
  const [resUrl, setResUrl] = useState("");
  const [resType, setResType] = useState("DOCUMENTATION");
  const [resProvider, setResProvider] = useState("Official Documentation");
  const [resIsActive, setResIsActive] = useState(true);

  // Query all subjects
  const { data: subjects = [], isLoading: subjectsLoading } = useQuery<Subject[]>({
    queryKey: ["adminSubjects", search, categoryFilter, difficultyFilter, statusFilter],
    queryFn: () =>
      adminService.getSubjects({
        search: search || undefined,
        category: categoryFilter !== "ALL" ? categoryFilter : undefined,
        difficulty: difficultyFilter !== "ALL" ? difficultyFilter : undefined,
        is_active: statusFilter === "ALL" ? undefined : statusFilter === "ACTIVE",
      }),
  });

  // Query selected subject detail (with lessons, child topics, resources)
  const { data: selectedSubject, isLoading: selectedSubjectLoading } = useQuery<Subject>({
    queryKey: ["adminSubjectDetail", selectedSubjectId],
    queryFn: () => adminService.getSubject(selectedSubjectId!),
    enabled: !!selectedSubjectId,
  });

  // ================= MUTATIONS =================
  const createOrUpdateSubjectMutation = useMutation({
    mutationFn: () => {
      const payload = {
        name: subName,
        code: subCode,
        description: subDesc,
        category: subCategory,
        difficulty_level: subDifficulty,
        is_active: subIsActive,
      };
      if (editingSubject) {
        return adminService.updateSubject(editingSubject.id, payload);
      }
      return adminService.createSubject(payload);
    },
    onSuccess: () => {
      setShowSubjectModal(false);
      setEditingSubject(null);
      queryClient.invalidateQueries({ queryKey: ["adminSubjects"] });
      queryClient.invalidateQueries({ queryKey: ["adminDashboard"] });
      if (selectedSubjectId) {
        queryClient.invalidateQueries({ queryKey: ["adminSubjectDetail", selectedSubjectId] });
      }
    },
  });

  const toggleSubjectStatusMutation = useMutation({
    mutationFn: ({ id, is_active }: { id: number; is_active: boolean }) =>
      adminService.toggleSubjectStatus(id, is_active),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["adminSubjects"] });
      if (selectedSubjectId) {
        queryClient.invalidateQueries({ queryKey: ["adminSubjectDetail", selectedSubjectId] });
      }
    },
  });

  const deleteSubjectMutation = useMutation({
    mutationFn: (id: number) => adminService.deleteSubject(id),
    onSuccess: () => {
      if (selectedSubjectId) setSelectedSubjectId(null);
      queryClient.invalidateQueries({ queryKey: ["adminSubjects"] });
      queryClient.invalidateQueries({ queryKey: ["adminDashboard"] });
    },
  });

  const reorderSubjectsMutation = useMutation({
    mutationFn: (items: { id: number; order: number }[]) => adminService.reorderSubjects(items),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["adminSubjects"] });
    },
  });

  // Lesson Mutations
  const createOrUpdateLessonMutation = useMutation({
    mutationFn: () => {
      const payload = {
        title: lesTitle,
        short_description: lesShortDesc,
        detailed_description: lesContent.slice(0, 300) + "...",
        content: lesContent,
        difficulty_level: lesDifficulty,
        difficulty: lesDifficulty,
        estimated_duration: Number(lesDuration),
        estimated_minutes: Number(lesDuration),
        is_active: lesIsActive,
      };
      if (editingLesson) {
        return adminService.updateLesson(editingLesson.id, payload);
      }
      return adminService.createLesson(selectedSubjectId!, payload);
    },
    onSuccess: () => {
      setShowLessonModal(false);
      setEditingLesson(null);
      queryClient.invalidateQueries({ queryKey: ["adminSubjectDetail", selectedSubjectId] });
    },
  });

  const toggleLessonStatusMutation = useMutation({
    mutationFn: ({ id, is_active }: { id: number; is_active: boolean }) =>
      adminService.toggleLessonStatus(id, is_active),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["adminSubjectDetail", selectedSubjectId] });
    },
  });

  const deleteLessonMutation = useMutation({
    mutationFn: (id: number) => adminService.deleteLesson(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["adminSubjectDetail", selectedSubjectId] });
    },
  });

  const reorderLessonsMutation = useMutation({
    mutationFn: (items: { id: number; order: number }[]) => adminService.reorderLessons(items),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["adminSubjectDetail", selectedSubjectId] });
    },
  });

  // Topic Mutations
  const createOrUpdateTopicMutation = useMutation({
    mutationFn: () => {
      const payload = {
        subject_id: selectedSubjectId!,
        lesson_id: targetLessonIdForTopic,
        name: topName,
        description: topDesc,
        difficulty_level: topDifficulty,
        is_active: topIsActive,
      };
      if (editingTopic) {
        return adminService.updateTopic(editingTopic.id, payload);
      }
      return adminService.createTopic(payload);
    },
    onSuccess: () => {
      setShowTopicModal(false);
      setEditingTopic(null);
      queryClient.invalidateQueries({ queryKey: ["adminSubjectDetail", selectedSubjectId] });
    },
  });

  const toggleTopicStatusMutation = useMutation({
    mutationFn: ({ id, is_active }: { id: number; is_active: boolean }) =>
      adminService.toggleTopicStatus(id, is_active),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["adminSubjectDetail", selectedSubjectId] });
    },
  });

  const deleteTopicMutation = useMutation({
    mutationFn: (id: number) => adminService.deleteTopic(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["adminSubjectDetail", selectedSubjectId] });
    },
  });

  // Study Resource Mutations
  const createOrUpdateResourceMutation = useMutation({
    mutationFn: () => {
      const payload = {
        title: resTitle,
        description: resDesc,
        url: resUrl,
        resource_type: resType,
        provider: resProvider,
        is_active: resIsActive,
      };
      if (editingResource) {
        return adminService.updateResource(editingResource.id, payload);
      }
      return adminService.createResource(targetLessonIdForResource!, payload);
    },
    onSuccess: () => {
      setShowResourceModal(false);
      setEditingResource(null);
      queryClient.invalidateQueries({ queryKey: ["adminSubjectDetail", selectedSubjectId] });
    },
  });

  const toggleResourceStatusMutation = useMutation({
    mutationFn: ({ id, is_active }: { id: number; is_active: boolean }) =>
      adminService.toggleResourceStatus(id, is_active),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["adminSubjectDetail", selectedSubjectId] });
    },
  });

  const deleteResourceMutation = useMutation({
    mutationFn: (id: number) => adminService.deleteResource(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["adminSubjectDetail", selectedSubjectId] });
    },
  });

  // Handlers
  const handleOpenSubjectModal = (subj?: Subject) => {
    if (subj) {
      setEditingSubject(subj);
      setSubName(subj.name);
      setSubCode(subj.code);
      setSubDesc(subj.description || "");
      setSubCategory(subj.category || "PROGRAMMING");
      setSubDifficulty(subj.difficulty_level || "BEGINNER");
      setSubIsActive(subj.is_active);
    } else {
      setEditingSubject(null);
      setSubName("");
      setSubCode("");
      setSubDesc("");
      setSubCategory("PROGRAMMING");
      setSubDifficulty("BEGINNER");
      setSubIsActive(true);
    }
    setShowSubjectModal(true);
  };

  const handleOpenLessonModal = (lesson?: Lesson) => {
    if (lesson) {
      setEditingLesson(lesson);
      setLesTitle(lesson.title);
      setLesShortDesc(lesson.short_description || lesson.description || "");
      setLesContent(lesson.content || "");
      setLesDifficulty(lesson.difficulty_level || lesson.difficulty || "MEDIUM");
      setLesDuration(lesson.estimated_duration || lesson.estimated_minutes || 15);
      setLesIsActive(lesson.is_active);
    } else {
      setEditingLesson(null);
      setLesTitle("");
      setLesShortDesc("");
      setLesContent("# Lesson Overview\n\nExplain key concepts and provide code examples.");
      setLesDifficulty("MEDIUM");
      setLesDuration(15);
      setLesIsActive(true);
    }
    setShowLessonModal(true);
  };

  const handleOpenTopicModal = (lessonId: number, topic?: Topic) => {
    setTargetLessonIdForTopic(lessonId);
    if (topic) {
      setEditingTopic(topic);
      setTopName(topic.name);
      setTopDesc(topic.description || "");
      setTopDifficulty(topic.difficulty_level || "MEDIUM");
      setTopIsActive(topic.is_active);
    } else {
      setEditingTopic(null);
      setTopName("");
      setTopDesc("");
      setTopDifficulty("MEDIUM");
      setTopIsActive(true);
    }
    setShowTopicModal(true);
  };

  const handleOpenResourceModal = (lessonId: number, res?: StudyResource) => {
    setTargetLessonIdForResource(lessonId);
    if (res) {
      setEditingResource(res);
      setResTitle(res.title);
      setResDesc(res.description || "");
      setResUrl(res.url);
      setResType(res.resource_type);
      setResProvider(res.provider);
      setResIsActive(res.is_active);
    } else {
      setEditingResource(null);
      setResTitle("");
      setResDesc("");
      setResUrl("");
      setResType("DOCUMENTATION");
      setResProvider("MDN Web Docs");
      setResIsActive(true);
    }
    setShowResourceModal(true);
  };

  const handleMoveSubject = (index: number, direction: "up" | "down") => {
    if (!subjects) return;
    const targetIndex = direction === "up" ? index - 1 : index + 1;
    if (targetIndex < 0 || targetIndex >= subjects.length) return;

    const currentSub = subjects[index];
    const targetSub = subjects[targetIndex];

    reorderSubjectsMutation.mutate([
      { id: currentSub.id, order: targetIndex + 1 },
      { id: targetSub.id, order: index + 1 },
    ]);
  };

  const handleMoveLesson = (lessons: Lesson[], index: number, direction: "up" | "down") => {
    const targetIndex = direction === "up" ? index - 1 : index + 1;
    if (targetIndex < 0 || targetIndex >= lessons.length) return;

    const currentLes = lessons[index];
    const targetLes = lessons[targetIndex];

    reorderLessonsMutation.mutate([
      { id: currentLes.id, order: targetIndex + 1 },
      { id: targetLes.id, order: index + 1 },
    ]);
  };

  return (
    <RoleLayout allowedRoles={["ADMIN"]}>
      <div className="space-y-6">
        {/* VIEW 1: SUBJECTS OVERVIEW TABLE */}
        {!selectedSubjectId ? (
          <div className="space-y-6">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
              <div>
                <h1 className="text-2xl font-bold tracking-tight text-slate-900">
                  Subject & Deep Lesson Management
                </h1>
                <p className="mt-1 text-sm text-slate-500">
                  Manage academic subjects, hierarchical modules, child topics, and verified external learning resources.
                </p>
              </div>

              <button
                onClick={() => handleOpenSubjectModal()}
                className="inline-flex items-center gap-2 rounded-xl bg-brand-600 px-4 py-2 text-xs font-bold text-white shadow hover:bg-brand-700 transition"
              >
                <Plus className="h-4 w-4" />
                <span>Create Subject</span>
              </button>
            </div>

            {/* Filter Toolbar */}
            <div className="flex flex-col md:flex-row items-stretch md:items-center justify-between gap-3 rounded-2xl border border-slate-200 dark:border-white/[0.08] bg-white dark:bg-[#0B1124]/85 p-3.5 shadow-sm">
              <div className="relative flex-1">
                <Search className="absolute left-3.5 top-1/2 -translate-y-1/2 h-4 w-4 text-slate-400" />
                <input
                  type="text"
                  value={search}
                  onChange={(e) => setSearch(e.target.value)}
                  placeholder="Filter subjects by name, code, or description..."
                  className="w-full rounded-xl border border-slate-200 dark:border-white/[0.08] bg-slate-50 dark:bg-white/[0.06] pl-10 pr-4 py-2 text-xs font-medium text-slate-900 dark:text-white placeholder:text-slate-400 dark:placeholder:text-slate-500 focus:bg-white dark:focus:bg-white/[0.08] focus:border-brand-500 dark:focus:border-cyan-500 focus:outline-none"
                />
              </div>

              <div className="flex flex-wrap items-center gap-2">
                <select
                  value={categoryFilter}
                  onChange={(e) => setCategoryFilter(e.target.value)}
                  className="rounded-xl border border-slate-200 dark:border-white/[0.08] bg-slate-50 dark:bg-white/[0.06] px-3 py-2 text-xs font-semibold text-slate-700 dark:text-slate-300 focus:bg-white dark:focus:bg-white/[0.08] focus:outline-none"
                >
                  <option value="ALL">All Categories</option>
                  <option value="PROGRAMMING">Programming</option>
                  <option value="DATA_ENGINEERING">Data Engineering</option>
                  <option value="MATHEMATICS">Mathematics</option>
                  <option value="BUSINESS">Business</option>
                </select>

                <select
                  value={difficultyFilter}
                  onChange={(e) => setDifficultyFilter(e.target.value)}
                  className="rounded-xl border border-slate-200 dark:border-white/[0.08] bg-slate-50 dark:bg-white/[0.06] px-3 py-2 text-xs font-semibold text-slate-700 dark:text-slate-300 focus:bg-white dark:focus:bg-white/[0.08] focus:outline-none"
                >
                  <option value="ALL">All Difficulties</option>
                  <option value="BEGINNER">Beginner</option>
                  <option value="INTERMEDIATE">Intermediate</option>
                  <option value="ADVANCED">Advanced</option>
                </select>

                <select
                  value={statusFilter}
                  onChange={(e) => setStatusFilter(e.target.value)}
                  className="rounded-xl border border-slate-200 dark:border-white/[0.08] bg-slate-50 dark:bg-white/[0.06] px-3 py-2 text-xs font-semibold text-slate-700 dark:text-slate-300 focus:bg-white dark:focus:bg-white/[0.08] focus:outline-none"
                >
                  <option value="ALL">All Visibility</option>
                  <option value="ACTIVE">Active Only</option>
                  <option value="INACTIVE">Inactive Only</option>
                </select>
              </div>
            </div>

            {/* Subjects Table */}
            <div className="rounded-3xl border border-slate-200 dark:border-white/[0.08] bg-white dark:bg-[#0B1124]/85 p-6 shadow-sm overflow-hidden">
              {subjectsLoading ? (
                <div className="space-y-3 animate-pulse">
                  {[1, 2, 3, 4].map((i) => (
                    <div key={i} className="h-16 bg-slate-100 dark:bg-white/[0.04] rounded-xl" />
                  ))}
                </div>
              ) : subjects.length === 0 ? (
                <div className="p-12 text-center text-slate-500 dark:text-slate-400">
                  <BookOpen className="h-10 w-10 mx-auto text-slate-300 dark:text-slate-600 mb-2" />
                  <p className="text-sm font-semibold">No subjects match the filter criteria.</p>
                </div>
              ) : (
                <div className="overflow-x-auto">
                  <table className="w-full text-left text-xs">
                    <thead className="border-b border-slate-200 dark:border-white/[0.06] bg-slate-50 dark:bg-white/[0.03] text-[11px] font-bold uppercase tracking-wider text-slate-500 dark:text-slate-400">
                      <tr>
                        <th className="px-4 py-3">Order</th>
                        <th className="px-4 py-3">Code</th>
                        <th className="px-4 py-3">Subject Name</th>
                        <th className="px-4 py-3">Category</th>
                        <th className="px-4 py-3">Modules</th>
                        <th className="px-4 py-3">Status</th>
                        <th className="px-4 py-3 text-right">Actions</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-slate-100 dark:divide-white/[0.04]">
                      {subjects.map((s, idx) => (
                        <tr key={s.id} className="hover:bg-slate-50/80 dark:hover:bg-white/[0.03] transition">
                          <td className="px-4 py-3.5">
                            <div className="flex items-center gap-1 text-slate-400">
                              <button
                                onClick={() => handleMoveSubject(idx, "up")}
                                disabled={idx === 0}
                                className="rounded p-1 hover:bg-slate-200 dark:hover:bg-white/[0.08] disabled:opacity-30"
                              >
                                <ArrowUp className="h-3.5 w-3.5" />
                              </button>
                              <button
                                onClick={() => handleMoveSubject(idx, "down")}
                                disabled={idx === subjects.length - 1}
                                className="rounded p-1 hover:bg-slate-200 dark:hover:bg-white/[0.08] disabled:opacity-30"
                              >
                                <ArrowDown className="h-3.5 w-3.5" />
                              </button>
                            </div>
                          </td>
                          <td className="px-4 py-3.5 font-bold text-brand-600 dark:text-cyan-400">{s.code}</td>
                          <td className="px-4 py-3.5">
                            <div className="font-bold text-slate-900 dark:text-white">{s.name}</div>
                            <div className="text-[11px] text-slate-500 dark:text-slate-400 max-w-xs truncate">{s.description}</div>
                          </td>
                          <td className="px-4 py-3.5">
                            <span className="rounded bg-slate-100 dark:bg-white/[0.06] px-2 py-0.5 text-[10px] font-bold text-slate-600 dark:text-slate-300 uppercase">
                              {s.category?.replace(/_/g, " ") || "GENERAL"}
                            </span>
                          </td>
                          <td className="px-4 py-3.5 font-semibold text-slate-700 dark:text-slate-300">
                            {s.lessons_count} Modules
                          </td>
                          <td className="px-4 py-3.5">
                            <button
                              onClick={() =>
                                toggleSubjectStatusMutation.mutate({
                                  id: s.id,
                                  is_active: !s.is_active,
                                })
                              }
                              className={`inline-flex items-center gap-1.5 rounded-full px-2.5 py-1 text-[11px] font-bold transition ${
                                s.is_active
                                  ? "bg-emerald-50 dark:bg-emerald-900/20 text-emerald-700 dark:text-emerald-400 border border-emerald-200 dark:border-emerald-500/30 hover:bg-emerald-100 dark:hover:bg-emerald-900/30"
                                  : "bg-rose-50 dark:bg-rose-900/20 text-rose-700 dark:text-rose-400 border border-rose-200 dark:border-rose-500/30 hover:bg-rose-100 dark:hover:bg-rose-900/30"
                              }`}
                            >
                              {s.is_active ? <CheckCircle2 className="h-3 w-3" /> : <XCircle className="h-3 w-3" />}
                              <span>{s.is_active ? "Active" : "Inactive"}</span>
                            </button>
                          </td>
                          <td className="px-4 py-3.5 text-right">
                            <div className="flex items-center justify-end gap-2">
                              <button
                                onClick={() => setSelectedSubjectId(s.id)}
                                className="inline-flex items-center gap-1 rounded-lg bg-brand-50 dark:bg-cyan-900/20 hover:bg-brand-100 dark:hover:bg-cyan-900/30 text-brand-700 dark:text-cyan-300 border border-brand-200 dark:border-cyan-500/30 px-2.5 py-1.5 text-xs font-bold transition"
                              >
                                <Layers className="h-3.5 w-3.5" />
                                <span>Curriculum</span>
                              </button>
                              <button
                                onClick={() => handleOpenSubjectModal(s)}
                                className="rounded-lg p-1.5 text-slate-400 hover:bg-slate-100 dark:hover:bg-white/[0.06] hover:text-slate-700 dark:hover:text-white transition"
                              >
                                <Edit2 className="h-3.5 w-3.5" />
                              </button>
                              <button
                                onClick={() => {
                                  if (confirm(`Delete subject "${s.name}" and all associated lessons/topics?`)) {
                                    deleteSubjectMutation.mutate(s.id);
                                  }
                                }}
                                className="rounded-lg p-1.5 text-slate-400 hover:bg-rose-50 dark:hover:bg-rose-950/20 hover:text-rose-600 dark:hover:text-rose-400 transition"
                              >
                                <Trash2 className="h-3.5 w-3.5" />
                              </button>
                            </div>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              )}
            </div>
          </div>
        ) : (
          /* VIEW 2: DRILLDOWN DEEP CURRICULUM MANAGER FOR SELECTED SUBJECT */
          <div className="space-y-6">
            <div className="flex items-center justify-between">
              <button
                onClick={() => setSelectedSubjectId(null)}
                className="inline-flex items-center gap-1.5 text-xs font-bold text-slate-600 hover:text-slate-900 transition"
              >
                <ArrowLeft className="h-4 w-4" />
                <span>Back to All Subjects</span>
              </button>
            </div>

            {selectedSubjectLoading ? (
              <div className="h-64 bg-slate-200 dark:bg-slate-700/40 rounded-3xl animate-pulse" />
            ) : selectedSubject ? (
              <div className="space-y-6">
                {/* Subject Header Card */}
                <div className="rounded-3xl border border-slate-200 dark:border-white/[0.08] bg-white dark:bg-[#0B1124]/85 p-6 sm:p-8 shadow-sm">
                  <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
                    <div>
                      <div className="flex items-center gap-2 mb-2">
                        <span className="rounded-lg bg-brand-50 px-2.5 py-1 text-xs font-bold text-brand-700 uppercase border border-brand-100">
                          {selectedSubject.code}
                        </span>
                        <Badge
                          variant={
                            selectedSubject.difficulty_level === "BEGINNER"
                              ? "emerald"
                              : selectedSubject.difficulty_level === "INTERMEDIATE"
                              ? "brand"
                              : "purple"
                          }
                          size="sm"
                        >
                          {selectedSubject.difficulty_level || "ALL LEVELS"}
                        </Badge>
                      </div>
                      <h1 className="text-2xl font-bold text-slate-900 dark:text-white">{selectedSubject.name}</h1>
                      <p className="mt-1 text-xs sm:text-sm text-slate-600 dark:text-slate-400 max-w-2xl">{selectedSubject.description}</p>
                    </div>

                    <div className="flex items-center gap-2 self-start sm:self-center">
                      <button
                        onClick={() => handleOpenLessonModal()}
                        className="inline-flex items-center gap-2 rounded-xl bg-brand-600 hover:bg-brand-700 text-white px-4 py-2 text-xs font-bold transition shadow-sm"
                      >
                        <Plus className="h-4 w-4" />
                        <span>Add Module / Lesson</span>
                      </button>
                    </div>
                  </div>
                </div>

                {/* Modules & Deep Hierarchy List */}
                <div className="space-y-4">
                  <div className="flex items-center justify-between">
                    <h2 className="text-base font-bold text-slate-900 dark:text-white">
                      Curriculum Modules ({selectedSubject.lessons?.length || 0})
                    </h2>
                    <span className="text-xs text-slate-500 dark:text-slate-400">Hierarchy: Subject → Lesson → Topics → Study Resources</span>
                  </div>

                  {!selectedSubject.lessons || selectedSubject.lessons.length === 0 ? (
                    <div className="rounded-3xl border border-dashed border-slate-300 dark:border-white/10 bg-white dark:bg-white/[0.02] p-12 text-center text-slate-500 dark:text-slate-400">
                      <BookOpen className="h-10 w-10 mx-auto text-slate-300 mb-2" />
                      <p className="text-sm font-semibold">No modules configured yet for this subject.</p>
                      <button
                        onClick={() => handleOpenLessonModal()}
                        className="mt-3 inline-flex items-center gap-1.5 rounded-xl bg-brand-600 px-3 py-1.5 text-xs font-bold text-white"
                      >
                        <Plus className="h-3.5 w-3.5" />
                        <span>Add First Module</span>
                      </button>
                    </div>
                  ) : (
                    <div className="space-y-5">
                      {selectedSubject.lessons.map((lesson, lIdx) => (
                        <div
                          key={lesson.id}
                          className="rounded-3xl border border-slate-200 dark:border-white/[0.08] bg-white dark:bg-[#0B1124]/85 p-6 shadow-sm space-y-4"
                        >
                          {/* Module Header Bar */}
                          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-4 border-b border-slate-100 dark:border-white/[0.06]">
                            <div className="flex items-start gap-3">
                              <div className="flex items-center gap-1 text-slate-400 pt-1">
                                <button
                                  onClick={() => handleMoveLesson(selectedSubject.lessons!, lIdx, "up")}
                                  disabled={lIdx === 0}
                                  className="rounded p-1 hover:bg-slate-100 disabled:opacity-30"
                                >
                                  <ArrowUp className="h-3.5 w-3.5" />
                                </button>
                                <button
                                  onClick={() => handleMoveLesson(selectedSubject.lessons!, lIdx, "down")}
                                  disabled={lIdx === selectedSubject.lessons!.length - 1}
                                  className="rounded p-1 hover:bg-slate-100 disabled:opacity-30"
                                >
                                  <ArrowDown className="h-3.5 w-3.5" />
                                </button>
                              </div>

                              <div>
                                <div className="flex items-center gap-2">
                                  <span className="text-xs font-extrabold text-brand-600 uppercase">
                                    Module {lesson.lesson_order}
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
                                    <Clock className="h-3 w-3 text-slate-400" />
                                    {lesson.estimated_duration || lesson.estimated_minutes || 15} mins
                                  </span>
                                </div>
                                <h3 className="text-base font-bold text-slate-900 dark:text-white mt-1">{lesson.title}</h3>
                                {lesson.short_description && (
                                  <p className="text-xs text-slate-500 dark:text-slate-400 mt-0.5">{lesson.short_description}</p>
                                )}
                              </div>
                            </div>

                            <div className="flex items-center gap-2 self-end sm:self-center">
                              <button
                                onClick={() =>
                                  toggleLessonStatusMutation.mutate({
                                    id: lesson.id,
                                    is_active: !lesson.is_active,
                                  })
                                }
                                className={`inline-flex items-center gap-1 rounded-full px-2.5 py-1 text-[11px] font-bold transition ${
                                  lesson.is_active
                                    ? "bg-emerald-50 text-emerald-700 border border-emerald-200"
                                    : "bg-rose-50 text-rose-700 border border-rose-200"
                                }`}
                              >
                                {lesson.is_active ? <CheckCircle2 className="h-3 w-3" /> : <XCircle className="h-3 w-3" />}
                                <span>{lesson.is_active ? "Active" : "Inactive"}</span>
                              </button>

                              <button
                                onClick={() => handleOpenLessonModal(lesson)}
                                className="rounded-lg p-1.5 text-slate-400 hover:bg-slate-100 hover:text-slate-700 transition"
                              >
                                <Edit2 className="h-3.5 w-3.5" />
                              </button>

                              <button
                                onClick={() => {
                                  if (confirm(`Delete lesson "${lesson.title}"?`)) {
                                    deleteLessonMutation.mutate(lesson.id);
                                  }
                                }}
                                className="rounded-lg p-1.5 text-slate-400 hover:bg-rose-50 hover:text-rose-600 transition"
                              >
                                <Trash2 className="h-3.5 w-3.5" />
                              </button>
                            </div>
                          </div>

                          {/* Child Topics Section */}
                          <div className="rounded-2xl bg-slate-50/70 dark:bg-white/[0.02] border border-slate-200/70 dark:border-white/[0.06] p-4 space-y-3">
                            <div className="flex items-center justify-between">
                              <div className="flex items-center gap-1.5 text-xs font-bold text-slate-700 dark:text-slate-300">
                                <Layers className="h-3.5 w-3.5 text-indigo-600 dark:text-indigo-400" />
                                <span>Child Topics ({lesson.topics?.length || 0})</span>
                              </div>
                              <button
                                onClick={() => handleOpenTopicModal(lesson.id)}
                                className="inline-flex items-center gap-1 rounded-lg bg-indigo-50 dark:bg-indigo-900/20 hover:bg-indigo-100 dark:hover:bg-indigo-900/30 text-indigo-700 dark:text-indigo-300 px-2 py-1 text-[11px] font-bold transition"
                              >
                                <Plus className="h-3 w-3" />
                                <span>Add Topic</span>
                              </button>
                            </div>

                            {!lesson.topics || lesson.topics.length === 0 ? (
                              <p className="text-[11px] text-slate-400 italic">No topics attached to this module.</p>
                            ) : (
                              <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
                                {lesson.topics.map((t) => (
                                  <div
                                    key={t.id}
                                    className="flex items-center justify-between rounded-xl bg-white dark:bg-white/[0.04] border border-slate-200 dark:border-white/[0.06] px-3 py-2 text-xs"
                                  >
                                    <div>
                                      <span className="font-semibold text-slate-900 dark:text-white">{t.name}</span>
                                      <span className="ml-2 text-[10px] text-slate-500 dark:text-slate-400 font-medium">
                                        ({t.difficulty_level})
                                      </span>
                                    </div>
                                    <div className="flex items-center gap-1">
                                      <button
                                        onClick={() =>
                                          toggleTopicStatusMutation.mutate({
                                            id: t.id,
                                            is_active: !t.is_active,
                                          })
                                        }
                                        className={`rounded-full px-1.5 py-0.5 text-[9px] font-bold ${
                                          t.is_active ? "bg-emerald-50 dark:bg-emerald-900/20 text-emerald-700 dark:text-emerald-400" : "bg-rose-50 dark:bg-rose-900/20 text-rose-700 dark:text-rose-400"
                                        }`}
                                      >
                                        {t.is_active ? "Active" : "Off"}
                                      </button>
                                      <button
                                        onClick={() => handleOpenTopicModal(lesson.id, t)}
                                        className="p-1 text-slate-400 hover:text-slate-700 dark:hover:text-white"
                                      >
                                        <Edit2 className="h-3 w-3" />
                                      </button>
                                      <button
                                        onClick={() => {
                                          if (confirm(`Delete topic "${t.name}"?`)) {
                                            deleteTopicMutation.mutate(t.id);
                                          }
                                        }}
                                        className="p-1 text-slate-400 hover:text-rose-600 dark:hover:text-rose-400"
                                      >
                                        <Trash2 className="h-3 w-3" />
                                      </button>
                                    </div>
                                  </div>
                                ))}
                              </div>
                            )}
                          </div>

                          {/* Child Study Resources Section */}
                          <div className="rounded-2xl bg-brand-50/40 dark:bg-cyan-900/[0.08] border border-brand-100 dark:border-cyan-500/20 p-4 space-y-3">
                            <div className="flex items-center justify-between">
                              <div className="flex items-center gap-1.5 text-xs font-bold text-slate-800 dark:text-slate-200">
                                <Sparkles className="h-3.5 w-3.5 text-brand-600 dark:text-cyan-400" />
                                <span>Verified Study Resources ({lesson.study_resources?.length || 0})</span>
                              </div>
                              <button
                                onClick={() => handleOpenResourceModal(lesson.id)}
                                className="inline-flex items-center gap-1 rounded-lg bg-brand-600 hover:bg-brand-700 text-white px-2 py-1 text-[11px] font-bold transition shadow-xs"
                              >
                                <Plus className="h-3 w-3" />
                                <span>Add Resource</span>
                              </button>
                            </div>

                            {!lesson.study_resources || lesson.study_resources.length === 0 ? (
                              <p className="text-[11px] text-slate-400 italic">No external educational links attached.</p>
                            ) : (
                              <div className="space-y-2">
                                {lesson.study_resources.map((res) => (
                                  <div
                                    key={res.id}
                                    className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 rounded-xl bg-white dark:bg-white/[0.04] border border-slate-200 dark:border-white/[0.06] px-3.5 py-2.5 text-xs shadow-xs"
                                  >
                                    <div className="space-y-0.5">
                                      <div className="flex items-center gap-2">
                                        <span className="font-bold text-slate-900 dark:text-white">{res.title}</span>
                                        <span className="rounded bg-brand-50 dark:bg-cyan-900/20 text-brand-700 dark:text-cyan-300 border border-brand-100 dark:border-cyan-500/20 px-1.5 py-0.2 text-[10px] font-semibold">
                                          {res.provider}
                                        </span>
                                        <span className="rounded bg-slate-100 dark:bg-white/[0.06] px-1.5 py-0.2 text-[10px] font-bold text-slate-600 dark:text-slate-300 uppercase">
                                          {res.resource_type}
                                        </span>
                                      </div>
                                      <a
                                        href={res.url}
                                        target="_blank"
                                        rel="noopener noreferrer"
                                        className="text-[11px] text-brand-600 dark:text-cyan-400 hover:underline flex items-center gap-1"
                                      >
                                        <span>{res.url}</span>
                                        <ExternalLink className="h-2.5 w-2.5" />
                                      </a>
                                    </div>

                                    <div className="flex items-center gap-1.5 shrink-0 self-end sm:self-center">
                                      <button
                                        onClick={() =>
                                          toggleResourceStatusMutation.mutate({
                                            id: res.id,
                                            is_active: !res.is_active,
                                          })
                                        }
                                        className={`rounded-full px-2 py-0.5 text-[10px] font-bold ${
                                          res.is_active ? "bg-emerald-50 dark:bg-emerald-900/20 text-emerald-700 dark:text-emerald-400" : "bg-rose-50 dark:bg-rose-900/20 text-rose-700 dark:text-rose-400"
                                        }`}
                                      >
                                        {res.is_active ? "Active" : "Off"}
                                      </button>
                                      <button
                                        onClick={() => handleOpenResourceModal(lesson.id, res)}
                                        className="p-1 text-slate-400 hover:text-slate-700 dark:hover:text-white"
                                      >
                                        <Edit2 className="h-3 w-3" />
                                      </button>
                                      <button
                                        onClick={() => {
                                          if (confirm(`Delete resource "${res.title}"?`)) {
                                            deleteResourceMutation.mutate(res.id);
                                          }
                                        }}
                                        className="p-1 text-slate-400 hover:text-rose-600 dark:hover:text-rose-400"
                                      >
                                        <Trash2 className="h-3 w-3" />
                                      </button>
                                    </div>
                                  </div>
                                ))}
                              </div>
                            )}
                          </div>
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              </div>
            ) : null}
          </div>
        )}

        {/* ================= MODAL: ADD / EDIT SUBJECT ================= */}
        {showSubjectModal && (
          <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/40 dark:bg-black/60 backdrop-blur-xs p-4">
            <div className="w-full max-w-lg rounded-3xl bg-white dark:bg-[#0B1124] p-6 sm:p-7 shadow-xl space-y-4 border border-slate-100 dark:border-white/[0.08]">
              <h3 className="text-lg font-bold text-slate-900 dark:text-white">
                {editingSubject ? "Edit Subject" : "Create New Academic Subject"}
              </h3>

              <div className="space-y-3 text-xs">
                <div>
                  <label className="font-bold text-slate-700 dark:text-slate-300">Subject Name</label>
                  <input
                    type="text"
                    value={subName}
                    onChange={(e) => setSubName(e.target.value)}
                    placeholder="e.g. Artificial Intelligence & Machine Learning"
                    className="mt-1 w-full rounded-xl border border-slate-200 dark:border-white/[0.08] bg-white dark:bg-white/[0.06] text-slate-900 dark:text-white placeholder:text-slate-400 dark:placeholder:text-slate-500 p-2.5 focus:border-brand-500 dark:focus:border-cyan-500 focus:outline-none"
                  />
                </div>

                <div className="grid grid-cols-2 gap-3">
                  <div>
                    <label className="font-bold text-slate-700 dark:text-slate-300">Subject Code</label>
                    <input
                      type="text"
                      value={subCode}
                      onChange={(e) => setSubCode(e.target.value)}
                      placeholder="e.g. AIML"
                      className="mt-1 w-full rounded-xl border border-slate-200 dark:border-white/[0.08] bg-white dark:bg-white/[0.06] text-slate-900 dark:text-white placeholder:text-slate-400 dark:placeholder:text-slate-500 p-2.5 uppercase focus:border-brand-500 dark:focus:border-cyan-500 focus:outline-none"
                    />
                  </div>

                  <div>
                    <label className="font-bold text-slate-700 dark:text-slate-300">Category</label>
                    <select
                      value={subCategory}
                      onChange={(e) => setSubCategory(e.target.value)}
                      className="mt-1 w-full rounded-xl border border-slate-200 dark:border-white/[0.08] bg-white dark:bg-white/[0.06] text-slate-900 dark:text-white p-2.5 focus:border-brand-500 dark:focus:border-cyan-500 focus:outline-none"
                    >
                      <option value="PROGRAMMING">Programming</option>
                      <option value="DATA_ENGINEERING">Data Engineering</option>
                      <option value="MATHEMATICS">Mathematics</option>
                      <option value="BUSINESS">Business</option>
                      <option value="CLOUD_INFRASTRUCTURE">Cloud Infrastructure</option>
                    </select>
                  </div>
                </div>

                <div className="grid grid-cols-2 gap-3">
                  <div>
                    <label className="font-bold text-slate-700 dark:text-slate-300">Difficulty Level</label>
                    <select
                      value={subDifficulty}
                      onChange={(e) => setSubDifficulty(e.target.value)}
                      className="mt-1 w-full rounded-xl border border-slate-200 dark:border-white/[0.08] bg-white dark:bg-white/[0.06] text-slate-900 dark:text-white p-2.5 focus:border-brand-500 dark:focus:border-cyan-500 focus:outline-none"
                    >
                      <option value="BEGINNER">Beginner</option>
                      <option value="INTERMEDIATE">Intermediate</option>
                      <option value="ADVANCED">Advanced</option>
                    </select>
                  </div>

                  <div>
                    <label className="font-bold text-slate-700 dark:text-slate-300">Student Visibility</label>
                    <div className="mt-2 flex items-center gap-2">
                      <input
                        type="checkbox"
                        id="subActiveCheck"
                        checked={subIsActive}
                        onChange={(e) => setSubIsActive(e.target.checked)}
                        className="rounded border-slate-300 text-brand-600 focus:ring-brand-500 h-4 w-4"
                      />
                      <label htmlFor="subActiveCheck" className="text-xs text-slate-700 dark:text-slate-300 font-medium">
                        Active (Visible to Students)
                      </label>
                    </div>
                  </div>
                </div>

                <div>
                  <label className="font-bold text-slate-700 dark:text-slate-300">Description</label>
                  <textarea
                    rows={3}
                    value={subDesc}
                    onChange={(e) => setSubDesc(e.target.value)}
                    placeholder="Provide curriculum scope and objectives..."
                    className="mt-1 w-full rounded-xl border border-slate-200 dark:border-white/[0.08] bg-white dark:bg-white/[0.06] text-slate-900 dark:text-white placeholder:text-slate-400 dark:placeholder:text-slate-500 p-2.5 focus:border-brand-500 dark:focus:border-cyan-500 focus:outline-none"
                  />
                </div>
              </div>

              <div className="flex items-center justify-end gap-2 pt-2 border-t border-slate-100 dark:border-white/[0.06]">
                <button
                  onClick={() => setShowSubjectModal(false)}
                  className="rounded-xl px-4 py-2 text-xs font-semibold text-slate-600 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-white/[0.06]"
                >
                  Cancel
                </button>
                <button
                  onClick={() => createOrUpdateSubjectMutation.mutate()}
                  disabled={!subName.trim() || !subCode.trim() || createOrUpdateSubjectMutation.isPending}
                  className="rounded-xl bg-brand-600 hover:bg-brand-700 text-white px-4 py-2 text-xs font-bold transition disabled:opacity-50"
                >
                  {createOrUpdateSubjectMutation.isPending ? "Saving..." : editingSubject ? "Save Changes" : "Create Subject"}
                </button>
              </div>
            </div>
          </div>
        )}

        {/* ================= MODAL: ADD / EDIT LESSON ================= */}
        {showLessonModal && (
          <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/40 dark:bg-black/60 backdrop-blur-xs p-4">
            <div className="w-full max-w-xl rounded-3xl bg-white dark:bg-[#0B1124] p-6 sm:p-7 shadow-xl space-y-4 border border-slate-100 dark:border-white/[0.08]">
              <h3 className="text-lg font-bold text-slate-900 dark:text-white">
                {editingLesson ? "Edit Module / Lesson" : "Create New Module / Lesson"}
              </h3>

              <div className="space-y-3 text-xs">
                <div>
                  <label className="font-bold text-slate-700 dark:text-slate-300">Module Title</label>
                  <input
                    type="text"
                    value={lesTitle}
                    onChange={(e) => setLesTitle(e.target.value)}
                    placeholder="e.g. Asynchronous Programming & Promises"
                    className="mt-1 w-full rounded-xl border border-slate-200 dark:border-white/[0.08] bg-white dark:bg-white/[0.06] text-slate-900 dark:text-white placeholder:text-slate-400 dark:placeholder:text-slate-500 p-2.5 focus:border-brand-500 dark:focus:border-cyan-500 focus:outline-none"
                  />
                </div>

                <div className="grid grid-cols-3 gap-3">
                  <div>
                    <label className="font-bold text-slate-700 dark:text-slate-300">Difficulty</label>
                    <select
                      value={lesDifficulty}
                      onChange={(e) => setLesDifficulty(e.target.value)}
                      className="mt-1 w-full rounded-xl border border-slate-200 dark:border-white/[0.08] bg-white dark:bg-white/[0.06] text-slate-900 dark:text-white p-2.5 focus:border-brand-500 dark:focus:border-cyan-500 focus:outline-none"
                    >
                      <option value="EASY">Easy</option>
                      <option value="MEDIUM">Medium</option>
                      <option value="HARD">Hard</option>
                    </select>
                  </div>

                  <div>
                    <label className="font-bold text-slate-700 dark:text-slate-300">Duration (mins)</label>
                    <input
                      type="number"
                      value={lesDuration}
                      onChange={(e) => setLesDuration(Number(e.target.value))}
                      className="mt-1 w-full rounded-xl border border-slate-200 dark:border-white/[0.08] bg-white dark:bg-white/[0.06] text-slate-900 dark:text-white p-2.5 focus:border-brand-500 dark:focus:border-cyan-500 focus:outline-none"
                    />
                  </div>

                  <div>
                    <label className="font-bold text-slate-700 dark:text-slate-300">Active Status</label>
                    <div className="mt-2 flex items-center gap-2">
                      <input
                        type="checkbox"
                        id="lesActiveCheck"
                        checked={lesIsActive}
                        onChange={(e) => setLesIsActive(e.target.checked)}
                        className="rounded border-slate-300 text-brand-600 focus:ring-brand-500 h-4 w-4"
                      />
                      <label htmlFor="lesActiveCheck" className="text-xs text-slate-700 dark:text-slate-300 font-medium">
                        Active
                      </label>
                    </div>
                  </div>
                </div>

                <div>
                  <label className="font-bold text-slate-700 dark:text-slate-300">Short Summary</label>
                  <input
                    type="text"
                    value={lesShortDesc}
                    onChange={(e) => setLesShortDesc(e.target.value)}
                    placeholder="One-line summary shown in syllabus..."
                    className="mt-1 w-full rounded-xl border border-slate-200 dark:border-white/[0.08] bg-white dark:bg-white/[0.06] text-slate-900 dark:text-white placeholder:text-slate-400 dark:placeholder:text-slate-500 p-2.5 focus:border-brand-500 dark:focus:border-cyan-500 focus:outline-none"
                  />
                </div>

                <div>
                  <label className="font-bold text-slate-700 dark:text-slate-300">Lesson Markdown Content</label>
                  <textarea
                    rows={6}
                    value={lesContent}
                    onChange={(e) => setLesContent(e.target.value)}
                    placeholder="Enter comprehensive markdown notes, headers, and code snippets..."
                    className="mt-1 w-full rounded-xl border border-slate-200 dark:border-white/[0.08] bg-white dark:bg-white/[0.06] text-slate-900 dark:text-white placeholder:text-slate-400 dark:placeholder:text-slate-500 p-2.5 font-mono text-xs focus:border-brand-500 dark:focus:border-cyan-500 focus:outline-none"
                  />
                </div>
              </div>

              <div className="flex items-center justify-end gap-2 pt-2 border-t border-slate-100 dark:border-white/[0.06]">
                <button
                  onClick={() => setShowLessonModal(false)}
                  className="rounded-xl px-4 py-2 text-xs font-semibold text-slate-600 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-white/[0.06]"
                >
                  Cancel
                </button>
                <button
                  onClick={() => createOrUpdateLessonMutation.mutate()}
                  disabled={!lesTitle.trim() || createOrUpdateLessonMutation.isPending}
                  className="rounded-xl bg-brand-600 hover:bg-brand-700 text-white px-4 py-2 text-xs font-bold transition disabled:opacity-50"
                >
                  {createOrUpdateLessonMutation.isPending ? "Saving..." : editingLesson ? "Save Changes" : "Create Module"}
                </button>
              </div>
            </div>
          </div>
        )}

        {/* ================= MODAL: ADD / EDIT TOPIC ================= */}
        {showTopicModal && (
          <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/40 dark:bg-black/60 backdrop-blur-xs p-4">
            <div className="w-full max-w-md rounded-3xl bg-white dark:bg-[#0B1124] p-6 shadow-xl space-y-4 border border-slate-100 dark:border-white/[0.08]">
              <h3 className="text-lg font-bold text-slate-900 dark:text-white">
                {editingTopic ? "Edit Child Topic" : "Add Topic Under Module"}
              </h3>

              <div className="space-y-3 text-xs">
                <div>
                  <label className="font-bold text-slate-700 dark:text-slate-300">Topic Name</label>
                  <input
                    type="text"
                    value={topName}
                    onChange={(e) => setTopName(e.target.value)}
                    placeholder="e.g. Event Loop & Microtasks"
                    className="mt-1 w-full rounded-xl border border-slate-200 dark:border-white/[0.08] bg-white dark:bg-white/[0.06] text-slate-900 dark:text-white placeholder:text-slate-400 dark:placeholder:text-slate-500 p-2.5 focus:border-brand-500 dark:focus:border-cyan-500 focus:outline-none"
                  />
                </div>

                <div className="grid grid-cols-2 gap-3">
                  <div>
                    <label className="font-bold text-slate-700 dark:text-slate-300">Difficulty</label>
                    <select
                      value={topDifficulty}
                      onChange={(e) => setTopDifficulty(e.target.value)}
                      className="mt-1 w-full rounded-xl border border-slate-200 dark:border-white/[0.08] bg-white dark:bg-white/[0.06] text-slate-900 dark:text-white p-2.5 focus:border-brand-500 dark:focus:border-cyan-500 focus:outline-none"
                    >
                      <option value="EASY">Easy</option>
                      <option value="MEDIUM">Medium</option>
                      <option value="HARD">Hard</option>
                    </select>
                  </div>

                  <div>
                    <label className="font-bold text-slate-700 dark:text-slate-300">Status</label>
                    <div className="mt-2 flex items-center gap-2">
                      <input
                        type="checkbox"
                        id="topActiveCheck"
                        checked={topIsActive}
                        onChange={(e) => setTopIsActive(e.target.checked)}
                        className="rounded border-slate-300 text-brand-600 focus:ring-brand-500 h-4 w-4"
                      />
                      <label htmlFor="topActiveCheck" className="text-xs text-slate-700 dark:text-slate-300 font-medium">
                        Active
                      </label>
                    </div>
                  </div>
                </div>

                <div>
                  <label className="font-bold text-slate-700 dark:text-slate-300">Description</label>
                  <textarea
                    rows={3}
                    value={topDesc}
                    onChange={(e) => setTopDesc(e.target.value)}
                    placeholder="Core concept definition..."
                    className="mt-1 w-full rounded-xl border border-slate-200 dark:border-white/[0.08] bg-white dark:bg-white/[0.06] text-slate-900 dark:text-white placeholder:text-slate-400 dark:placeholder:text-slate-500 p-2.5 focus:border-brand-500 dark:focus:border-cyan-500 focus:outline-none"
                  />
                </div>
              </div>

              <div className="flex items-center justify-end gap-2 pt-2 border-t border-slate-100 dark:border-white/[0.06]">
                <button
                  onClick={() => setShowTopicModal(false)}
                  className="rounded-xl px-4 py-2 text-xs font-semibold text-slate-600 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-white/[0.06]"
                >
                  Cancel
                </button>
                <button
                  onClick={() => createOrUpdateTopicMutation.mutate()}
                  disabled={!topName.trim() || createOrUpdateTopicMutation.isPending}
                  className="rounded-xl bg-indigo-600 hover:bg-indigo-700 text-white px-4 py-2 text-xs font-bold transition disabled:opacity-50"
                >
                  {createOrUpdateTopicMutation.isPending ? "Saving..." : editingTopic ? "Save Changes" : "Save Topic"}
                </button>
              </div>
            </div>
          </div>
        )}

        {/* ================= MODAL: ADD / EDIT STUDY RESOURCE ================= */}
        {showResourceModal && (
          <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/40 dark:bg-black/60 backdrop-blur-xs p-4">
            <div className="w-full max-w-lg rounded-3xl bg-white dark:bg-[#0B1124] p-6 shadow-xl space-y-4 border border-slate-100 dark:border-white/[0.08]">
              <h3 className="text-lg font-bold text-slate-900 dark:text-white">
                {editingResource ? "Edit Study Resource" : "Attach Verified Study Resource"}
              </h3>

              <div className="space-y-3 text-xs">
                <div>
                  <label className="font-bold text-slate-700 dark:text-slate-300">Resource Title</label>
                  <input
                    type="text"
                    value={resTitle}
                    onChange={(e) => setResTitle(e.target.value)}
                    placeholder="e.g. MDN Web Docs: Asynchronous JavaScript"
                    className="mt-1 w-full rounded-xl border border-slate-200 dark:border-white/[0.08] bg-white dark:bg-white/[0.06] text-slate-900 dark:text-white placeholder:text-slate-400 dark:placeholder:text-slate-500 p-2.5 focus:border-brand-500 dark:focus:border-cyan-500 focus:outline-none"
                  />
                </div>

                <div>
                  <label className="font-bold text-slate-700 dark:text-slate-300">External URL</label>
                  <div className="mt-1 flex items-center gap-2">
                    <input
                      type="url"
                      value={resUrl}
                      onChange={(e) => setResUrl(e.target.value)}
                      placeholder="https://developer.mozilla.org/..."
                      className="w-full rounded-xl border border-slate-200 dark:border-white/[0.08] bg-white dark:bg-white/[0.06] text-slate-900 dark:text-white placeholder:text-slate-400 dark:placeholder:text-slate-500 p-2.5 focus:border-brand-500 dark:focus:border-cyan-500 focus:outline-none"
                    />
                    {resUrl && (
                      <a
                        href={resUrl}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="rounded-xl border border-slate-200 dark:border-white/[0.08] bg-slate-50 dark:bg-white/[0.04] p-2.5 text-slate-600 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-white/[0.08]"
                        title="Test Link"
                      >
                        <ExternalLink className="h-4 w-4" />
                      </a>
                    )}
                  </div>
                </div>

                <div className="grid grid-cols-2 gap-3">
                  <div>
                    <label className="font-bold text-slate-700 dark:text-slate-300">Resource Type</label>
                    <select
                      value={resType}
                      onChange={(e) => setResType(e.target.value)}
                      className="mt-1 w-full rounded-xl border border-slate-200 dark:border-white/[0.08] bg-white dark:bg-white/[0.06] text-slate-900 dark:text-white p-2.5 focus:border-brand-500 dark:focus:border-cyan-500 focus:outline-none"
                    >
                      <option value="DOCUMENTATION">Documentation</option>
                      <option value="TUTORIAL">Tutorial</option>
                      <option value="ARTICLE">Article / Deep Dive</option>
                      <option value="PRACTICE">Interactive Practice</option>
                      <option value="CHEATSHEET">Cheatsheet</option>
                      <option value="VIDEO">Video</option>
                    </select>
                  </div>

                  <div>
                    <label className="font-bold text-slate-700 dark:text-slate-300">Provider Name</label>
                    <input
                      type="text"
                      value={resProvider}
                      onChange={(e) => setResProvider(e.target.value)}
                      placeholder="e.g. MDN, W3Schools, Python Docs..."
                      className="mt-1 w-full rounded-xl border border-slate-200 dark:border-white/[0.08] bg-white dark:bg-white/[0.06] text-slate-900 dark:text-white placeholder:text-slate-400 dark:placeholder:text-slate-500 p-2.5 focus:border-brand-500 dark:focus:border-cyan-500 focus:outline-none"
                    />
                  </div>
                </div>

                {/* Quick Provider Suggestions */}
                <div className="flex flex-wrap items-center gap-1.5 pt-1">
                  <span className="text-[10px] text-slate-400 font-semibold">Quick Presets:</span>
                  {[
                    "MDN Web Docs",
                    "Python Official Docs",
                    "Oracle Java Docs",
                    "PostgreSQL Tutorial",
                    "W3Schools",
                    "Khan Academy",
                    "freeCodeCamp",
                    "GeeksforGeeks",
                  ].map((p) => (
                    <button
                      key={p}
                      type="button"
                      onClick={() => setResProvider(p)}
                      className="rounded bg-slate-100 dark:bg-white/[0.06] px-2 py-0.5 text-[10px] font-medium text-slate-600 dark:text-slate-300 hover:bg-brand-50 dark:hover:bg-cyan-900/20 hover:text-brand-700 dark:hover:text-cyan-300"
                    >
                      {p}
                    </button>
                  ))}
                </div>

                <div>
                  <label className="font-bold text-slate-700 dark:text-slate-300">Description</label>
                  <textarea
                    rows={2}
                    value={resDesc}
                    onChange={(e) => setResDesc(e.target.value)}
                    placeholder="Brief description of what this resource covers..."
                    className="mt-1 w-full rounded-xl border border-slate-200 dark:border-white/[0.08] bg-white dark:bg-white/[0.06] text-slate-900 dark:text-white placeholder:text-slate-400 dark:placeholder:text-slate-500 p-2.5 focus:border-brand-500 dark:focus:border-cyan-500 focus:outline-none"
                  />
                </div>
              </div>

              <div className="flex items-center justify-end gap-2 pt-2 border-t border-slate-100 dark:border-white/[0.06]">
                <button
                  onClick={() => setShowResourceModal(false)}
                  className="rounded-xl px-4 py-2 text-xs font-semibold text-slate-600 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-white/[0.06]"
                >
                  Cancel
                </button>
                <button
                  onClick={() => createOrUpdateResourceMutation.mutate()}
                  disabled={!resTitle.trim() || !resUrl.trim() || createOrUpdateResourceMutation.isPending}
                  className="rounded-xl bg-brand-600 hover:bg-brand-700 text-white px-4 py-2 text-xs font-bold transition disabled:opacity-50"
                >
                  {createOrUpdateResourceMutation.isPending ? "Saving..." : editingResource ? "Save Changes" : "Attach Resource"}
                </button>
              </div>
            </div>
          </div>
        )}
      </div>
    </RoleLayout>
  );
}
