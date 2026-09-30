from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from datetime import datetime
from app.schemas.auth import UserOut

class UserUpdateRole(BaseModel):
    role: str

class AuditLogOut(BaseModel):
    id: int
    user_id: Optional[int]
    user_name: Optional[str]
    action: str
    entity: str
    entity_id: Optional[str]
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class AdminDashboardOut(BaseModel):
    total_users: int
    total_students: int
    total_teachers: int
    total_subjects: int
    total_quizzes: int
    total_questions: int
    recent_logs: List[AuditLogOut]
