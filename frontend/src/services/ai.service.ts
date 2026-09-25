import { api } from "@/lib/api";

export interface AIChatResponse {
  reply: string;
  conversation_id: number;
  hints: string[];
  recommended_topics: string[];
}

export interface AIMessage {
  id: number;
  role: "user" | "assistant" | "system";
  content: string;
  created_at: string;
}

export interface AIConversation {
  id: number;
  title: string;
  created_at: string;
  messages: AIMessage[];
}

export const aiService = {
  chat: (data: {
    message: string;
    conversation_id?: number;
    subject_id?: number;
    topic_id?: number;
    is_during_quiz?: boolean;
  }) => api.post<AIChatResponse>("/api/ai/chat", data),
  getConversations: () => api.get<AIConversation[]>("/api/ai/conversations"),
  getConversation: (id: number) => api.get<AIConversation>(`/api/ai/conversations/${id}`),
};
