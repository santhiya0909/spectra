import { api } from "@/lib/api";

export type PuzzleType = 
  | "MULTIPLE_CHOICE" 
  | "TRUE_FALSE" 
  | "FILL_BLANK" 
  | "CODE_OUTPUT" 
  | "ORDERING" 
  | "MATCHING";

export interface Puzzle {
  id: number;
  subject_id: number;
  lesson_id: number;
  topic_id?: number | null;
  title: string;
  description?: string | null;
  puzzle_type: PuzzleType;
  question: string;
  puzzle_data: any; // options list, snippet string, ordering list, matching pairs
  difficulty: "EASY" | "MEDIUM" | "HARD";
  xp_reward: number;
  display_order: number;
  is_active: boolean;
  user_solved?: boolean;
  user_attempts?: number;
  topic_name?: string | null;
  lesson_title?: string | null;
  subject_name?: string | null;
  estimated_time?: string;
  instructions?: string | null;
  puzzle_index?: number;
  total_in_lesson?: number;
  created_at?: string;
  updated_at?: string;
}

export interface PuzzleSubmissionResult {
  is_correct: boolean;
  xp_earned: number;
  explanation?: string | null;
  hint?: string | null;
  attempts_count: number;
  lesson_progress_percentage: number;
  lesson_completed: boolean;
  topic_id?: number | null;
  topic_name?: string | null;
  mastery_before?: number | null;
  mastery_after?: number | null;
  mastery_state_before?: string | null;
  mastery_state_after?: string | null;
  spectra_feedback?: string | null;
  recommended_action?: string | null;
  recommended_video?: {
    video_id: string;
    title: string;
    thumbnail_url: string;
    channel_name: string;
    url: string;
  } | null;
  next_puzzle_id?: number | null;
  next_lesson_id?: number | null;
}

export interface StudentPuzzleProgressOut {
  total_solved: number;
  total_puzzles: number;
  total_xp: number;
  accuracy: number;
  topics_strengthened: number;
  total_attempts: number;
  recent_attempts: Array<{
    puzzle_id: number;
    puzzle_title: string;
    is_correct: boolean;
    attempts_count: number;
    xp_earned: number;
    completed_at: string;
  }>;
}

export const puzzleService = {
  getPuzzles: (params?: { subjectId?: number; lessonId?: number; topicId?: number; filter?: string }) => {
    const query = new URLSearchParams();
    if (params?.subjectId) query.set("subject_id", params.subjectId.toString());
    if (params?.lessonId) query.set("lesson_id", params.lessonId.toString());
    if (params?.topicId) query.set("topic_id", params.topicId.toString());
    if (params?.filter) query.set("filter", params.filter);
    const qs = query.toString();
    return api.get<Puzzle[]>(`/api/puzzles${qs ? `?${qs}` : ""}`);
  },

  getRecommendedPuzzle: () =>
    api.get<Puzzle | null>("/api/puzzles/recommended"),

  getLessonPuzzles: (lessonId: number) => 
    api.get<Puzzle[]>(`/api/lessons/${lessonId}/puzzles`),

  getPuzzle: (puzzleId: number) => 
    api.get<Puzzle>(`/api/puzzles/${puzzleId}`),

  submitPuzzle: (puzzleId: number, answer: any, timeTaken: number = 0) =>
    api.post<PuzzleSubmissionResult>(`/api/puzzles/${puzzleId}/submit`, {
      submitted_answer: answer,
      time_taken: timeTaken,
    }),

  getStudentProgress: () =>
    api.get<StudentPuzzleProgressOut>("/api/students/me/puzzle-progress"),

  getLessonQuiz: (lessonId: number) =>
    api.get<{
      quiz_id: number;
      title: string;
      difficulty: string;
      question_count: number;
      best_score: number | null;
      questions: Array<{
        id: number;
        question_text: string;
        options: string[];
        difficulty: string;
      }>;
    }>(`/api/lessons/${lessonId}/quiz`),

  getTopicPractice: (topicId: number) =>
    api.get<Array<{
      id: number;
      question_text: string;
      options: string[];
      difficulty: string;
    }>>(`/api/topics/${topicId}/practice`),

  submitTopicPractice: (topicId: number, answers: any[] = []) =>
    api.post<{
      xp_earned: number;
      message: string;
      completed: boolean;
      total_xp?: number;
    }>(`/api/topics/${topicId}/practice/submit`, { answers }),
};
