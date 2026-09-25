from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class RecommendationOut(BaseModel):
    id: int
    topic_id: int
    topic_name: str
    subject_name: str
    recommendation_type: str  # FOUNDATIONAL_LESSON, CONCEPT_REVISION, TARGETED_PRACTICE, RETAKE_QUIZ, ADVANCED_CHALLENGE
    title: str
    reason: str
    priority: str  # HIGH, MEDIUM, LOW
    resource_id: Optional[int] = None
    status: str  # ACTIVE, COMPLETED, DISMISSED
    created_at: datetime

    class Config:
        from_attributes = True

class LearningPlanItemOut(BaseModel):
    id: int
    resource_type: str
    resource_id: int
    title: str
    description: Optional[str] = None
    order_index: int
    completed: bool

class LearningPlanOut(BaseModel):
    id: int
    title: str
    generated_at: datetime
    active: bool
    items: List[LearningPlanItemOut] = []

    class Config:
        from_attributes = True
