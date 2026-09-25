from typing import List, Dict, Any
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.core.dependencies import get_current_student
from app.db.models.user import StudentProfile
from app.db.models.academic import Topic, Subject, Lesson, LessonProgress
from app.db.models.quiz import QuizAttempt, Quiz
from app.db.models.performance import StudentTopicPerformance
from app.schemas.performance import PerformanceOverviewOut, TopicPerformanceOut, PerformanceHistoryOut, HistoryItem

router = APIRouter(prefix="/performance", tags=["Performance & Analytics"])

@router.get("/overview", response_model=PerformanceOverviewOut)
def get_performance_overview(
    student: StudentProfile = Depends(get_current_student),
    db: Session = Depends(get_db)
):
    """Retrieve comprehensive performance metrics and classified topics for the current student."""
    attempts = db.query(QuizAttempt).filter(QuizAttempt.student_id == student.id).all()
    avg_score = round(sum(a.percentage for a in attempts) / len(attempts), 1) if attempts else 0.0

    completed_lessons = db.query(LessonProgress).filter(
        LessonProgress.student_id == student.id,
        LessonProgress.status == "COMPLETED"
    ).count()
    total_lessons = db.query(Lesson).count()
    overall_progress = round((completed_lessons / total_lessons * 100.0), 1) if total_lessons > 0 else 0.0

    perfs = db.query(StudentTopicPerformance).filter(StudentTopicPerformance.student_id == student.id).all()
    weak_topics = []
    strong_topics = []

    for p in perfs:
        t = db.query(Topic).filter(Topic.id == p.topic_id).first()
        subj = t.subject if t else None
        status = "WEAK" if (p.mastery_score < 60.0 or p.accuracy < 60.0) else ("NEEDS_PRACTICE" if p.mastery_score < 75.0 else "MASTERED")
        
        item = TopicPerformanceOut(
            topic_id=p.topic_id,
            topic_name=t.name if t else "Topic",
            subject_id=t.subject_id if t else 0,
            subject_name=subj.name if subj else "General",
            attempts=p.attempts,
            correct_answers=p.correct_answers,
            total_questions=p.total_questions,
            accuracy=p.accuracy,
            mastery_score=p.mastery_score,
            difficulty_level=t.difficulty_level if t else "MEDIUM",
            status=status,
            last_attempt_at=p.last_attempt_at
        )
        if status == "WEAK":
            weak_topics.append(item)
        elif status == "MASTERED":
            strong_topics.append(item)

    return PerformanceOverviewOut(
        overall_progress=overall_progress,
        average_quiz_score=avg_score,
        lessons_completed=completed_lessons,
        total_lessons=total_lessons,
        current_streak=4,
        total_quizzes_taken=len(attempts),
        weak_topics=weak_topics,
        strong_topics=strong_topics
    )

@router.get("/topics", response_model=List[TopicPerformanceOut])
def get_topic_performances(
    student: StudentProfile = Depends(get_current_student),
    db: Session = Depends(get_db)
):
    """Retrieve mastery score and accuracy breakdown for each assessed topic."""
    perfs = db.query(StudentTopicPerformance).filter(StudentTopicPerformance.student_id == student.id).all()
    outs = []
    for p in perfs:
        t = db.query(Topic).filter(Topic.id == p.topic_id).first()
        subj = t.subject if t else None
        status = "WEAK" if (p.mastery_score < 60.0 or p.accuracy < 60.0) else ("NEEDS_PRACTICE" if p.mastery_score < 75.0 else "MASTERED")
        
        outs.append(
            TopicPerformanceOut(
                topic_id=p.topic_id,
                topic_name=t.name if t else "Topic",
                subject_id=t.subject_id if t else 0,
                subject_name=subj.name if subj else "General",
                attempts=p.attempts,
                correct_answers=p.correct_answers,
                total_questions=p.total_questions,
                accuracy=p.accuracy,
                mastery_score=p.mastery_score,
                difficulty_level=t.difficulty_level if t else "MEDIUM",
                status=status,
                last_attempt_at=p.last_attempt_at
            )
        )
    return outs

@router.get("/history", response_model=PerformanceHistoryOut)
def get_performance_history(
    student: StudentProfile = Depends(get_current_student),
    db: Session = Depends(get_db)
):
    """History trends for charting progress over time, topic mastery, and subject breakdown."""
    attempts = db.query(QuizAttempt).filter(
        QuizAttempt.student_id == student.id
    ).order_by(QuizAttempt.started_at.asc()).all()

    trends = []
    for a in attempts:
        quiz = db.query(Quiz).filter(Quiz.id == a.quiz_id).first()
        subj = db.query(Subject).filter(Subject.id == quiz.subject_id).first() if quiz else None
        trends.append(
            HistoryItem(
                date=a.started_at.strftime("%b %d"),
                score=a.percentage,
                quiz_title=quiz.title if quiz else "Quiz",
                subject_name=subj.name if subj else "General"
            )
        )

    # Subject breakdown
    subjects = db.query(Subject).all()
    subj_data = []
    for s in subjects:
        lessons = db.query(Lesson).filter(Lesson.subject_id == s.id).all()
        l_ids = [l.id for l in lessons]
        done = db.query(LessonProgress).filter(
            LessonProgress.student_id == student.id,
            LessonProgress.lesson_id.in_(l_ids),
            LessonProgress.status == "COMPLETED"
        ).count() if l_ids else 0
        pct = round((done / len(lessons) * 100.0), 1) if lessons else 0.0
        subj_data.append({
            "subject": s.name,
            "progress": pct,
            "completed": done,
            "total": len(lessons)
        })

    # Topic Mastery
    perfs = db.query(StudentTopicPerformance).filter(StudentTopicPerformance.student_id == student.id).all()
    topic_data = []
    for p in perfs:
        t = db.query(Topic).filter(Topic.id == p.topic_id).first()
        topic_data.append({
            "topic": t.name if t else f"Topic {p.topic_id}",
            "mastery": p.mastery_score,
            "accuracy": p.accuracy
        })

    return PerformanceHistoryOut(
        score_trends=trends,
        subject_progress=subj_data,
        topic_mastery=topic_data
    )
