from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserRegister(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(..., min_length=6)
    role: str = Field(default="STUDENT", pattern="^(STUDENT|TEACHER|ADMIN)$")
    department: Optional[str] = "Computer Science"
    semester: Optional[int] = 4
    student_id: Optional[str] = None
    employee_id: Optional[str] = None

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    role: str
    user_id: int
    name: str
    email: str

class StudentProfileOut(BaseModel):
    id: int
    student_id: str
    department: str
    semester: int
    academic_year: str
    learning_preferences: Optional[str] = None

    class Config:
        from_attributes = True

class TeacherProfileOut(BaseModel):
    id: int
    employee_id: str
    department: str

    class Config:
        from_attributes = True

class UserOut(BaseModel):
    id: int
    name: str
    email: str
    role: str
    created_at: datetime
    student_profile: Optional[StudentProfileOut] = None
    teacher_profile: Optional[TeacherProfileOut] = None

    class Config:
        from_attributes = True
