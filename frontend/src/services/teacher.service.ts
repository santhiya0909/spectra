import { api } from "@/lib/api";

export interface TeacherAlert {
  id: number;
  student_id: number;
  student_name: string;
  topic_id: number;
  topic_name: string;
  alert_type: string;
  severity: "HIGH" | "MEDIUM" | "LOW";
  message: string;
  status: "ACTIVE" | "REVIEWED" | "RESOLVED";
  created_at: string;
}

export interface TopicGap {
  topic_id: number;
  topic_name: string;
  subject_name: string;
  class_average_accuracy: number;
  total_students_assessed: number;
  students_needing_intervention: number;
  difficulty: string;
}

export interface StudentSummary {
  id: number;
  student_profile_id: number;
  name: string;
  email: string;
  student_id: string;
  department: string;
  average_score: number;
  quizzes_completed: number;
  weak_topics_count: number;
  at_risk: boolean;
}

export interface TeacherDashboardData {
  total_students: number;
  average_class_performance: number;
  completion_rate: number;
  students_needing_attention: number;
  recent_alerts: TeacherAlert[];
  topic_gaps: TopicGap[];
}

export const teacherService = {
  getDashboard: () => api.get<TeacherDashboardData>("/api/teacher/dashboard"),
  getStudents: () => api.get<StudentSummary[]>("/api/teacher/students"),
  getStudentDetail: (studentId: number) => api.get<any>(`/api/teacher/students/${studentId}`),
  getTopicGaps: () => api.get<TopicGap[]>("/api/teacher/topic-gaps"),
  getAlerts: () => api.get<TeacherAlert[]>("/api/teacher/alerts"),
  updateAlertStatus: (alertId: number, status: "ACTIVE" | "REVIEWED" | "RESOLVED") =>
    api.patch<TeacherAlert>(`/api/teacher/alerts/${alertId}`, { status }),
};
