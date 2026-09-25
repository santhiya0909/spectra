import { api } from "@/lib/api";

export interface Question {
  id: number;
  subject_id: number;
  topic_id: number;
  topic_name: string;
  question_text: string;
  question_type: string;
  options: string[];
  difficulty: string;
}

export interface Quiz {
  id: number;
  subject_id: number;
  subject_name?: string;
  title: string;
  description: string;
  quiz_type: string;
  difficulty: string;
  question_count: number;
  best_score?: number | null;
  attempts_count?: number;
}

export interface QuestionReview {
  id: number;
  question_text: string;
  options: string[];
  selected_answer: string;
  correct_answer: string;
  is_correct: boolean;
  explanation: string;
  topic_id: number;
  topic_name: string;
}

export interface QuizResult {
  attempt_id: number;
  quiz_id: number;
  quiz_title: string;
  score: number;
  total_questions: number;
  percentage: number;
  status: string;
  questions_review: QuestionReview[];
  weak_topics: string[];
  recommendations_generated: string[];
}

export const quizService = {
  getQuizzes: (subjectId?: number) =>
    api.get<Quiz[]>(`/api/quizzes${subjectId ? `?subject_id=${subjectId}` : ""}`),
  getQuiz: (quizId: number) => api.get<Quiz>(`/api/quizzes/${quizId}`),
  startQuiz: (quizId: number) => api.post<Question[]>(`/api/quizzes/${quizId}/start`),
  submitQuiz: (quizId: number, answers: Array<{ question_id: number; selected_answer: string; time_taken: number }>) =>
    api.post<QuizResult>(`/api/quizzes/${quizId}/submit`, { answers }),
  getAttempts: () => api.get<any[]>("/api/quizzes/attempts"),
  getAttemptDetail: (attemptId: number) => api.get<QuizResult>(`/api/quizzes/attempts/${attemptId}`),
};
