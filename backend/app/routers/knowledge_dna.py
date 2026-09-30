from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.core.dependencies import get_current_student
from app.db.models.user import StudentProfile
from app.schemas.knowledge_dna import (
    KnowledgeDNAResponse,
    KnowledgeDNASummary,
    TopicKnowledgeDNADetail
)
from app.services.knowledge_dna_service import (
    get_knowledge_dna_for_student,
    get_knowledge_dna_summary,
    get_topic_knowledge_dna_detail
)

router = APIRouter(prefix="/knowledge-dna", tags=["Knowledge DNA"])


@router.get("", response_model=KnowledgeDNAResponse)
def get_knowledge_dna_endpoint(
    subject_id: Optional[int] = Query(None, description="Optional subject ID to filter graph"),
    student: StudentProfile = Depends(get_current_student),
    db: Session = Depends(get_db)
):
    """
    Retrieve the student's complete Knowledge DNA graph for the active or requested subject.
    Computes mastery from quiz performance and lesson progress, detects prerequisite gaps,
    and returns connected nodes, edges, and AI focus recommendations.
    """
    return get_knowledge_dna_for_student(db, student.id, subject_id)


@router.get("/summary", response_model=KnowledgeDNASummary)
def get_knowledge_dna_summary_endpoint(
    subject_id: Optional[int] = Query(None, description="Optional subject ID"),
    student: StudentProfile = Depends(get_current_student),
    db: Session = Depends(get_db)
):
    """
    Lightweight summary for compact dashboard cards:
    Overall mastery score, count breakdown (Mastered/Developing/Weak), and recommended focus.
    """
    return get_knowledge_dna_summary(db, student.id, subject_id)


@router.get("/topics/{topic_id}", response_model=TopicKnowledgeDNADetail)
def get_topic_dna_detail_endpoint(
    topic_id: int,
    student: StudentProfile = Depends(get_current_student),
    db: Session = Depends(get_db)
):
    """
    Detailed topic drill-down view:
    Learning evidence, why-weak explanation, prerequisite statuses, and curated YouTube recommendations.
    """
    try:
        return get_topic_knowledge_dna_detail(db, student.id, topic_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
