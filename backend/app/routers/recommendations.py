from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.core.dependencies import get_current_student
from app.db.models.user import StudentProfile
from app.db.models.academic import Topic
from app.db.models.recommendation import Recommendation
from app.schemas.recommendation import RecommendationOut
from app.services.recommendation_service import generate_recommendations_for_student

router = APIRouter(prefix="/recommendations", tags=["Recommendations"])

@router.get("", response_model=List[RecommendationOut])
def list_recommendations(
    student: StudentProfile = Depends(get_current_student),
    db: Session = Depends(get_db)
):
    """Retrieve all active recommendations for the authenticated student."""
    recs = (
        db.query(Recommendation)
        .filter(Recommendation.student_id == student.id, Recommendation.status == "ACTIVE")
        .order_by(Recommendation.priority.desc(), Recommendation.created_at.desc())
        .all()
    )
    outs = []
    for r in recs:
        t = db.query(Topic).filter(Topic.id == r.topic_id).first()
        subj = t.subject if t else None
        outs.append(
            RecommendationOut(
                id=r.id,
                topic_id=r.topic_id,
                topic_name=t.name if t else "Topic",
                subject_name=subj.name if subj else "General",
                recommendation_type=r.recommendation_type,
                title=r.title,
                reason=r.reason,
                priority=r.priority,
                resource_id=r.resource_id,
                status=r.status,
                created_at=r.created_at
            )
        )
    return outs

@router.post("/{id}/complete")
def complete_recommendation(
    id: int,
    student: StudentProfile = Depends(get_current_student),
    db: Session = Depends(get_db)
):
    """Mark a recommendation as completed after student practices or reviews."""
    rec = db.query(Recommendation).filter(
        Recommendation.id == id,
        Recommendation.student_id == student.id
    ).first()
    if not rec:
        raise HTTPException(status_code=404, detail="Recommendation not found")

    rec.status = "COMPLETED"
    db.commit()
    return {"message": "Recommendation marked as completed", "id": id, "status": "COMPLETED"}

@router.post("/generate", response_model=List[RecommendationOut])
def trigger_recommendation_generation(
    student: StudentProfile = Depends(get_current_student),
    db: Session = Depends(get_db)
):
    """Re-run the recommendation engine on demand for the current student."""
    new_recs = generate_recommendations_for_student(db, student.id)
    outs = []
    for r in new_recs:
        t = db.query(Topic).filter(Topic.id == r.topic_id).first()
        subj = t.subject if t else None
        outs.append(
            RecommendationOut(
                id=r.id,
                topic_id=r.topic_id,
                topic_name=t.name if t else "Topic",
                subject_name=subj.name if subj else "General",
                recommendation_type=r.recommendation_type,
                title=r.title,
                reason=r.reason,
                priority=r.priority,
                resource_id=r.resource_id,
                status=r.status,
                created_at=r.created_at
            )
        )
    return outs
