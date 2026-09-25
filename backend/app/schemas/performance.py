from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class TopicPerformanceOut(BaseModel):
    topic_id: int
    topic_name: str
    subject_id: int
    subject_name: str
    attempts: int
    correct_answers: int
    total_questions: int
    accuracy: float
    mastery_score: float
    difficulty_level: str
    status: str  # WEAK (<40), NEEDS_PRACTICE (40-69), MASTERED (>=70)
    last_attempt_at: datetime

    class Config:
        from_attributes = True

class PerformanceOverviewOut(BaseModel):
    overall_progress: float
    average_quiz_score: float
    lessons_completed: int
    total_lessons: int
    current_streak: int
    total_quizzes_taken: int
    weak_topics: List[TopicPerformanceOut]
    strong_topics: List[TopicPerformanceOut]

class HistoryItem(BaseModel):
    date: str
    score: float
    quiz_title: str
    subject_name: str

class PerformanceHistoryOut(BaseModel):
    score_trends: List[HistoryItem]
    subject_progress: List[dict]
    topic_mastery: List[dict]
