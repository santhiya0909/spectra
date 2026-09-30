from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from datetime import datetime

class TeacherAlertOut(BaseModel):
    id: int
    student_id: int
    student_name: str
    topic_id: int
    topic_name: str
    alert_type: str  # LOW_PERFORMANCE, REPEATED_FAILURE, LOW_ACTIVITY, IMPROVING, MASTERY_ACHIEVED
    severity: str    # HIGH, MEDIUM, LOW
    message: str
    status: str      # ACTIVE, REVIEWED, RESOLVED
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class AlertUpdate(BaseModel):
    status: str  # ACTIVE, REVIEWED, RESOLVED

class TopicGapOut(BaseModel):
    topic_id: int
    topic_name: str
    subject_name: str
    class_average_accuracy: float
    total_students_assessed: int
    students_needing_intervention: int
    difficulty: str

class StudentSummaryOut(BaseModel):
    id: int
    student_profile_id: int
    name: str
    email: str
    student_id: str
    department: str
    average_score: float
    quizzes_completed: int
    weak_topics_count: int
    at_risk: bool

class TeacherDashboardOut(BaseModel):
    total_students: int
    average_class_performance: float
    completion_rate: float
    students_needing_attention: int
    recent_alerts: List[TeacherAlertOut]
    topic_gaps: List[TopicGapOut]
