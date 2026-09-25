import { api } from "@/lib/api";
import { Subject, Lesson, Topic, StudyResource } from "./subject.service";

export interface AdminDashboardData {
  total_users: number;
  total_students: number;
  total_teachers: number;
  total_subjects: number;
  total_quizzes: number;
  total_questions: number;
  recent_logs: Array<{
    id: number;
    user_name: string;
    action: string;
    entity: string;
    entity_id: string;
    created_at: string;
  }>;
}

export interface AdminSubjectFilter {
  search?: string;
  category?: string;
  difficulty?: string;
  is_active?: boolean;
}

export const adminService = {
  // Dashboard & Users
  getDashboard: () => api.get<AdminDashboardData>("/api/admin/dashboard"),
  getUsers: () => api.get<any[]>("/api/admin/users"),
  updateUserRole: (id: number, role: string) => api.patch(`/api/admin/users/${id}/role`, { role }),

  // Subjects CRUD & Order & Status
  getSubjects: (params?: AdminSubjectFilter | any) => {
    const sp = new URLSearchParams();
    if (params && typeof params === "object" && !("queryKey" in params)) {
      if (params.search) sp.append("search", params.search);
      if (params.category) sp.append("category", params.category);
      if (params.difficulty) sp.append("difficulty", params.difficulty);
      if (params.is_active !== undefined) sp.append("is_active", params.is_active.toString());
    }
    const qs = sp.toString();
    return api.get<Subject[]>(`/api/admin/subjects${qs ? `?${qs}` : ""}`);
  },
  getSubject: (id: number) => api.get<Subject>(`/api/admin/subjects/${id}`),
  createSubject: (data: Partial<Subject>) => api.post<Subject>("/api/admin/subjects", data),
  updateSubject: (id: number, data: Partial<Subject>) => api.patch<Subject>(`/api/admin/subjects/${id}`, data),
  toggleSubjectStatus: (id: number, is_active: boolean) =>
    api.patch<{ message: string; id: number; is_active: boolean }>(`/api/admin/subjects/${id}/status`, { is_active }),
  reorderSubjects: (items: { id: number; order: number }[]) =>
    api.post<{ message: string }>("/api/admin/subjects/reorder", { items }),
  deleteSubject: (id: number) => api.delete<{ message: string; id: number }>(`/api/admin/subjects/${id}`),

  // Lessons CRUD & Order & Status
  getSubjectLessons: (subjectId: number) => api.get<Lesson[]>(`/api/admin/subjects/${subjectId}/lessons`),
  createLesson: (subjectId: number, data: Partial<Lesson>) =>
    api.post<Lesson>(`/api/admin/subjects/${subjectId}/lessons`, data),
  getLesson: (id: number) => api.get<Lesson>(`/api/admin/lessons/${id}`),
  updateLesson: (id: number, data: Partial<Lesson>) => api.patch<Lesson>(`/api/admin/lessons/${id}`, data),
  toggleLessonStatus: (id: number, is_active: boolean) =>
    api.patch<{ message: string; id: number; is_active: boolean }>(`/api/admin/lessons/${id}/status`, { is_active }),
  reorderLessons: (items: { id: number; order: number }[]) =>
    api.post<{ message: string }>("/api/admin/lessons/reorder", { items }),
  deleteLesson: (id: number) => api.delete<{ message: string; id: number }>(`/api/admin/lessons/${id}`),

  // Topics CRUD & Order & Status
  getTopics: (params?: { subject_id?: number; lesson_id?: number } | any) => {
    const sp = new URLSearchParams();
    if (params && typeof params === "object" && !("queryKey" in params)) {
      if (params.subject_id) sp.append("subject_id", params.subject_id.toString());
      if (params.lesson_id) sp.append("lesson_id", params.lesson_id.toString());
    }
    const qs = sp.toString();
    return api.get<Topic[]>(`/api/admin/topics${qs ? `?${qs}` : ""}`);
  },

  getTopic: (id: number) => api.get<Topic>(`/api/admin/topics/${id}`),
  createTopic: (data: Partial<Topic>) => api.post<Topic>("/api/admin/topics", data),
  updateTopic: (id: number, data: Partial<Topic>) => api.patch<Topic>(`/api/admin/topics/${id}`, data),
  toggleTopicStatus: (id: number, is_active: boolean) =>
    api.patch<{ message: string; id: number; is_active: boolean }>(`/api/admin/topics/${id}/status`, { is_active }),
  reorderTopics: (items: { id: number; order: number }[]) =>
    api.post<{ message: string }>("/api/admin/topics/reorder", { items }),
  deleteTopic: (id: number) => api.delete<{ message: string; id: number }>(`/api/admin/topics/${id}`),

  // Study Resources CRUD & Order & Status
  getLessonResources: (lessonId: number) => api.get<StudyResource[]>(`/api/admin/lessons/${lessonId}/resources`),
  createResource: (lessonId: number, data: Partial<StudyResource>) =>
    api.post<StudyResource>(`/api/admin/lessons/${lessonId}/resources`, data),
  getResource: (id: number) => api.get<StudyResource>(`/api/admin/resources/${id}`),
  updateResource: (id: number, data: Partial<StudyResource>) =>
    api.patch<StudyResource>(`/api/admin/resources/${id}`, data),
  toggleResourceStatus: (id: number, is_active: boolean) =>
    api.patch<{ message: string; id: number; is_active: boolean }>(`/api/admin/resources/${id}/status`, { is_active }),
  reorderResources: (items: { id: number; order: number }[]) =>
    api.post<{ message: string }>("/api/admin/resources/reorder", { items }),
  deleteResource: (id: number) => api.delete<{ message: string; id: number }>(`/api/admin/resources/${id}`),

  // Questions & Quizzes
  getQuestions: () => api.get<any[]>("/api/admin/questions"),
  createQuestion: (data: any) => api.post("/api/admin/questions", data),
  deleteQuestion: (id: number) => api.delete(`/api/admin/questions/${id}`),
  getQuizzes: () => api.get<any[]>("/api/admin/quizzes"),
  createQuiz: (data: any) => api.post("/api/admin/quizzes", data),
};
