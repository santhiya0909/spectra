import { api } from "@/lib/api";

export interface StudentDashboardData {
  greeting: string;
  student: {
    name: string;
    student_id: string;
    department: string;
    semester: number;
  };
  overall_progress: number;
  average_quiz_score: number;
  lessons_completed: number;
  total_lessons: number;
  current_streak: number;
  xp?: number;
  puzzles_solved?: number;
  topics_mastered?: number;
  continue_learning_card?: {
    subject_id?: number;
    subject_name: string;
    subject_code?: string;
    lesson_id: number;
    lesson_title: string;
    progress?: number;
    progress_percentage?: number;
    next_action?: string;
    lesson_order?: number;
  };
  today_learning_path?: Array<{
    id?: number;
    step?: number;
    resource_id?: number;
    title: string;
    type: string;
    status?: string;
    completed?: boolean;
    xp_reward?: number;
    duration_minutes?: number;
    url?: string;
    is_current?: boolean;
  }>;
  recent_achievements?: Array<{
    id: string;
    title: string;
    description: string;
    icon: string;
    earned_at: string;
    xp: number;
  }>;
  weak_topics: Array<{
    topic_id: number;
    topic_name: string;
    accuracy: number;
    mastery_score: number;
    status: string;
  }>;
  recommended_next_activity: {
    id?: number;
    title: string;
    reason: string;
    priority: string;
    resource_id?: number;
    recommendation_type: string;
    topic_name?: string;
  };
  recent_quiz_results: Array<{
    attempt_id: number;
    quiz_id: number;
    quiz_title: string;
    subject_name: string;
    score: number;
    percentage: number;
    completed_at: string;
  }>;
  subject_progress: Array<{
    subject_id: number;
    subject_name: string;
    code: string;
    completed_lessons: number;
    total_lessons: number;
    percentage: number;
    current_lesson?: {
      id: number;
      title: string;
    } | null;
  }>;
  today_learning_plan: Array<{
    id: number;
    resource_type: string;
    resource_id: number;
    title: string;
    description: string;
    order_index: number;
    completed: boolean;
  }>;
}

export interface TopicPerformance {
  topic_id: number;
  topic_name: string;
  subject_id: number;
  subject_name: string;
  attempts: number;
  correct_answers: number;
  total_questions: number;
  accuracy: number;
  mastery_score: number;
  difficulty_level: string;
  status: "WEAK" | "NEEDS_PRACTICE" | "MASTERED";
  last_attempt_at: string;
}

export interface PerformanceHistory {
  score_trends: Array<{
    date: string;
    score: number;
    quiz_title: string;
    subject_name: string;
  }>;
  subject_progress: Array<{
    subject: string;
    progress: number;
    completed: number;
    total: number;
  }>;
  topic_mastery: Array<{
    topic: string;
    mastery: number;
    accuracy: number;
  }>;
}

export const studentService = {
  getDashboard: () => api.get<StudentDashboardData>("/api/students/me/dashboard"),
  getProfile: () => api.get<any>("/api/students/me"),
  getPerformanceOverview: () => api.get<any>("/api/performance/overview"),
  getTopicPerformances: () => api.get<TopicPerformance[]>("/api/performance/topics"),
  getPerformanceHistory: () => api.get<PerformanceHistory>("/api/performance/history"),
  getLearningPlan: () => api.get<any>("/api/students/me/learning-plan"),
};
