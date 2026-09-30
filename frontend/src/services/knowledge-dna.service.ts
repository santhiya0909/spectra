import { api } from "@/lib/api";
import { YouTubeVideoRecommendation } from "./subject.service";

export type MasteryState = "MASTERED" | "DEVELOPING" | "WEAK" | "NOT_STARTED" | "LOCKED";

export interface KnowledgeDNANode {
  id: number;
  name: string;
  description?: string | null;
  lesson_id?: number | null;
  lesson_title?: string | null;
  lesson_order: number;
  display_order: number;
  difficulty_level: string;
  mastery_score: number;
  mastery_state: MasteryState;
  recent_quiz_score?: number | null;
  attempts_count: number;
  correct_answers: number;
  total_questions: number;
  lesson_completed: boolean;
  prerequisite_gap: boolean;
  prerequisite_names: string[];
  prerequisite_ids: number[];
  dependent_names: string[];
  why_weak_explanation?: string | null;
  recommended_action?: string | null;
}

export interface KnowledgeDNAEdge {
  source: number;
  target: number;
  source_name: string;
  target_name: string;
  status: "SATISFIED" | "GAP" | "LOCKED";
}

export interface KnowledgeDNAFocusRecommendation {
  topic_id: number;
  topic_name: string;
  lesson_id?: number | null;
  lesson_title?: string | null;
  mastery_score: number;
  mastery_state: string;
  reason: string;
  prerequisite_impact?: string | null;
  action_plan: string[];
}

export interface KnowledgeDNASummary {
  subject_id: number;
  subject_name: string;
  subject_code: string;
  overall_mastery: number;
  mastered_count: number;
  developing_count: number;
  weak_count: number;
  not_started_count: number;
  locked_count: number;
  total_topics: number;
  recommended_focus?: KnowledgeDNAFocusRecommendation | null;
}

export interface KnowledgeDNAResponse {
  subject_id: number;
  subject_name: string;
  subject_code: string;
  overall_mastery: number;
  mastered_count: number;
  developing_count: number;
  weak_count: number;
  not_started_count: number;
  locked_count: number;
  total_topics: number;
  recommended_focus?: KnowledgeDNAFocusRecommendation | null;
  nodes: KnowledgeDNANode[];
  edges: KnowledgeDNAEdge[];
  strong_areas: KnowledgeDNANode[];
  developing_areas: KnowledgeDNANode[];
  weak_areas: KnowledgeDNANode[];
  not_started_areas: KnowledgeDNANode[];
}

export interface TopicKnowledgeDNADetail {
  node: KnowledgeDNANode;
  prerequisites: Array<{
    topic_id: number;
    name: string;
    mastery_score: number;
    mastery_state: string;
    lesson_id?: number | null;
  }>;
  dependents: Array<{
    topic_id: number;
    name: string;
    mastery_score: number;
    mastery_state: string;
    lesson_id?: number | null;
  }>;
  recent_attempts: Array<{
    attempt_id: number;
    score: number;
    percentage: number;
    completed_at?: string | null;
  }>;
  puzzle_attempts?: Array<{
    attempt_id: number;
    puzzle_id: number;
    puzzle_title: string;
    is_correct: boolean;
    xp_earned: number;
    completed_at?: string | null;
  }>;
  puzzle_accuracy?: number | null;
  puzzle_solved_count?: number;
  puzzle_total_count?: number;
  youtube_videos: YouTubeVideoRecommendation[];
}

export const knowledgeDnaService = {
  getKnowledgeDNA: (subjectId?: number) => {
    const qs = subjectId ? `?subject_id=${subjectId}` : "";
    return api.get<KnowledgeDNAResponse>(`/api/knowledge-dna${qs}`);
  },
  getKnowledgeDNASummary: (subjectId?: number) => {
    const qs = subjectId ? `?subject_id=${subjectId}` : "";
    return api.get<KnowledgeDNASummary>(`/api/knowledge-dna/summary${qs}`);
  },
  getTopicDNADetail: (topicId: number) => {
    return api.get<TopicKnowledgeDNADetail>(`/api/knowledge-dna/topics/${topicId}`);
  },
};
