from typing import List, Optional
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.db.database import get_db
from app.db.models.academic import Lesson, LessonProgress, Subject, Topic, StudyResource
from app.schemas.academic import LessonOut, LessonProgressUpdate, TopicOut, StudyResourceOut
from app.core.dependencies import get_current_user, get_current_student
from app.db.models.user import User, StudentProfile

router = APIRouter(prefix="/lessons", tags=["Lessons"])


@router.get("", response_model=List[LessonOut])
def get_lessons(
    subject_id: Optional[int] = Query(None),
    topic_id: Optional[int] = Query(None),
    search: Optional[str] = Query(None),
    difficulty: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user),
):
    """List lessons optionally filtered by subject or topic, with student completion status."""
    query = db.query(Lesson)

    if not current_user or current_user.role == "STUDENT":
        query = query.filter(Lesson.is_active == True)

    if subject_id:
        query = query.filter(Lesson.subject_id == subject_id)
    if topic_id:
        query = query.filter(or_(Lesson.topic_id == topic_id, Lesson.topics.any(Topic.id == topic_id)))
    if difficulty:
        query = query.filter(Lesson.difficulty_level == difficulty)
    if search:
        search_filter = f"%{search}%"
        query = query.filter(
            or_(
                Lesson.title.ilike(search_filter),
                Lesson.short_description.ilike(search_filter),
                Lesson.detailed_description.ilike(search_filter),
            )
        )

    lessons = query.order_by(Lesson.lesson_order.asc(), Lesson.id.asc()).all()

    student = None
    if current_user and current_user.role == "STUDENT":
        student = db.query(StudentProfile).filter(StudentProfile.user_id == current_user.id).first()

    results = []
    for l in lessons:
        status = "NOT_STARTED"
        pct = 0.0
        if student:
            prog = db.query(LessonProgress).filter(
                LessonProgress.student_id == student.id,
                LessonProgress.lesson_id == l.id,
            ).first()
            if prog:
                status = prog.status
                pct = prog.completion_percentage

        top = db.query(Topic).filter(Topic.id == l.topic_id).first()
        subj = db.query(Subject).filter(Subject.id == l.subject_id).first()

        # Child topics
        child_topics = db.query(Topic).filter(Topic.lesson_id == l.id)
        if not current_user or current_user.role == "STUDENT":
            child_topics = child_topics.filter(Topic.is_active == True)
        child_topics = child_topics.order_by(Topic.display_order.asc()).all()

        # Child study resources
        child_resources = db.query(StudyResource).filter(StudyResource.lesson_id == l.id)
        if not current_user or current_user.role == "STUDENT":
            child_resources = child_resources.filter(StudyResource.is_active == True)
        child_resources = child_resources.order_by(StudyResource.display_order.asc()).all()

        results.append(
            LessonOut(
                id=l.id,
                subject_id=l.subject_id,
                topic_id=l.topic_id,
                topic_name=top.name if top else None,
                subject_name=subj.name if subj else None,
                title=l.title,
                short_description=l.short_description,
                detailed_description=l.detailed_description,
                description=l.description,
                content=l.content,
                resource_url=l.resource_url,
                difficulty=l.difficulty or "MEDIUM",
                difficulty_level=l.difficulty_level or "MEDIUM",
                estimated_minutes=l.estimated_minutes or 15,
                estimated_duration=l.estimated_duration or 15,
                lesson_order=l.lesson_order,
                display_order=l.display_order,
                is_active=l.is_active,
                status=status,
                completion_percentage=pct,
                topics=[TopicOut.model_validate(t) for t in child_topics],
                study_resources=[StudyResourceOut.model_validate(r) for r in child_resources],
                created_at=l.created_at,
                updated_at=l.updated_at,
            )
        )
    return results


@router.get("/{lesson_id}", response_model=LessonOut)
def get_lesson(
    lesson_id: int,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user),
):
    """Retrieve deep details, structured topics, verified external resources, and content for a single lesson."""
    l = db.query(Lesson).filter(Lesson.id == lesson_id).first()
    if not l:
        raise HTTPException(status_code=404, detail="Lesson not found")

    if (not current_user or current_user.role == "STUDENT") and not l.is_active:
        raise HTTPException(status_code=404, detail="Lesson is currently unavailable")

    status = "NOT_STARTED"
    pct = 0.0
    if current_user and current_user.role == "STUDENT":
        student = db.query(StudentProfile).filter(StudentProfile.user_id == current_user.id).first()
        if student:
            prog = db.query(LessonProgress).filter(
                LessonProgress.student_id == student.id,
                LessonProgress.lesson_id == l.id,
            ).first()
            if prog:
                status = prog.status
                pct = prog.completion_percentage

    top = db.query(Topic).filter(Topic.id == l.topic_id).first()
    subj = db.query(Subject).filter(Subject.id == l.subject_id).first()

    # Child topics
    child_topics = db.query(Topic).filter(Topic.lesson_id == l.id)
    if not current_user or current_user.role == "STUDENT":
        child_topics = child_topics.filter(Topic.is_active == True)
    child_topics = child_topics.order_by(Topic.display_order.asc()).all()

    # Child study resources
    child_resources = db.query(StudyResource).filter(StudyResource.lesson_id == l.id)
    if not current_user or current_user.role == "STUDENT":
        child_resources = child_resources.filter(StudyResource.is_active == True)
    child_resources = child_resources.order_by(StudyResource.display_order.asc()).all()

    return LessonOut(
        id=l.id,
        subject_id=l.subject_id,
        topic_id=l.topic_id,
        topic_name=top.name if top else None,
        subject_name=subj.name if subj else None,
        title=l.title,
        short_description=l.short_description,
        detailed_description=l.detailed_description,
        description=l.description,
        content=l.content,
        resource_url=l.resource_url,
        difficulty=l.difficulty or "MEDIUM",
        difficulty_level=l.difficulty_level or "MEDIUM",
        estimated_minutes=l.estimated_minutes or 15,
        estimated_duration=l.estimated_duration or 15,
        lesson_order=l.lesson_order,
        display_order=l.display_order,
        is_active=l.is_active,
        status=status,
        completion_percentage=pct,
        topics=[TopicOut.model_validate(t) for t in child_topics],
        study_resources=[StudyResourceOut.model_validate(r) for r in child_resources],
        created_at=l.created_at,
        updated_at=l.updated_at,
    )


@router.post("/{lesson_id}/progress")
def update_lesson_progress(
    lesson_id: int,
    progress_in: LessonProgressUpdate,
    student: StudentProfile = Depends(get_current_student),
    db: Session = Depends(get_db),
):
    """Update student progress for a lesson (e.g. IN_PROGRESS or COMPLETED)."""
    lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")

    prog = db.query(LessonProgress).filter(
        LessonProgress.student_id == student.id,
        LessonProgress.lesson_id == lesson_id,
    ).first()

    now = datetime.now(timezone.utc)
    if not prog:
        prog = LessonProgress(
            student_id=student.id,
            lesson_id=lesson_id,
            status=progress_in.status,
            completion_percentage=progress_in.completion_percentage,
            completed_at=now if progress_in.status == "COMPLETED" else None,
        )
        db.add(prog)
    else:
        prog.status = progress_in.status
        prog.completion_percentage = max(prog.completion_percentage, progress_in.completion_percentage)
        if progress_in.status == "COMPLETED" and not prog.completed_at:
            prog.completed_at = now

    db.commit()
    db.refresh(prog)
    return {
        "message": "Progress recorded successfully",
        "status": prog.status,
        "completion_percentage": prog.completion_percentage,
    }
