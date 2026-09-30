from pydantic import BaseModel, ConfigDict, Field
from typing import Optional, List, Any, Dict, Union
from datetime import datetime

class PuzzleBase(BaseModel):
    subject_id: int
    lesson_id: int
    topic_id: Optional[int] = None
    title: str
    description: Optional[str] = None
    puzzle_type: str  # MULTIPLE_CHOICE, FILL_BLANK, CODE_OUTPUT, ORDERING, MATCHING, TRUE_FALSE
    question: str
    puzzle_data: Union[Dict[str, Any], List[Any], str]
    correct_answer: Union[Dict[str, Any], List[Any], str]
    explanation: Optional[str] = None
    difficulty: str = "MEDIUM"
    xp_reward: int = 10
    display_order: int = 0
    is_active: bool = True

class PuzzleCreate(PuzzleBase):
    pass

class PuzzleUpdate(BaseModel):
    subject_id: Optional[int] = None
    lesson_id: Optional[int] = None
    topic_id: Optional[int] = None
    title: Optional[str] = None
    description: Optional[str] = None
    puzzle_type: Optional[str] = None
    question: Optional[str] = None
    puzzle_data: Optional[Union[Dict[str, Any], List[Any], str]] = None
    correct_answer: Optional[Union[Dict[str, Any], List[Any], str]] = None
    explanation: Optional[str] = None
    difficulty: Optional[str] = None
    xp_reward: Optional[int] = None
    display_order: Optional[int] = None
    is_active: Optional[bool] = None

class PuzzleOut(BaseModel):
    id: int
    subject_id: int
    lesson_id: int
    topic_id: Optional[int] = None
    title: str
    description: Optional[str] = None
    puzzle_type: str
    question: str
    puzzle_data: Union[Dict[str, Any], List[Any], str]
    difficulty: str
    xp_reward: int
    display_order: int
    is_active: bool
    user_solved: bool = False
    user_attempts: int = 0
    topic_name: Optional[str] = None
    lesson_title: Optional[str] = None
    subject_name: Optional[str] = None
    estimated_time: Optional[str] = "3 min"
    instructions: Optional[str] = None
    puzzle_index: Optional[int] = 1
    total_in_lesson: Optional[int] = 1
    # Note: correct_answer is strictly EXCLUDED to prevent leakage to students

    model_config = ConfigDict(from_attributes=True)

class PuzzleAdminOut(BaseModel):
    id: int
    subject_id: int
    lesson_id: int
    topic_id: Optional[int] = None
    title: str
    description: Optional[str] = None
    puzzle_type: str
    question: str
    puzzle_data: Union[Dict[str, Any], List[Any], str]
    correct_answer: Union[Dict[str, Any], List[Any], str]
    explanation: Optional[str] = None
    difficulty: str
    xp_reward: int
    display_order: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

class PuzzleSubmission(BaseModel):
    submitted_answer: Union[Dict[str, Any], List[Any], str, bool, int]
    time_taken: int = 0

class PuzzleSubmissionResult(BaseModel):
    is_correct: bool
    xp_earned: int
    explanation: Optional[str] = None
    hint: Optional[str] = None
    attempts_count: int
    lesson_progress_percentage: float
    lesson_completed: bool
    topic_id: Optional[int] = None
    topic_name: Optional[str] = None
    mastery_before: Optional[float] = None
    mastery_after: Optional[float] = None
    mastery_state_before: Optional[str] = None
    mastery_state_after: Optional[str] = None
    spectra_feedback: Optional[str] = None
    recommended_action: Optional[str] = None
    recommended_video: Optional[Dict[str, Any]] = None
    next_puzzle_id: Optional[int] = None
    next_lesson_id: Optional[int] = None

class PuzzleAttemptSummary(BaseModel):
    puzzle_id: int
    puzzle_title: str
    is_correct: bool
    attempts_count: int
    xp_earned: int
    completed_at: datetime

class StudentPuzzleProgressOut(BaseModel):
    total_solved: int
    total_puzzles: int
    total_xp: int
    accuracy: float = 0.0
    topics_strengthened: int = 0
    total_attempts: int = 0
    recent_attempts: List[PuzzleAttemptSummary] = []

