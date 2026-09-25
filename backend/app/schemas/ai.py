from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class AIChatRequest(BaseModel):
    message: str = Field(..., min_length=1)
    conversation_id: Optional[int] = None
    subject_id: Optional[int] = None
    topic_id: Optional[int] = None
    is_during_quiz: bool = False  # If True, tutor acts as Socratic guide without revealing direct answers

class AIMessageOut(BaseModel):
    id: int
    role: str
    content: str
    created_at: datetime

    class Config:
        from_attributes = True

class AIConversationOut(BaseModel):
    id: int
    title: str
    created_at: datetime
    messages: List[AIMessageOut] = []

    class Config:
        from_attributes = True

class AIChatResponse(BaseModel):
    reply: str
    conversation_id: int
    hints: List[str] = []
    recommended_topics: List[str] = []
