import { api } from "@/lib/api";

export interface Recommendation {
  id: number;
  topic_id: number;
  topic_name: string;
  subject_name: string;
  recommendation_type: string;
  title: string;
  reason: string;
  priority: "HIGH" | "MEDIUM" | "LOW";
  resource_id?: number | null;
  status: "ACTIVE" | "COMPLETED" | "DISMISSED";
  created_at: string;
}

export const recommendationService = {
  getRecommendations: () => api.get<Recommendation[]>("/api/recommendations"),
  completeRecommendation: (id: number) => api.post(`/api/recommendations/${id}/complete`),
  generateRecommendations: () => api.post<Recommendation[]>("/api/recommendations/generate"),
};
