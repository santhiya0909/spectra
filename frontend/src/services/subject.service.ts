import { api } from "@/lib/api";

export interface StudyResource {
  id: number;
  lesson_id: number;
  topic_id?: number | null;
  title: string;
  description?: string | null;
  url: string;
  resource_type: string; // DOCUMENTATION, ARTICLE, VIDEO, TUTORIAL, CHEATSHEET, PRACTICE
  provider: string;
  display_order: number;
  is_active: boolean;
  created_at?: string;
  updated_at?: string;
}

export interface Topic {
  id: number;
  subject_id: number;
  lesson_id?: number | null;
  name: string;
  description?: string | null;
  difficulty_level: string;
  display_order: number;
  is_active: boolean;
  study_resources?: StudyResource[];
  created_at?: string;
  updated_at?: string;
}

export interface Lesson {
  id: number;
  subject_id: number;
  topic_id?: number | null;
  topic_name?: string | null;
  subject_name?: string | null;
  title: string;
  short_description?: string | null;
  detailed_description?: string | null;
  description?: string | null;
  content?: string | null;
  resource_url?: string | null;
  difficulty?: string;
  difficulty_level?: string;
  estimated_minutes?: number;
  estimated_duration?: number;
  lesson_order: number;
  display_order: number;
  is_active: boolean;
  status: "NOT_STARTED" | "IN_PROGRESS" | "COMPLETED";
  completion_percentage: number;
  topics?: Topic[];
  study_resources?: StudyResource[];
  created_at?: string;
  updated_at?: string;
}

export interface Subject {
  id: number;
  name: string;
  code: string;
  description?: string | null;
  category?: string;
  difficulty_level?: string;
  thumbnail_url?: string | null;
  display_order: number;
  is_active: boolean;
  topics?: Topic[];
  lessons?: Lesson[];
  lessons_count: number;
  quizzes_count: number;
  progress_percentage: number;
  created_at?: string;
  updated_at?: string;
}

export interface SubjectQueryParams {
  search?: string;
  category?: string;
  difficulty?: string;
}

export const subjectService = {
  getSubjects: (params?: SubjectQueryParams | any) => {
    const sp = new URLSearchParams();
    if (params && typeof params === "object" && !("queryKey" in params)) {
      if (params.search) sp.append("search", params.search);
      if (params.category) sp.append("category", params.category);
      if (params.difficulty) sp.append("difficulty", params.difficulty);
    }
    const qs = sp.toString();
    return api.get<Subject[]>(`/api/subjects${qs ? `?${qs}` : ""}`);
  },

  getSubject: (id: number) => api.get<Subject>(`/api/subjects/${id}`),
  getSubjectTopics: (id: number) => api.get<Topic[]>(`/api/subjects/${id}/topics`),
  getLessons: (params?: { subjectId?: number; topicId?: number; search?: string; difficulty?: string }) => {
    const sp = new URLSearchParams();
    if (params?.subjectId) sp.append("subject_id", params.subjectId.toString());
    if (params?.topicId) sp.append("topic_id", params.topicId.toString());
    if (params?.search) sp.append("search", params.search);
    if (params?.difficulty) sp.append("difficulty", params.difficulty);
    const qs = sp.toString();
    return api.get<Lesson[]>(`/api/lessons${qs ? `?${qs}` : ""}`);
  },
  getLesson: (id: number) => api.get<Lesson>(`/api/lessons/${id}`),
  updateLessonProgress: (id: number, status: string, completion_percentage: number) =>
    api.post<{ message: string; status: string; completion_percentage: number }>(`/api/lessons/${id}/progress`, {
      status,
      completion_percentage,
    }),
};
