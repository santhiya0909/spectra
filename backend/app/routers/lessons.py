import json
from typing import List, Optional, Any, Dict
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.db.database import get_db
from app.db.models.academic import Lesson, LessonProgress, Subject, Topic, StudyResource
from app.db.models.puzzle import Puzzle, PuzzleAttempt
from app.db.models.quiz import Quiz, Question, QuizAttempt, QuizResponse
from app.db.models.performance import StudentTopicPerformance
from app.schemas.academic import LessonOut, LessonProgressUpdate, TopicOut, StudyResourceOut, LessonYouTubeResponse
from app.schemas.quiz import QuizOut, QuestionOut, QuizSubmission, QuizResultOut
from app.core.dependencies import get_current_user, get_current_student, get_optional_current_user
from app.db.models.user import User, StudentProfile
from app.routers.puzzles import format_puzzle_out

router = APIRouter(tags=["Lessons & Topics"])


@router.get("/lessons", response_model=List[LessonOut])
def get_lessons(
    subject_id: Optional[int] = Query(None),
    topic_id: Optional[int] = Query(None),
    search: Optional[str] = Query(None),
    difficulty: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_current_user),
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
        topics_done = 0
        puzzles_done = 0
        quiz_done = False
        xp_earned = 0

        if student:
            prog = db.query(LessonProgress).filter(
                LessonProgress.student_id == student.id,
                LessonProgress.lesson_id == l.id,
            ).first()
            if prog:
                status = prog.status
                pct = prog.completion_percentage
                topics_done = prog.topics_completed or 0
                puzzles_done = prog.puzzles_completed or 0
                quiz_done = prog.quiz_completed or False
                xp_earned = prog.xp_earned or 0

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
                topics_completed=topics_done,
                puzzles_completed=puzzles_done,
                quiz_completed=quiz_done,
                xp_earned=xp_earned,
                topics=[TopicOut.model_validate(t) for t in child_topics],
                study_resources=[StudyResourceOut.model_validate(r) for r in child_resources],
                created_at=l.created_at,
                updated_at=l.updated_at,
            )
        )
    return results


@router.get("/lessons/{lesson_id}", response_model=LessonOut)
def get_lesson(
    lesson_id: int,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_current_user),
):
    """Retrieve deep details, structured topics, verified external resources, and content for a single lesson."""
    l = db.query(Lesson).filter(Lesson.id == lesson_id).first()
    if not l:
        raise HTTPException(status_code=404, detail="Lesson not found")

    if (not current_user or current_user.role == "STUDENT") and not l.is_active:
        raise HTTPException(status_code=404, detail="Lesson is currently unavailable")

    status = "NOT_STARTED"
    pct = 0.0
    topics_done = 0
    puzzles_done = 0
    quiz_done = False
    xp_earned = 0
    student = None

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
                topics_done = prog.topics_completed or 0
                puzzles_done = prog.puzzles_completed or 0
                quiz_done = prog.quiz_completed or False
                xp_earned = prog.xp_earned or 0

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

    # Puzzles for this lesson
    lesson_puzzles = db.query(Puzzle).filter(
        Puzzle.lesson_id == l.id,
        Puzzle.is_active == True
    ).order_by(Puzzle.display_order.asc(), Puzzle.id.asc()).all()
    puzzles_out = [format_puzzle_out(p, student_id=student.id if student else None, db=db) for p in lesson_puzzles]

    # Quizzes for this lesson
    quizzes = db.query(Quiz).filter(Quiz.lesson_id == l.id).all()
    quizzes_out = []
    for q in quizzes:
        best_score = None
        attempts_count = 0
        if student:
            attempts = db.query(QuizAttempt).filter(
                QuizAttempt.student_id == student.id,
                QuizAttempt.quiz_id == q.id
            ).all()
            attempts_count = len(attempts)
            if attempts:
                best_score = max(a.percentage for a in attempts)
        quizzes_out.append({
            "id": q.id,
            "title": q.title,
            "description": q.description,
            "quiz_type": q.quiz_type,
            "difficulty": q.difficulty,
            "question_count": q.question_count,
            "best_score": best_score,
            "attempts_count": attempts_count
        })

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
        topics_completed=topics_done,
        puzzles_completed=puzzles_done,
        quiz_completed=quiz_done,
        xp_earned=xp_earned,
        topics=[TopicOut.model_validate(t) for t in child_topics],
        study_resources=[StudyResourceOut.model_validate(r) for r in child_resources],
        puzzles=puzzles_out,
        quizzes=quizzes_out,
        created_at=l.created_at,
        updated_at=l.updated_at,
    )


@router.get("/lessons/{lesson_id}/youtube", response_model=LessonYouTubeResponse)
def get_lesson_youtube_recommendations_endpoint(
    lesson_id: int,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_current_user),
):
    """
    Fetch 3 relevant educational YouTube video recommendations for a lesson.
    Automatically generates search query, filters educational content,
    and caches recommendations in the database.
    """
    from app.services.youtube_service import get_or_create_lesson_youtube_recommendations
    return get_or_create_lesson_youtube_recommendations(db, lesson_id)


@router.post("/lessons/{lesson_id}/progress")
def update_lesson_progress(
    lesson_id: int,
    progress_in: LessonProgressUpdate,
    student: StudentProfile = Depends(get_current_student),
    db: Session = Depends(get_db),
):
    """
    Update student progress for a lesson.
    Follows pedagogical weighting:
    - Topic Content: 40%
    - Puzzle: 20%
    - Practice: 10%
    - Quiz: 30%
    Awards XP for completion and milestone activities.
    """
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
            status="IN_PROGRESS",
            completion_percentage=20.0,
            topics_completed=0,
            puzzles_completed=0,
            quiz_completed=False,
            xp_earned=0
        )
        db.add(prog)
        db.flush()

    xp_awarded = 0
    # Handle actions
    if progress_in.action_type == "TOPIC_READ":
        prog.topics_completed = (prog.topics_completed or 0) + 1
        # Award +5 XP for reading/completing topic
        xp_awarded += 5
        student.xp = (student.xp or 0) + 5
        prog.xp_earned = (prog.xp_earned or 0) + 5
        student.last_active_date = now

    elif progress_in.action_type == "PUZZLE_SOLVED":
        prog.puzzles_completed = (prog.puzzles_completed or 0) + 1

    elif progress_in.action_type == "QUIZ_PASSED":
        prog.quiz_completed = True
        if progress_in.quiz_score is not None:
            prog.quiz_score = max(prog.quiz_score or 0.0, progress_in.quiz_score)

    # Calculate weighted percentage
    total_puzzles = db.query(Puzzle).filter(Puzzle.lesson_id == lesson_id, Puzzle.is_active == True).count() or 1
    total_topics = db.query(Topic).filter(Topic.lesson_id == lesson_id, Topic.is_active == True).count() or 1

    topic_pct = min(40.0, 40.0 if (prog.topics_completed or 0) >= total_topics else (20.0 if (prog.topics_completed or 0) > 0 else 10.0))
    puzzle_pct = min(20.0, ((prog.puzzles_completed or 0) / total_puzzles) * 20.0)
    quiz_pct = 30.0 if prog.quiz_completed else 0.0
    practice_pct = 10.0 if (prog.completion_percentage or 0) >= 60.0 else 0.0

    calc_pct = min(100.0, round(topic_pct + puzzle_pct + practice_pct + quiz_pct, 1))
    if progress_in.completion_percentage is not None:
        calc_pct = max(calc_pct, progress_in.completion_percentage)

    prog.completion_percentage = max(prog.completion_percentage or 0.0, calc_pct)

    # Check for completion (95%+ or passing quiz + puzzles)
    if prog.completion_percentage >= 95.0 or (prog.quiz_completed and (prog.puzzles_completed or 0) >= total_puzzles):
        if prog.status != "COMPLETED":
            prog.status = "COMPLETED"
            prog.completed_at = now
            # Award lesson completion XP (+30 XP)
            xp_awarded += 30
            student.xp = (student.xp or 0) + 30
            prog.xp_earned = (prog.xp_earned or 0) + 30
    else:
        if prog.status == "NOT_STARTED":
            prog.status = "IN_PROGRESS"

    db.commit()
    db.refresh(prog)

    return {
        "message": "Progress recorded successfully",
        "status": prog.status,
        "completion_percentage": prog.completion_percentage,
        "xp_earned": xp_awarded,
        "topics_completed": prog.topics_completed,
        "puzzles_completed": prog.puzzles_completed,
        "quiz_completed": prog.quiz_completed,
    }


@router.get("/lessons/{lesson_id}/quiz")
def get_lesson_quiz(
    lesson_id: int,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user),
):
    """Retrieve the primary quiz associated with a lesson."""
    quiz = db.query(Quiz).filter(Quiz.lesson_id == lesson_id).first()
    if not quiz:
        # Fallback: check if lesson has a subject quiz
        lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()
        if lesson:
            quiz = db.query(Quiz).filter(Quiz.subject_id == lesson.subject_id).first()

    if not quiz:
        raise HTTPException(status_code=404, detail="No quiz configured for this lesson yet")

    subj = db.query(Subject).filter(Subject.id == quiz.subject_id).first()
    student = None
    best_score = None
    attempts_count = 0
    if current_user and current_user.role == "STUDENT":
        student = db.query(StudentProfile).filter(StudentProfile.user_id == current_user.id).first()
        if student:
            attempts = db.query(QuizAttempt).filter(
                QuizAttempt.student_id == student.id,
                QuizAttempt.quiz_id == quiz.id
            ).all()
            attempts_count = len(attempts)
            if attempts:
                best_score = max(a.percentage for a in attempts)

    return QuizOut(
        id=quiz.id,
        subject_id=quiz.subject_id,
        lesson_id=quiz.lesson_id,
        topic_id=quiz.topic_id,
        subject_name=subj.name if subj else None,
        title=quiz.title,
        description=quiz.description,
        quiz_type=quiz.quiz_type,
        difficulty=quiz.difficulty,
        question_count=quiz.question_count,
        best_score=best_score,
        attempts_count=attempts_count
    )


# ============================================================
# TOPIC PRACTICE (Practice Topic - 3 to 5 Questions)
# ============================================================

@router.get("/topics/{topic_id}/practice", response_model=List[QuestionOut])
def get_topic_practice_questions(
    topic_id: int,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user)
):
    """Retrieve 3-5 practice questions specific to a topic."""
    topic = db.query(Topic).filter(Topic.id == topic_id).first()
    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")

    questions = db.query(Question).filter(
        Question.topic_id == topic_id
    ).limit(5).all()

    if not questions:
        # Fallback to subject questions
        questions = db.query(Question).filter(
            Question.subject_id == topic.subject_id
        ).limit(5).all()

    outs = []
    for q in questions:
        try:
            opts = json.loads(q.options) if isinstance(q.options, str) else q.options
        except Exception:
            opts = [q.options]
        outs.append(
            QuestionOut(
                id=q.id,
                subject_id=q.subject_id,
                topic_id=q.topic_id,
                lesson_id=q.lesson_id,
                topic_name=topic.name,
                question_text=q.question_text,
                question_type=q.question_type,
                options=opts,
                difficulty=q.difficulty
            )
        )
    return outs


@router.post("/topics/{topic_id}/practice/submit")
def submit_topic_practice(
    topic_id: int,
    submission: QuizSubmission,
    student: StudentProfile = Depends(get_current_student),
    db: Session = Depends(get_db)
):
    """
    Submits answers for topic practice:
    - Calculates accuracy
    - Awards +10 XP for practicing
    - Updates StudentTopicPerformance
    """
    topic = db.query(Topic).filter(Topic.id == topic_id).first()
    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")

    answers_map = {ans.question_id: ans for ans in submission.answers}
    questions = db.query(Question).filter(Question.id.in_(list(answers_map.keys()))).all()

    correct_count = 0
    total = len(questions)
    for q in questions:
        user_ans = answers_map.get(q.id)
        if not user_ans or not user_ans.selected_answer:
            continue
        sel = user_ans.selected_answer.strip().lower()
        corr = q.correct_answer.strip().lower()
        if sel == corr or sel[0:2] == corr[0:2]:
            correct_count += 1

    pct = round((correct_count / total * 100.0), 1) if total > 0 else 0.0

    # Award +10 XP for completing topic practice
    xp_awarded = 10
    student.xp = (student.xp or 0) + xp_awarded
    student.last_active_date = datetime.now(timezone.utc)

    # Update StudentTopicPerformance
    perf = db.query(StudentTopicPerformance).filter(
        StudentTopicPerformance.student_id == student.id,
        StudentTopicPerformance.topic_id == topic_id
    ).first()

    now = datetime.now(timezone.utc)
    if not perf:
        perf = StudentTopicPerformance(
            student_id=student.id,
            topic_id=topic_id,
            attempts=1,
            correct_answers=correct_count,
            total_questions=total,
            accuracy=pct,
            mastery_score=pct,
            last_attempt_at=now
        )
        db.add(perf)
    else:
        perf.attempts = (perf.attempts or 0) + 1
        perf.correct_answers = (perf.correct_answers or 0) + correct_count
        perf.total_questions = (perf.total_questions or 0) + total
        if perf.total_questions > 0:
            perf.accuracy = round((perf.correct_answers / perf.total_questions) * 100.0, 1)
        # Weighted adaptive mastery update
        perf.mastery_score = round(0.4 * perf.mastery_score + 0.6 * pct, 1)
        perf.last_attempt_at = now

    db.commit()

    return {
        "topic_id": topic_id,
        "topic_name": topic.name,
        "score": correct_count,
        "total_questions": total,
        "percentage": pct,
        "xp_earned": xp_awarded,
        "mastery_score": perf.mastery_score,
        "status": "MASTERED" if perf.mastery_score >= 80.0 else ("NEEDS_PRACTICE" if perf.mastery_score < 60.0 else "PROFICIENT")
    }
