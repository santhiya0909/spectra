from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.db.database import get_db
from app.db.models.academic import (
    Subject,
    Topic,
    Lesson,
    LessonProgress,
    Enrollment,
    StudyResource,
)
from app.db.models.quiz import Quiz
from app.schemas.academic import SubjectOut, TopicOut, LessonOut, StudyResourceOut
from app.core.dependencies import get_current_user, get_optional_current_user
from app.db.models.user import User, StudentProfile
from app.services.enrollment import enroll_student_in_default_subjects

router = APIRouter(prefix="/subjects", tags=["Subjects"])


# ============================================================
# GET ALL SUBJECTS (Student & Public)
# ============================================================

@router.get("", response_model=List[SubjectOut])
def get_subjects(
    search: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    difficulty: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_current_user),
):
    """
    Retrieve active subjects for students with optional search, category, and difficulty filtering.
    """
    student = None
    query = db.query(Subject)

    # For students or anonymous, only show active subjects
    if not current_user or current_user.role == "STUDENT":
        query = query.filter(Subject.is_active == True)

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

    if current_user and current_user.role == "STUDENT":
        student = (
            db.query(StudentProfile)
            .filter(StudentProfile.user_id == current_user.id)
            .first()
        )
        if student:
            enroll_student_in_default_subjects(db, student.id)

    subjects = query.order_by(Subject.display_order.asc(), Subject.id.asc()).all()

    results = []
    for subject in subjects:
        # Get active lessons
        lessons_query = db.query(Lesson).filter(Lesson.subject_id == subject.id)
        if not current_user or current_user.role == "STUDENT":
            lessons_query = lessons_query.filter(Lesson.is_active == True)
        lessons = lessons_query.order_by(Lesson.lesson_order.asc()).all()

        # Get active topics
        topics_query = db.query(Topic).filter(Topic.subject_id == subject.id)
        if not current_user or current_user.role == "STUDENT":
            topics_query = topics_query.filter(Topic.is_active == True)
        topics = topics_query.order_by(Topic.display_order.asc()).all()

        quizzes = db.query(Quiz).filter(Quiz.subject_id == subject.id).all()

        progress_percentage = 0.0
        completed = 0
        current_lesson = None
        if lessons:
            if student:
                lesson_ids = [l.id for l in lessons]
                completed_progs = (
                    db.query(LessonProgress)
                    .filter(
                        LessonProgress.student_id == student.id,
                        LessonProgress.lesson_id.in_(lesson_ids),
                    )
                    .all()
                )
                completed_ids = {p.lesson_id for p in completed_progs if p.status == "COMPLETED"}
                completed = len(completed_ids)
                progress_percentage = round(completed / len(lessons) * 100.0, 1)

                for l in lessons:
                    if l.id not in completed_ids:
                        current_lesson = {"id": l.id, "title": l.title, "lesson_order": l.lesson_order}
                        break
                if not current_lesson and lessons:
                    current_lesson = {"id": lessons[-1].id, "title": lessons[-1].title, "lesson_order": lessons[-1].lesson_order}
            else:
                current_lesson = {"id": lessons[0].id, "title": lessons[0].title, "lesson_order": lessons[0].lesson_order}

        results.append(
            SubjectOut(
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
                topics=[TopicOut.model_validate(topic) for topic in topics],
                lessons_count=len(lessons),
                quizzes_count=len(quizzes),
                progress_percentage=progress_percentage,
                completed_lessons_count=completed,
                current_lesson=current_lesson,
            )
        )

    return results


# ============================================================
# GET SUBJECT BY ID (Deep Curriculum Overview)
# ============================================================

@router.get("/{subject_id}", response_model=SubjectOut)
def get_subject_detail(
    subject_id: int,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_current_user),
):
    """
    Get detailed view of a subject with active lessons, child topics, study resources, and student progress.
    """
    subject = db.query(Subject).filter(Subject.id == subject_id).first()
    if not subject:
        raise HTTPException(status_code=404, detail="Subject not found")

    student = None
    if current_user and current_user.role == "STUDENT":
        if not subject.is_active:
            raise HTTPException(status_code=404, detail="Subject is currently inactive")

        student = (
            db.query(StudentProfile)
            .filter(StudentProfile.user_id == current_user.id)
            .first()
        )
        if student:
            enrollment = (
                db.query(Enrollment)
                .filter(
                    Enrollment.student_id == student.id,
                    Enrollment.subject_id == subject.id,
                )
                .first()
            )
            if not enrollment:
                enroll_student_in_default_subjects(db, student.id)

    # Lessons query
    lessons_query = db.query(Lesson).filter(Lesson.subject_id == subject.id)
    if not current_user or current_user.role == "STUDENT":
        lessons_query = lessons_query.filter(Lesson.is_active == True)
    lessons = lessons_query.order_by(Lesson.lesson_order.asc()).all()

    # Topics query
    topics_query = db.query(Topic).filter(Topic.subject_id == subject.id)
    if not current_user or current_user.role == "STUDENT":
        topics_query = topics_query.filter(Topic.is_active == True)
    topics = topics_query.order_by(Topic.display_order.asc()).all()

    quizzes = db.query(Quiz).filter(Quiz.subject_id == subject.id).all()

    # Calculate overall progress and lesson specific statuses
    completed_count = 0
    progress_percentage = 0.0
    lesson_progress_map = {}
    current_lesson = None

    if student and lessons:
        lesson_ids = [l.id for l in lessons]
        progs = (
            db.query(LessonProgress)
            .filter(
                LessonProgress.student_id == student.id,
                LessonProgress.lesson_id.in_(lesson_ids),
            )
            .all()
        )
        for p in progs:
            lesson_progress_map[p.lesson_id] = p

        completed_count = sum(1 for p in progs if p.status == "COMPLETED")
        progress_percentage = round(completed_count / len(lessons) * 100.0, 1)

        for l in lessons:
            p = lesson_progress_map.get(l.id)
            if not p or p.status != "COMPLETED":
                current_lesson = {"id": l.id, "title": l.title, "lesson_order": l.lesson_order}
                break
        if not current_lesson and lessons:
            current_lesson = {"id": lessons[-1].id, "title": lessons[-1].title, "lesson_order": lessons[-1].lesson_order}
    elif lessons:
        current_lesson = {"id": lessons[0].id, "title": lessons[0].title, "lesson_order": lessons[0].lesson_order}

    lesson_outs = []
    for l in lessons:
        l_status = "NOT_STARTED"
        l_pct = 0.0
        if l.id in lesson_progress_map:
            l_status = lesson_progress_map[l.id].status
            l_pct = lesson_progress_map[l.id].completion_percentage

        # Child topics under this lesson
        child_topics_query = db.query(Topic).filter(Topic.lesson_id == l.id)
        if not current_user or current_user.role == "STUDENT":
            child_topics_query = child_topics_query.filter(Topic.is_active == True)
        child_topics = child_topics_query.order_by(Topic.display_order.asc()).all()

        # Child study resources under this lesson
        child_resources_query = db.query(StudyResource).filter(StudyResource.lesson_id == l.id)
        if not current_user or current_user.role == "STUDENT":
            child_resources_query = child_resources_query.filter(StudyResource.is_active == True)
        child_resources = child_resources_query.order_by(StudyResource.display_order.asc()).all()

        lesson_outs.append(
            LessonOut(
                id=l.id,
                subject_id=l.subject_id,
                topic_id=l.topic_id,
                subject_name=subject.name,
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
                status=l_status,
                completion_percentage=l_pct,
                topics=[TopicOut.model_validate(t) for t in child_topics],
                study_resources=[StudyResourceOut.model_validate(r) for r in child_resources],
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
        topics=[TopicOut.model_validate(topic) for topic in topics],
        lessons=lesson_outs,
        lessons_count=len(lessons),
        quizzes_count=len(quizzes),
        progress_percentage=progress_percentage,
        completed_lessons_count=completed_count,
        current_lesson=current_lesson,
    )


# ============================================================
# GET SUBJECT TOPICS
# ============================================================

@router.get("/{subject_id}/topics", response_model=List[TopicOut])
def get_subject_topics(
    subject_id: int,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_current_user),
):
    """
    Retrieve all active topics under a specific subject.
    """
    subject = db.query(Subject).filter(Subject.id == subject_id).first()
    if not subject:
        raise HTTPException(status_code=404, detail="Subject not found")

    query = db.query(Topic).filter(Topic.subject_id == subject_id)
    if not current_user or current_user.role == "STUDENT":
        query = query.filter(Topic.is_active == True)

    return query.order_by(Topic.display_order.asc(), Topic.id.asc()).all()