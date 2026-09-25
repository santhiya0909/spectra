import json
from typing import List, Optional
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.db.database import get_db
from app.core.dependencies import require_role
from app.db.models.user import User, AuditLog
from app.db.models.academic import Subject, Topic, Lesson, StudyResource
from app.db.models.quiz import Question, Quiz, QuizQuestion
from app.schemas.admin import AdminDashboardOut, UserUpdateRole
from app.schemas.auth import UserOut
from app.schemas.academic import (
    SubjectCreate,
    SubjectUpdate,
    SubjectOut,
    LessonCreate,
    LessonUpdate,
    LessonOut,
    TopicCreate,
    TopicUpdate,
    TopicOut,
    StudyResourceCreate,
    StudyResourceUpdate,
    StudyResourceOut,
    ReorderRequest,
    StatusToggleRequest,
)
from app.schemas.quiz import QuestionCreate, QuestionOut, QuizCreate, QuizOut
from app.services.admin_service import get_admin_dashboard_stats

router = APIRouter(prefix="/admin", tags=["Admin"])


@router.get("/dashboard", response_model=AdminDashboardOut)
def read_admin_dashboard(
    current_user: User = Depends(require_role(["ADMIN"])),
    db: Session = Depends(get_db),
):
    """Retrieve full platform administrator dashboard metrics and recent audit logs."""
    return get_admin_dashboard_stats(db)


# ============================================================
# USER MANAGEMENT
# ============================================================

@router.get("/users", response_model=List[UserOut])
def list_users(
    current_user: User = Depends(require_role(["ADMIN"])),
    db: Session = Depends(get_db),
):
    """List all registered platform users."""
    users = db.query(User).all()
    return users


@router.patch("/users/{id}/role", response_model=UserOut)
def update_user_role(
    id: int,
    role_in: UserUpdateRole,
    current_user: User = Depends(require_role(["ADMIN"])),
    db: Session = Depends(get_db),
):
    """Change user role (STUDENT, TEACHER, ADMIN)."""
    user = db.query(User).filter(User.id == id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.role = role_in.role
    db.add(AuditLog(user_id=current_user.id, action=f"UPDATED_ROLE_TO_{role_in.role}", entity="USER", entity_id=str(id)))
    db.commit()
    db.refresh(user)
    return user


# ============================================================
# SUBJECT MANAGEMENT (CRUD + Reorder + Status Toggle)
# ============================================================

@router.get("/subjects", response_model=List[SubjectOut])
def admin_get_subjects(
    search: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    difficulty: Optional[str] = Query(None),
    is_active: Optional[bool] = Query(None),
    current_user: User = Depends(require_role(["ADMIN"])),
    db: Session = Depends(get_db),
):
    """List subjects with filtering and curriculum metadata."""
    query = db.query(Subject)

    if search:
        search_filter = f"%{search}%"
        query = query.filter(
            or_(
                Subject.name.ilike(search_filter),
                Subject.code.ilike(search_filter),
                Subject.description.ilike(search_filter),
            )
        )

    if category:
        query = query.filter(Subject.category == category)

    if difficulty:
        query = query.filter(Subject.difficulty_level == difficulty)

    if is_active is not None:
        query = query.filter(Subject.is_active == is_active)

    subjects = query.order_by(Subject.display_order.asc(), Subject.id.asc()).all()

    results = []
    for s in subjects:
        lessons = db.query(Lesson).filter(Lesson.subject_id == s.id).order_by(Lesson.lesson_order.asc()).all()
        topics = db.query(Topic).filter(Topic.subject_id == s.id).order_by(Topic.display_order.asc()).all()
        quizzes = db.query(Quiz).filter(Quiz.subject_id == s.id).all()

        results.append(
            SubjectOut(
                id=s.id,
                name=s.name,
                code=s.code,
                description=s.description,
                category=s.category or "COMPUTER_SCIENCE",
                difficulty_level=s.difficulty_level or "BEGINNER",
                thumbnail_url=s.thumbnail_url,
                display_order=s.display_order,
                is_active=s.is_active,
                created_at=s.created_at,
                updated_at=s.updated_at,
                topics=[TopicOut.model_validate(t) for t in topics],
                lessons_count=len(lessons),
                quizzes_count=len(quizzes),
                progress_percentage=0.0,
            )
        )
    return results


@router.post("/subjects", response_model=SubjectOut, status_code=status.HTTP_201_CREATED)
def admin_create_subject(
    subject_in: SubjectCreate,
    current_user: User = Depends(require_role(["ADMIN"])),
    db: Session = Depends(get_db),
):
    """Create a new curriculum subject."""
    existing = db.query(Subject).filter((Subject.code == subject_in.code) | (Subject.name == subject_in.name)).first()
    if existing:
        raise HTTPException(status_code=400, detail="Subject with this code or name already exists.")

    subject = Subject(
        name=subject_in.name,
        code=subject_in.code,
        description=subject_in.description,
        category=subject_in.category or "COMPUTER_SCIENCE",
        difficulty_level=subject_in.difficulty_level or "BEGINNER",
        thumbnail_url=subject_in.thumbnail_url,
        display_order=subject_in.display_order,
        is_active=subject_in.is_active,
    )
    db.add(subject)
    db.flush()
    db.add(AuditLog(user_id=current_user.id, action="CREATE_SUBJECT", entity="SUBJECT", entity_id=str(subject.id)))
    db.commit()
    db.refresh(subject)

    return SubjectOut(
        id=subject.id,
        name=subject.name,
        code=subject.code,
        description=subject.description,
        category=subject.category,
        difficulty_level=subject.difficulty_level,
        thumbnail_url=subject.thumbnail_url,
        display_order=subject.display_order,
        is_active=subject.is_active,
        created_at=subject.created_at,
        updated_at=subject.updated_at,
        topics=[],
        lessons=[],
        lessons_count=0,
        quizzes_count=0,
        progress_percentage=0.0,
    )


@router.get("/subjects/{id}", response_model=SubjectOut)
def admin_get_subject_detail(
    id: int,
    current_user: User = Depends(require_role(["ADMIN"])),
    db: Session = Depends(get_db),
):
    """Get full details of a subject including all lessons, topics, and resources."""
    subject = db.query(Subject).filter(Subject.id == id).first()
    if not subject:
        raise HTTPException(status_code=404, detail="Subject not found")

    lessons = db.query(Lesson).filter(Lesson.subject_id == id).order_by(Lesson.lesson_order.asc()).all()
    topics = db.query(Topic).filter(Topic.subject_id == id).order_by(Topic.display_order.asc()).all()
    quizzes = db.query(Quiz).filter(Quiz.subject_id == id).all()

    lesson_outs = []
    for l in lessons:
        l_topics = db.query(Topic).filter(Topic.lesson_id == l.id).order_by(Topic.display_order.asc()).all()
        l_resources = db.query(StudyResource).filter(StudyResource.lesson_id == l.id).order_by(StudyResource.display_order.asc()).all()
        lesson_outs.append(
            LessonOut(
                id=l.id,
                subject_id=l.subject_id,
                topic_id=l.topic_id,
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
                topics=[TopicOut.model_validate(t) for t in l_topics],
                study_resources=[StudyResourceOut.model_validate(r) for r in l_resources],
                created_at=l.created_at,
                updated_at=l.updated_at,
            )
        )

    return SubjectOut(
        id=subject.id,
        name=subject.name,
        code=subject.code,
        description=subject.description,
        category=subject.category or "COMPUTER_SCIENCE",
        difficulty_level=subject.difficulty_level or "BEGINNER",
        thumbnail_url=subject.thumbnail_url,
        display_order=subject.display_order,
        is_active=subject.is_active,
        created_at=subject.created_at,
        updated_at=subject.updated_at,
        topics=[TopicOut.model_validate(t) for t in topics],
        lessons=lesson_outs,
        lessons_count=len(lessons),
        quizzes_count=len(quizzes),
        progress_percentage=0.0,
    )


@router.patch("/subjects/{id}", response_model=SubjectOut)
def admin_update_subject(
    id: int,
    subject_in: SubjectUpdate,
    current_user: User = Depends(require_role(["ADMIN"])),
    db: Session = Depends(get_db),
):
    """Update subject details."""
    subject = db.query(Subject).filter(Subject.id == id).first()
    if not subject:
        raise HTTPException(status_code=404, detail="Subject not found")

    if subject_in.name is not None:
        subject.name = subject_in.name
    if subject_in.code is not None:
        subject.code = subject_in.code
    if subject_in.description is not None:
        subject.description = subject_in.description
    if subject_in.category is not None:
        subject.category = subject_in.category
    if subject_in.difficulty_level is not None:
        subject.difficulty_level = subject_in.difficulty_level
    if subject_in.thumbnail_url is not None:
        subject.thumbnail_url = subject_in.thumbnail_url
    if subject_in.display_order is not None:
        subject.display_order = subject_in.display_order
    if subject_in.is_active is not None:
        subject.is_active = subject_in.is_active

    subject.updated_at = datetime.now(timezone.utc)
    db.add(AuditLog(user_id=current_user.id, action="UPDATE_SUBJECT", entity="SUBJECT", entity_id=str(id)))
    db.commit()
    db.refresh(subject)
    return subject


@router.patch("/subjects/{id}/status")
def admin_toggle_subject_status(
    id: int,
    req: StatusToggleRequest,
    current_user: User = Depends(require_role(["ADMIN"])),
    db: Session = Depends(get_db),
):
    """Toggle subject active/inactive status."""
    subject = db.query(Subject).filter(Subject.id == id).first()
    if not subject:
        raise HTTPException(status_code=404, detail="Subject not found")

    subject.is_active = req.is_active
    subject.updated_at = datetime.now(timezone.utc)
    action = "ACTIVATE_SUBJECT" if req.is_active else "DEACTIVATE_SUBJECT"
    db.add(AuditLog(user_id=current_user.id, action=action, entity="SUBJECT", entity_id=str(id)))
    db.commit()
    return {"message": f"Subject {'activated' if req.is_active else 'deactivated'} successfully", "id": id, "is_active": req.is_active}


@router.post("/subjects/reorder")
def admin_reorder_subjects(
    req: ReorderRequest,
    current_user: User = Depends(require_role(["ADMIN"])),
    db: Session = Depends(get_db),
):
    """Reorder subjects by display order."""
    for item in req.items:
        db.query(Subject).filter(Subject.id == item.id).update(
            {"display_order": item.order, "updated_at": datetime.now(timezone.utc)}
        )
    db.add(AuditLog(user_id=current_user.id, action="REORDER_SUBJECTS", entity="SUBJECT", entity_id="BULK"))
    db.commit()
    return {"message": "Subjects reordered successfully"}


@router.delete("/subjects/{id}")
def admin_delete_subject(
    id: int,
    current_user: User = Depends(require_role(["ADMIN"])),
    db: Session = Depends(get_db),
):
    """Delete a subject and its associated topics/lessons/quizzes."""
    subject = db.query(Subject).filter(Subject.id == id).first()
    if not subject:
        raise HTTPException(status_code=404, detail="Subject not found")

    db.delete(subject)
    db.add(AuditLog(user_id=current_user.id, action="DELETE_SUBJECT", entity="SUBJECT", entity_id=str(id)))
    db.commit()
    return {"message": "Subject deleted successfully", "id": id}


# ============================================================
# LESSON / MODULE MANAGEMENT (CRUD + Reorder + Status Toggle)
# ============================================================

@router.get("/subjects/{subject_id}/lessons", response_model=List[LessonOut])
def admin_get_subject_lessons(
    subject_id: int,
    current_user: User = Depends(require_role(["ADMIN"])),
    db: Session = Depends(get_db),
):
    """List all lessons under a subject with child topics and resources."""
    subject = db.query(Subject).filter(Subject.id == subject_id).first()
    if not subject:
        raise HTTPException(status_code=404, detail="Subject not found")

    lessons = db.query(Lesson).filter(Lesson.subject_id == subject_id).order_by(Lesson.lesson_order.asc()).all()
    results = []
    for l in lessons:
        l_topics = db.query(Topic).filter(Topic.lesson_id == l.id).order_by(Topic.display_order.asc()).all()
        l_resources = db.query(StudyResource).filter(StudyResource.lesson_id == l.id).order_by(StudyResource.display_order.asc()).all()
        results.append(
            LessonOut(
                id=l.id,
                subject_id=l.subject_id,
                topic_id=l.topic_id,
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
                topics=[TopicOut.model_validate(t) for t in l_topics],
                study_resources=[StudyResourceOut.model_validate(r) for r in l_resources],
                created_at=l.created_at,
                updated_at=l.updated_at,
            )
        )
    return results


@router.post("/subjects/{subject_id}/lessons", response_model=LessonOut, status_code=status.HTTP_201_CREATED)
def admin_create_lesson(
    subject_id: int,
    lesson_in: LessonCreate,
    current_user: User = Depends(require_role(["ADMIN"])),
    db: Session = Depends(get_db),
):
    """Create a new lesson under a subject."""
    subject = db.query(Subject).filter(Subject.id == subject_id).first()
    if not subject:
        raise HTTPException(status_code=404, detail="Subject not found")

    # If lesson_order is 0, auto-assign next order
    order = lesson_in.lesson_order
    if order == 0:
        max_order = db.query(Lesson.lesson_order).filter(Lesson.subject_id == subject_id).order_by(Lesson.lesson_order.desc()).first()
        order = (max_order[0] + 1) if max_order else 1

    diff = lesson_in.difficulty_level or lesson_in.difficulty or "MEDIUM"
    dur = lesson_in.estimated_duration or lesson_in.estimated_minutes or 15

    lesson = Lesson(
        subject_id=subject_id,
        topic_id=lesson_in.topic_id,
        title=lesson_in.title,
        short_description=lesson_in.short_description,
        detailed_description=lesson_in.detailed_description,
        description=lesson_in.description or lesson_in.short_description,
        content=lesson_in.content or "# " + lesson_in.title,
        resource_url=lesson_in.resource_url,
        difficulty=diff,
        difficulty_level=diff,
        estimated_minutes=dur,
        estimated_duration=dur,
        lesson_order=order,
        display_order=order,
        is_active=lesson_in.is_active,
    )
    db.add(lesson)
    db.flush()
    db.add(AuditLog(user_id=current_user.id, action="CREATE_LESSON", entity="LESSON", entity_id=str(lesson.id)))
    db.commit()
    db.refresh(lesson)

    return LessonOut(
        id=lesson.id,
        subject_id=lesson.subject_id,
        topic_id=lesson.topic_id,
        title=lesson.title,
        short_description=lesson.short_description,
        detailed_description=lesson.detailed_description,
        description=lesson.description,
        content=lesson.content,
        resource_url=lesson.resource_url,
        difficulty=lesson.difficulty,
        difficulty_level=lesson.difficulty_level,
        estimated_minutes=lesson.estimated_minutes,
        estimated_duration=lesson.estimated_duration,
        lesson_order=lesson.lesson_order,
        display_order=lesson.display_order,
        is_active=lesson.is_active,
        topics=[],
        study_resources=[],
        created_at=lesson.created_at,
        updated_at=lesson.updated_at,
    )


@router.get("/lessons/{id}", response_model=LessonOut)
def admin_get_lesson(
    id: int,
    current_user: User = Depends(require_role(["ADMIN"])),
    db: Session = Depends(get_db),
):
    """Get single lesson detail with topics and resources."""
    l = db.query(Lesson).filter(Lesson.id == id).first()
    if not l:
        raise HTTPException(status_code=404, detail="Lesson not found")

    l_topics = db.query(Topic).filter(Topic.lesson_id == l.id).order_by(Topic.display_order.asc()).all()
    l_resources = db.query(StudyResource).filter(StudyResource.lesson_id == l.id).order_by(StudyResource.display_order.asc()).all()

    return LessonOut(
        id=l.id,
        subject_id=l.subject_id,
        topic_id=l.topic_id,
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
        topics=[TopicOut.model_validate(t) for t in l_topics],
        study_resources=[StudyResourceOut.model_validate(r) for r in l_resources],
        created_at=l.created_at,
        updated_at=l.updated_at,
    )


@router.patch("/lessons/{id}", response_model=LessonOut)
def admin_update_lesson(
    id: int,
    lesson_in: LessonUpdate,
    current_user: User = Depends(require_role(["ADMIN"])),
    db: Session = Depends(get_db),
):
    """Update lesson details."""
    l = db.query(Lesson).filter(Lesson.id == id).first()
    if not l:
        raise HTTPException(status_code=404, detail="Lesson not found")

    if lesson_in.title is not None:
        l.title = lesson_in.title
    if lesson_in.short_description is not None:
        l.short_description = lesson_in.short_description
    if lesson_in.detailed_description is not None:
        l.detailed_description = lesson_in.detailed_description
    if lesson_in.description is not None:
        l.description = lesson_in.description
    if lesson_in.content is not None:
        l.content = lesson_in.content
    if lesson_in.resource_url is not None:
        l.resource_url = lesson_in.resource_url
    if lesson_in.difficulty is not None:
        l.difficulty = lesson_in.difficulty
    if lesson_in.difficulty_level is not None:
        l.difficulty_level = lesson_in.difficulty_level
    if lesson_in.estimated_minutes is not None:
        l.estimated_minutes = lesson_in.estimated_minutes
    if lesson_in.estimated_duration is not None:
        l.estimated_duration = lesson_in.estimated_duration
    if lesson_in.lesson_order is not None:
        l.lesson_order = lesson_in.lesson_order
        l.display_order = lesson_in.lesson_order
    if lesson_in.display_order is not None:
        l.display_order = lesson_in.display_order
        l.lesson_order = lesson_in.display_order
    if lesson_in.is_active is not None:
        l.is_active = lesson_in.is_active
    if lesson_in.topic_id is not None:
        l.topic_id = lesson_in.topic_id

    l.updated_at = datetime.now(timezone.utc)
    db.add(AuditLog(user_id=current_user.id, action="UPDATE_LESSON", entity="LESSON", entity_id=str(id)))
    db.commit()
    db.refresh(l)

    l_topics = db.query(Topic).filter(Topic.lesson_id == l.id).order_by(Topic.display_order.asc()).all()
    l_resources = db.query(StudyResource).filter(StudyResource.lesson_id == l.id).order_by(StudyResource.display_order.asc()).all()

    return LessonOut(
        id=l.id,
        subject_id=l.subject_id,
        topic_id=l.topic_id,
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
        topics=[TopicOut.model_validate(t) for t in l_topics],
        study_resources=[StudyResourceOut.model_validate(r) for r in l_resources],
        created_at=l.created_at,
        updated_at=l.updated_at,
    )


@router.patch("/lessons/{id}/status")
def admin_toggle_lesson_status(
    id: int,
    req: StatusToggleRequest,
    current_user: User = Depends(require_role(["ADMIN"])),
    db: Session = Depends(get_db),
):
    """Toggle lesson active/inactive status."""
    l = db.query(Lesson).filter(Lesson.id == id).first()
    if not l:
        raise HTTPException(status_code=404, detail="Lesson not found")

    l.is_active = req.is_active
    l.updated_at = datetime.now(timezone.utc)
    action = "ACTIVATE_LESSON" if req.is_active else "DEACTIVATE_LESSON"
    db.add(AuditLog(user_id=current_user.id, action=action, entity="LESSON", entity_id=str(id)))
    db.commit()
    return {"message": f"Lesson {'activated' if req.is_active else 'deactivated'} successfully", "id": id, "is_active": req.is_active}


@router.post("/lessons/reorder")
def admin_reorder_lessons(
    req: ReorderRequest,
    current_user: User = Depends(require_role(["ADMIN"])),
    db: Session = Depends(get_db),
):
    """Reorder lessons by order index."""
    for item in req.items:
        db.query(Lesson).filter(Lesson.id == item.id).update(
            {"lesson_order": item.order, "display_order": item.order, "updated_at": datetime.now(timezone.utc)}
        )
    db.add(AuditLog(user_id=current_user.id, action="REORDER_LESSONS", entity="LESSON", entity_id="BULK"))
    db.commit()
    return {"message": "Lessons reordered successfully"}


@router.delete("/lessons/{id}")
def admin_delete_lesson(
    id: int,
    current_user: User = Depends(require_role(["ADMIN"])),
    db: Session = Depends(get_db),
):
    """Delete a lesson."""
    l = db.query(Lesson).filter(Lesson.id == id).first()
    if not l:
        raise HTTPException(status_code=404, detail="Lesson not found")

    db.delete(l)
    db.add(AuditLog(user_id=current_user.id, action="DELETE_LESSON", entity="LESSON", entity_id=str(id)))
    db.commit()
    return {"message": "Lesson deleted successfully", "id": id}


# ============================================================
# TOPIC MANAGEMENT (CRUD + Reorder + Status Toggle)
# ============================================================

@router.get("/topics", response_model=List[TopicOut])
def admin_get_topics(
    subject_id: Optional[int] = Query(None),
    lesson_id: Optional[int] = Query(None),
    current_user: User = Depends(require_role(["ADMIN"])),
    db: Session = Depends(get_db),
):
    """List topics optionally filtered by subject or lesson."""
    query = db.query(Topic)
    if subject_id:
        query = query.filter(Topic.subject_id == subject_id)
    if lesson_id:
        query = query.filter(Topic.lesson_id == lesson_id)
    return query.order_by(Topic.display_order.asc(), Topic.id.asc()).all()


@router.post("/topics", response_model=TopicOut, status_code=status.HTTP_201_CREATED)
def admin_create_topic(
    topic_in: TopicCreate,
    current_user: User = Depends(require_role(["ADMIN"])),
    db: Session = Depends(get_db),
):
    """Create a new topic under a subject/lesson."""
    subject = db.query(Subject).filter(Subject.id == topic_in.subject_id).first()
    if not subject:
        raise HTTPException(status_code=404, detail="Subject not found")

    order = topic_in.display_order
    if order == 0:
        max_order = db.query(Topic.display_order).filter(Topic.subject_id == topic_in.subject_id).order_by(Topic.display_order.desc()).first()
        order = (max_order[0] + 1) if max_order else 1

    topic = Topic(
        subject_id=topic_in.subject_id,
        lesson_id=topic_in.lesson_id,
        name=topic_in.name,
        description=topic_in.description,
        difficulty_level=topic_in.difficulty_level or "MEDIUM",
        display_order=order,
        is_active=topic_in.is_active,
    )
    db.add(topic)
    db.flush()
    db.add(AuditLog(user_id=current_user.id, action="CREATE_TOPIC", entity="TOPIC", entity_id=str(topic.id)))
    db.commit()
    db.refresh(topic)
    return topic


@router.get("/topics/{id}", response_model=TopicOut)
def admin_get_topic(
    id: int,
    current_user: User = Depends(require_role(["ADMIN"])),
    db: Session = Depends(get_db),
):
    """Get single topic detail."""
    topic = db.query(Topic).filter(Topic.id == id).first()
    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")
    return topic


@router.patch("/topics/{id}", response_model=TopicOut)
def admin_update_topic(
    id: int,
    topic_in: TopicUpdate,
    current_user: User = Depends(require_role(["ADMIN"])),
    db: Session = Depends(get_db),
):
    """Update topic fields."""
    topic = db.query(Topic).filter(Topic.id == id).first()
    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")

    if topic_in.name is not None:
        topic.name = topic_in.name
    if topic_in.description is not None:
        topic.description = topic_in.description
    if topic_in.difficulty_level is not None:
        topic.difficulty_level = topic_in.difficulty_level
    if topic_in.lesson_id is not None:
        topic.lesson_id = topic_in.lesson_id
    if topic_in.display_order is not None:
        topic.display_order = topic_in.display_order
    if topic_in.is_active is not None:
        topic.is_active = topic_in.is_active

    topic.updated_at = datetime.now(timezone.utc)
    db.add(AuditLog(user_id=current_user.id, action="UPDATE_TOPIC", entity="TOPIC", entity_id=str(id)))
    db.commit()
    db.refresh(topic)
    return topic


@router.patch("/topics/{id}/status")
def admin_toggle_topic_status(
    id: int,
    req: StatusToggleRequest,
    current_user: User = Depends(require_role(["ADMIN"])),
    db: Session = Depends(get_db),
):
    """Toggle topic active/inactive status."""
    topic = db.query(Topic).filter(Topic.id == id).first()
    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")

    topic.is_active = req.is_active
    topic.updated_at = datetime.now(timezone.utc)
    action = "ACTIVATE_TOPIC" if req.is_active else "DEACTIVATE_TOPIC"
    db.add(AuditLog(user_id=current_user.id, action=action, entity="TOPIC", entity_id=str(id)))
    db.commit()
    return {"message": f"Topic {'activated' if req.is_active else 'deactivated'} successfully", "id": id, "is_active": req.is_active}


@router.post("/topics/reorder")
def admin_reorder_topics(
    req: ReorderRequest,
    current_user: User = Depends(require_role(["ADMIN"])),
    db: Session = Depends(get_db),
):
    """Reorder topics by display order."""
    for item in req.items:
        db.query(Topic).filter(Topic.id == item.id).update(
            {"display_order": item.order, "updated_at": datetime.now(timezone.utc)}
        )
    db.add(AuditLog(user_id=current_user.id, action="REORDER_TOPICS", entity="TOPIC", entity_id="BULK"))
    db.commit()
    return {"message": "Topics reordered successfully"}


@router.delete("/topics/{id}")
def admin_delete_topic(
    id: int,
    current_user: User = Depends(require_role(["ADMIN"])),
    db: Session = Depends(get_db),
):
    """Delete a topic."""
    topic = db.query(Topic).filter(Topic.id == id).first()
    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")

    db.delete(topic)
    db.add(AuditLog(user_id=current_user.id, action="DELETE_TOPIC", entity="TOPIC", entity_id=str(id)))
    db.commit()
    return {"message": "Topic deleted successfully", "id": id}


# ============================================================
# STUDY RESOURCE MANAGEMENT (CRUD + Reorder + Status Toggle)
# ============================================================

@router.get("/lessons/{lesson_id}/resources", response_model=List[StudyResourceOut])
def admin_get_lesson_resources(
    lesson_id: int,
    current_user: User = Depends(require_role(["ADMIN"])),
    db: Session = Depends(get_db),
):
    """List study resources under a lesson."""
    lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")

    resources = db.query(StudyResource).filter(StudyResource.lesson_id == lesson_id).order_by(StudyResource.display_order.asc()).all()
    return resources


@router.post("/lessons/{lesson_id}/resources", response_model=StudyResourceOut, status_code=status.HTTP_201_CREATED)
def admin_create_study_resource(
    lesson_id: int,
    resource_in: StudyResourceCreate,
    current_user: User = Depends(require_role(["ADMIN"])),
    db: Session = Depends(get_db),
):
    """Attach a verified study resource to a lesson."""
    lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")

    order = resource_in.display_order
    if order == 0:
        max_order = db.query(StudyResource.display_order).filter(StudyResource.lesson_id == lesson_id).order_by(StudyResource.display_order.desc()).first()
        order = (max_order[0] + 1) if max_order else 1

    resource = StudyResource(
        lesson_id=lesson_id,
        topic_id=resource_in.topic_id,
        title=resource_in.title,
        description=resource_in.description,
        url=resource_in.url,
        resource_type=resource_in.resource_type,
        provider=resource_in.provider,
        display_order=order,
        is_active=resource_in.is_active,
    )
    db.add(resource)
    db.flush()
    db.add(AuditLog(user_id=current_user.id, action="CREATE_STUDY_RESOURCE", entity="STUDY_RESOURCE", entity_id=str(resource.id)))
    db.commit()
    db.refresh(resource)
    return resource


@router.get("/resources/{id}", response_model=StudyResourceOut)
def admin_get_resource(
    id: int,
    current_user: User = Depends(require_role(["ADMIN"])),
    db: Session = Depends(get_db),
):
    """Get single study resource detail."""
    res = db.query(StudyResource).filter(StudyResource.id == id).first()
    if not res:
        raise HTTPException(status_code=404, detail="Study resource not found")
    return res


@router.patch("/resources/{id}", response_model=StudyResourceOut)
def admin_update_study_resource(
    id: int,
    res_in: StudyResourceUpdate,
    current_user: User = Depends(require_role(["ADMIN"])),
    db: Session = Depends(get_db),
):
    """Update study resource fields."""
    res = db.query(StudyResource).filter(StudyResource.id == id).first()
    if not res:
        raise HTTPException(status_code=404, detail="Study resource not found")

    if res_in.title is not None:
        res.title = res_in.title
    if res_in.description is not None:
        res.description = res_in.description
    if res_in.url is not None:
        res.url = res_in.url
    if res_in.resource_type is not None:
        res.resource_type = res_in.resource_type
    if res_in.provider is not None:
        res.provider = res_in.provider
    if res_in.display_order is not None:
        res.display_order = res_in.display_order
    if res_in.is_active is not None:
        res.is_active = res_in.is_active
    if res_in.topic_id is not None:
        res.topic_id = res_in.topic_id

    res.updated_at = datetime.now(timezone.utc)
    db.add(AuditLog(user_id=current_user.id, action="UPDATE_STUDY_RESOURCE", entity="STUDY_RESOURCE", entity_id=str(id)))
    db.commit()
    db.refresh(res)
    return res


@router.patch("/resources/{id}/status")
def admin_toggle_resource_status(
    id: int,
    req: StatusToggleRequest,
    current_user: User = Depends(require_role(["ADMIN"])),
    db: Session = Depends(get_db),
):
    """Toggle study resource active/inactive status."""
    res = db.query(StudyResource).filter(StudyResource.id == id).first()
    if not res:
        raise HTTPException(status_code=404, detail="Study resource not found")

    res.is_active = req.is_active
    res.updated_at = datetime.now(timezone.utc)
    action = "ACTIVATE_STUDY_RESOURCE" if req.is_active else "DEACTIVATE_STUDY_RESOURCE"
    db.add(AuditLog(user_id=current_user.id, action=action, entity="STUDY_RESOURCE", entity_id=str(id)))
    db.commit()
    return {"message": f"Resource {'activated' if req.is_active else 'deactivated'} successfully", "id": id, "is_active": req.is_active}


@router.post("/resources/reorder")
def admin_reorder_resources(
    req: ReorderRequest,
    current_user: User = Depends(require_role(["ADMIN"])),
    db: Session = Depends(get_db),
):
    """Reorder study resources."""
    for item in req.items:
        db.query(StudyResource).filter(StudyResource.id == item.id).update(
            {"display_order": item.order, "updated_at": datetime.now(timezone.utc)}
        )
    db.add(AuditLog(user_id=current_user.id, action="REORDER_RESOURCES", entity="STUDY_RESOURCE", entity_id="BULK"))
    db.commit()
    return {"message": "Resources reordered successfully"}


@router.delete("/resources/{id}")
def admin_delete_study_resource(
    id: int,
    current_user: User = Depends(require_role(["ADMIN"])),
    db: Session = Depends(get_db),
):
    """Delete a study resource."""
    res = db.query(StudyResource).filter(StudyResource.id == id).first()
    if not res:
        raise HTTPException(status_code=404, detail="Study resource not found")

    db.delete(res)
    db.add(AuditLog(user_id=current_user.id, action="DELETE_STUDY_RESOURCE", entity="STUDY_RESOURCE", entity_id=str(id)))
    db.commit()
    return {"message": "Study resource deleted successfully", "id": id}


# ============================================================
# QUESTION BANK CRUD
# ============================================================

@router.get("/questions", response_model=List[QuestionOut])
def admin_get_questions(
    current_user: User = Depends(require_role(["ADMIN"])),
    db: Session = Depends(get_db),
):
    """List questions in the question bank."""
    questions = db.query(Question).all()
    results = []
    for q in questions:
        try:
            opts = json.loads(q.options) if isinstance(q.options, str) else q.options
        except Exception:
            opts = [q.options]
        results.append(
            QuestionOut(
                id=q.id,
                subject_id=q.subject_id,
                topic_id=q.topic_id,
                topic_name=q.topic.name if q.topic else None,
                question_text=q.question_text,
                question_type=q.question_type,
                options=opts,
                difficulty=q.difficulty,
            )
        )
    return results


@router.post("/questions", response_model=QuestionOut, status_code=status.HTTP_201_CREATED)
def admin_create_question(
    q_in: QuestionCreate,
    current_user: User = Depends(require_role(["ADMIN"])),
    db: Session = Depends(get_db),
):
    """Add a question to the question bank."""
    q = Question(
        subject_id=q_in.subject_id,
        topic_id=q_in.topic_id,
        question_text=q_in.question_text,
        question_type=q_in.question_type,
        options=json.dumps(q_in.options),
        correct_answer=q_in.correct_answer,
        explanation=q_in.explanation,
        difficulty=q_in.difficulty,
    )
    db.add(q)
    db.flush()
    db.add(AuditLog(user_id=current_user.id, action="CREATE_QUESTION", entity="QUESTION", entity_id=str(q.id)))
    db.commit()
    db.refresh(q)
    return QuestionOut(
        id=q.id,
        subject_id=q.subject_id,
        topic_id=q.topic_id,
        topic_name=q.topic.name if q.topic else None,
        question_text=q.question_text,
        question_type=q.question_type,
        options=q_in.options,
        difficulty=q.difficulty,
    )


@router.delete("/questions/{id}")
def admin_delete_question(
    id: int,
    current_user: User = Depends(require_role(["ADMIN"])),
    db: Session = Depends(get_db),
):
    """Remove a question from question bank."""
    q = db.query(Question).filter(Question.id == id).first()
    if not q:
        raise HTTPException(status_code=404, detail="Question not found")
    db.delete(q)
    db.add(AuditLog(user_id=current_user.id, action="DELETE_QUESTION", entity="QUESTION", entity_id=str(id)))
    db.commit()
    return {"message": "Question deleted successfully", "id": id}


# ============================================================
# QUIZ MANAGEMENT
# ============================================================

@router.get("/quizzes", response_model=List[QuizOut])
def admin_get_quizzes(
    current_user: User = Depends(require_role(["ADMIN"])),
    db: Session = Depends(get_db),
):
    """List quizzes with metadata."""
    quizzes = db.query(Quiz).all()
    results = []
    for q in quizzes:
        subj = db.query(Subject).filter(Subject.id == q.subject_id).first()
        results.append(
            QuizOut(
                id=q.id,
                subject_id=q.subject_id,
                subject_name=subj.name if subj else None,
                title=q.title,
                description=q.description,
                quiz_type=q.quiz_type,
                difficulty=q.difficulty,
                question_count=q.question_count,
            )
        )
    return results


@router.post("/quizzes", response_model=QuizOut, status_code=status.HTTP_201_CREATED)
def admin_create_quiz(
    quiz_in: QuizCreate,
    current_user: User = Depends(require_role(["ADMIN"])),
    db: Session = Depends(get_db),
):
    """Create a new quiz and assign questions."""
    q = Quiz(
        subject_id=quiz_in.subject_id,
        title=quiz_in.title,
        description=quiz_in.description,
        quiz_type=quiz_in.quiz_type,
        difficulty=quiz_in.difficulty,
        question_count=quiz_in.question_count,
    )
    db.add(q)
    db.flush()

    if quiz_in.question_ids:
        for idx, qid in enumerate(quiz_in.question_ids):
            assoc = QuizQuestion(quiz_id=q.id, question_id=qid, order_index=idx + 1)
            db.add(assoc)

    db.add(AuditLog(user_id=current_user.id, action="CREATE_QUIZ", entity="QUIZ", entity_id=str(q.id)))
    db.commit()
    db.refresh(q)

    subj = db.query(Subject).filter(Subject.id == q.subject_id).first()
    return QuizOut(
        id=q.id,
        subject_id=q.subject_id,
        subject_name=subj.name if subj else None,
        title=q.title,
        description=q.description,
        quiz_type=q.quiz_type,
        difficulty=q.difficulty,
        question_count=q.question_count,
    )
