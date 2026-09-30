from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from app.schemas.academic import YouTubeVideoOut


class KnowledgeDNANode(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    lesson_id: Optional[int] = None
    lesson_title: Optional[str] = None
    lesson_order: int = 1
    display_order: int = 1
    difficulty_level: str = "MEDIUM"
    mastery_score: float = 0.0
    mastery_state: str = "NOT_STARTED"  # MASTERED, DEVELOPING, WEAK, NOT_STARTED, LOCKED
    recent_quiz_score: Optional[float] = None
    attempts_count: int = 0
    correct_answers: int = 0
    total_questions: int = 0
    lesson_completed: bool = False
    prerequisite_gap: bool = False
    prerequisite_names: List[str] = []
    prerequisite_ids: List[int] = []
    dependent_names: List[str] = []
    why_weak_explanation: Optional[str] = None
    recommended_action: Optional[str] = None


class KnowledgeDNAEdge(BaseModel):
    source: int
    target: int
    source_name: str
    target_name: str
    status: str = "SATISFIED"  # SATISFIED, GAP, LOCKED


class KnowledgeDNAFocusRecommendation(BaseModel):
    topic_id: int
    topic_name: str
    lesson_id: Optional[int] = None
    lesson_title: Optional[str] = None
    mastery_score: float = 0.0
    mastery_state: str = "WEAK"
    reason: str
    prerequisite_impact: Optional[str] = None
    action_plan: List[str] = []


class KnowledgeDNASummary(BaseModel):
    subject_id: int
    subject_name: str
    subject_code: str
    overall_mastery: float = 0.0
    mastered_count: int = 0
    developing_count: int = 0
    weak_count: int = 0
    not_started_count: int = 0
    locked_count: int = 0
    total_topics: int = 0
    recommended_focus: Optional[KnowledgeDNAFocusRecommendation] = None


class KnowledgeDNAResponse(BaseModel):
    subject_id: int
    subject_name: str
    subject_code: str
    overall_mastery: float = 0.0
    mastered_count: int = 0
    developing_count: int = 0
    weak_count: int = 0
    not_started_count: int = 0
    locked_count: int = 0
    total_topics: int = 0
    recommended_focus: Optional[KnowledgeDNAFocusRecommendation] = None
    nodes: List[KnowledgeDNANode] = []
    edges: List[KnowledgeDNAEdge] = []
    strong_areas: List[KnowledgeDNANode] = []
    developing_areas: List[KnowledgeDNANode] = []
    weak_areas: List[KnowledgeDNANode] = []
    not_started_areas: List[KnowledgeDNANode] = []


class TopicKnowledgeDNADetail(BaseModel):
    node: KnowledgeDNANode
    prerequisites: List[Dict[str, Any]] = []
    dependents: List[Dict[str, Any]] = []
    recent_attempts: List[Dict[str, Any]] = []
    puzzle_attempts: List[Dict[str, Any]] = []
    puzzle_accuracy: Optional[float] = None
    puzzle_solved_count: int = 0
    puzzle_total_count: int = 0
    youtube_videos: List[YouTubeVideoOut] = []
