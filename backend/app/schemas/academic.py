from pydantic import BaseModel, ConfigDict, Field
from typing import Optional, List, Any
from datetime import datetime

# STUDY RESOURCE SCHEMAS
class StudyResourceBase(BaseModel):
    title: str = Field(..., min_length=2, max_length=200)
    description: Optional[str] = None
    url: str = Field(..., min_length=5, max_length=500)
    resource_type: str = "DOCUMENTATION"  # DOCUMENTATION, ARTICLE, VIDEO, TUTORIAL, CHEATSHEET, PRACTICE
    provider: str = "EXTERNAL"  # MDN, W3Schools, Python Docs, etc.
    display_order: int = 0
    is_active: bool = True

class StudyResourceCreate(StudyResourceBase):
    lesson_id: Optional[int] = None
    topic_id: Optional[int] = None

class StudyResourceUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    url: Optional[str] = None
    resource_type: Optional[str] = None
    provider: Optional[str] = None
    display_order: Optional[int] = None
    is_active: Optional[bool] = None
    topic_id: Optional[int] = None

class StudyResourceOut(StudyResourceBase):
    id: int
    lesson_id: int
    topic_id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)

# TOPIC SCHEMAS
class TopicBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    description: Optional[str] = None
    difficulty_level: str = "MEDIUM"
    display_order: int = 0
    is_active: bool = True

class TopicCreate(TopicBase):
    subject_id: Optional[int] = None
    lesson_id: Optional[int] = None

class TopicUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    difficulty_level: Optional[str] = None
    lesson_id: Optional[int] = None
    display_order: Optional[int] = None
    is_active: Optional[bool] = None

class TopicOut(TopicBase):
    id: int
    subject_id: int
    lesson_id: Optional[int] = None
    study_resources: List[StudyResourceOut] = []
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)

# LESSON SCHEMAS
class LessonBase(BaseModel):
    title: str = Field(..., min_length=2, max_length=150)
    short_description: Optional[str] = None
    detailed_description: Optional[str] = None
    description: Optional[str] = None
    content: Optional[str] = None
    resource_url: Optional[str] = None
    difficulty: str = "MEDIUM"
    difficulty_level: str = "MEDIUM"
    estimated_minutes: int = 15
    estimated_duration: int = 15
    lesson_order: int = 0
    display_order: int = 0
    is_active: bool = True

class LessonCreate(LessonBase):
    subject_id: Optional[int] = None
    topic_id: Optional[int] = None


class LessonUpdate(BaseModel):
    title: Optional[str] = None
    short_description: Optional[str] = None
    detailed_description: Optional[str] = None
    description: Optional[str] = None
    content: Optional[str] = None
    resource_url: Optional[str] = None
    difficulty: Optional[str] = None
    difficulty_level: Optional[str] = None
    estimated_minutes: Optional[int] = None
    estimated_duration: Optional[int] = None
    lesson_order: Optional[int] = None
    display_order: Optional[int] = None
    is_active: Optional[bool] = None
    topic_id: Optional[int] = None

class LessonOut(LessonBase):
    id: int
    subject_id: int
    topic_id: Optional[int] = None
    topic_name: Optional[str] = None
    subject_name: Optional[str] = None
    status: Optional[str] = "NOT_STARTED"
    completion_percentage: Optional[float] = 0.0
    topics_completed: Optional[int] = 0
    puzzles_completed: Optional[int] = 0
    quiz_completed: Optional[bool] = False
    xp_earned: Optional[int] = 0
    topics: List[TopicOut] = []
    study_resources: List[StudyResourceOut] = []
    puzzles: List[Any] = []
    quizzes: List[Any] = []
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)

class LessonProgressUpdate(BaseModel):
    status: Optional[str] = "IN_PROGRESS"
    completion_percentage: Optional[float] = None
    action_type: Optional[str] = None  # TOPIC_READ, PUZZLE_SOLVED, QUIZ_PASSED, MANUAL_COMPLETE
    topic_id: Optional[int] = None
    puzzle_id: Optional[int] = None
    quiz_id: Optional[int] = None
    quiz_score: Optional[float] = None

# SUBJECT SCHEMAS
class SubjectBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    code: str = Field(..., min_length=2, max_length=20)
    description: Optional[str] = None
    category: Optional[str] = "COMPUTER_SCIENCE"
    difficulty_level: Optional[str] = "BEGINNER"
    thumbnail_url: Optional[str] = None
    display_order: int = 0
    is_active: bool = True

class SubjectCreate(SubjectBase):
    pass

class SubjectUpdate(BaseModel):
    name: Optional[str] = None
    code: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    difficulty_level: Optional[str] = None
    thumbnail_url: Optional[str] = None
    display_order: Optional[int] = None
    is_active: Optional[bool] = None

class SubjectOut(SubjectBase):
    id: int
    topics: List[TopicOut] = []
    lessons: List[LessonOut] = []
    lessons_count: Optional[int] = 0
    quizzes_count: Optional[int] = 0
    progress_percentage: Optional[float] = 0.0
    completed_lessons_count: Optional[int] = 0
    current_lesson: Optional[Any] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)

# UTILITY REORDER SCHEMAS
class ReorderItem(BaseModel):
    id: int
    order: int

class ReorderRequest(BaseModel):
    items: List[ReorderItem]

class StatusToggleRequest(BaseModel):
    is_active: bool

# YOUTUBE RECOMMENDATION SCHEMAS
class YouTubeVideoOut(BaseModel):
    video_id: str
    title: str
    thumbnail_url: str
    channel_name: str
    duration: Optional[str] = None
    description: Optional[str] = None
    url: str
    published_at: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

class LessonYouTubeResponse(BaseModel):
    lesson_id: int
    lesson_title: Optional[str] = None
    query_used: Optional[str] = None
    videos: List[YouTubeVideoOut] = []
