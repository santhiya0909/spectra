from pydantic import BaseModel, ConfigDict, Field
from typing import Optional, List
from datetime import datetime

class AIChatRequest(BaseModel):
    message: str = Field(..., min_length=1)
    conversation_id: Optional[int] = None
    subject_id: Optional[int] = None
    topic_id: Optional[int] = None
    lesson_id: Optional[int] = None
    puzzle_id: Optional[int] = None
    action_type: Optional[str] = None  # EXPLAIN_LESSON, HINT, EXPLAIN_PUZZLE, SIMILAR_PRACTICE, EXPLAIN_QUIZ
    is_during_quiz: bool = False  # If True, tutor acts as Socratic guide without revealing direct answers

class AIMessageOut(BaseModel):
    id: int
    role: str
    content: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class AIConversationOut(BaseModel):
    id: int
    title: str
    created_at: datetime
    messages: List[AIMessageOut] = []

    model_config = ConfigDict(from_attributes=True)

class AIChatResponse(BaseModel):
    reply: str
    conversation_id: int
    hints: List[str] = []
    recommended_topics: List[str] = []
