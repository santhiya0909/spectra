from pydantic import BaseModel, Field
from typing import Optional, List, Any
from datetime import datetime

class QuestionBase(BaseModel):
    subject_id: int
    topic_id: int
    question_text: str
    question_type: str = "MCQ"
    options: List[str]
    correct_answer: str
    explanation: Optional[str] = None
    difficulty: str = "MEDIUM"

class QuestionCreate(QuestionBase):
    pass

class QuestionOut(BaseModel):
    id: int
    subject_id: int
    topic_id: int
    topic_name: Optional[str] = None
    question_text: str
    question_type: str
    options: List[str]
    difficulty: str

    class Config:
        from_attributes = True

class QuestionReviewOut(BaseModel):
    id: int
    question_text: str
    options: List[str]
    selected_answer: Optional[str] = None
    correct_answer: str
    is_correct: bool
    explanation: Optional[str] = None
    topic_id: int
    topic_name: str

class QuizBase(BaseModel):
    subject_id: int
    title: str
    description: Optional[str] = None
    quiz_type: str = "TOPIC_ASSESSMENT"
    difficulty: str = "MEDIUM"
    question_count: int = 5

class QuizCreate(QuizBase):
    question_ids: Optional[List[int]] = None

class QuizOut(QuizBase):
    id: int
    subject_name: Optional[str] = None
    best_score: Optional[float] = None
    attempts_count: Optional[int] = 0

    class Config:
        from_attributes = True

class QuizDetailOut(QuizOut):
    questions: List[QuestionOut] = []

class QuizSubmissionItem(BaseModel):
    question_id: int
    selected_answer: Optional[str] = None
    time_taken: int = 0

class QuizSubmission(BaseModel):
    answers: List[QuizSubmissionItem]

class QuizAttemptOut(BaseModel):
    id: int
    quiz_id: int
    quiz_title: str
    subject_name: str
    score: float
    percentage: float
    started_at: datetime
    completed_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class QuizResultOut(BaseModel):
    attempt_id: int
    quiz_id: int
    quiz_title: str
    score: float
    total_questions: int
    percentage: float
    status: str
    questions_review: List[QuestionReviewOut]
    weak_topics: List[str]
    recommendations_generated: List[str]
