from typing import List, Optional, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db.models.quiz import Quiz, QuizAttempt, QuizResponse, Question
from app.db.models.academic import Subject, Topic
from app.schemas.quiz import (
    QuizOut, QuizDetailOut, QuizSubmission, QuizResultOut,
    QuizAttemptOut, QuestionOut, QuestionReviewOut
)
from app.services.quiz_service import get_questions_for_quiz, submit_quiz_attempt
from app.core.dependencies import get_current_user, get_current_student
from app.db.models.user import User, StudentProfile
import json

router = APIRouter(prefix="/quizzes", tags=["Quizzes"])

@router.get("", response_model=List[QuizOut])
def get_quizzes(
    subject_id: Optional[int] = Query(None),
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user)
):
    """Retrieve all available quizzes with attempts and highest score achieved."""
    query = db.query(Quiz)
    if subject_id:
        query = query.filter(Quiz.subject_id == subject_id)
    quizzes = query.all()

    student = None
    if current_user and current_user.role == "STUDENT":
        student = db.query(StudentProfile).filter(StudentProfile.user_id == current_user.id).first()

    results = []
    for q in quizzes:
        subj = db.query(Subject).filter(Subject.id == q.subject_id).first()
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
                best_score=best_score,
                attempts_count=attempts_count
            )
        )
    return results

@router.get("/{quiz_id}", response_model=QuizOut)
def get_quiz_info(quiz_id: int, db: Session = Depends(get_db)):
    """Retrieve quiz metadata."""
    q = db.query(Quiz).filter(Quiz.id == quiz_id).first()
    if not q:
        raise HTTPException(status_code=404, detail="Quiz not found")
    subj = db.query(Subject).filter(Subject.id == q.subject_id).first()
    return QuizOut(
        id=q.id,
        subject_id=q.subject_id,
        subject_name=subj.name if subj else None,
        title=q.title,
        description=q.description,
        quiz_type=q.quiz_type,
        difficulty=q.difficulty,
        question_count=q.question_count
    )

@router.post("/{quiz_id}/start", response_model=List[QuestionOut])
def start_quiz(
    quiz_id: int,
    student: StudentProfile = Depends(get_current_student),
    db: Session = Depends(get_db)
):
    """
    Initializes a quiz attempt and serves questions.
    Applies adaptive question selection based on current student mastery.
    """
    questions = get_questions_for_quiz(db, quiz_id, student_id=student.id)
    return questions

@router.post("/{quiz_id}/submit", response_model=QuizResultOut)
def submit_quiz(
    quiz_id: int,
    submission: QuizSubmission,
    student: StudentProfile = Depends(get_current_student),
    db: Session = Depends(get_db)
):
    """
    Evaluates quiz submission:
    - Calculates score & percentage
    - Persists attempt & responses
    - Updates topic performances
    - Detects knowledge gaps
    - Triggers targeted recommendations
    - Generates teacher alerts if necessary
    """
    return submit_quiz_attempt(db, quiz_id, student.id, submission)

@router.get("/attempts", response_model=List[QuizAttemptOut])
def get_student_attempts(
    student: StudentProfile = Depends(get_current_student),
    db: Session = Depends(get_db)
):
    """Retrieve all quiz attempts for the logged-in student."""
    attempts = db.query(QuizAttempt).filter(
        QuizAttempt.student_id == student.id
    ).order_by(QuizAttempt.started_at.desc()).all()

    outs = []
    for a in attempts:
        quiz = db.query(Quiz).filter(Quiz.id == a.quiz_id).first()
        subj = db.query(Subject).filter(Subject.id == quiz.subject_id).first() if quiz else None
        outs.append(
            QuizAttemptOut(
                id=a.id,
                quiz_id=a.quiz_id,
                quiz_title=quiz.title if quiz else "Quiz",
                subject_name=subj.name if subj else "General",
                score=a.score,
                percentage=a.percentage,
                started_at=a.started_at,
                completed_at=a.completed_at
            )
        )
    return outs

@router.get("/attempts/{attempt_id}", response_model=QuizResultOut)
def get_attempt_details(
    attempt_id: int,
    student: StudentProfile = Depends(get_current_student),
    db: Session = Depends(get_db)
):
    """Detailed post-assessment review of questions, answers, and explanations."""
    attempt = db.query(QuizAttempt).filter(
        QuizAttempt.id == attempt_id,
        QuizAttempt.student_id == student.id
    ).first()
    if not attempt:
        raise HTTPException(status_code=404, detail="Attempt not found")

    quiz = db.query(Quiz).filter(Quiz.id == attempt.quiz_id).first()
    responses = db.query(QuizResponse).filter(QuizResponse.attempt_id == attempt.id).all()

    reviews = []
    weak_topics = []
    for r in responses:
        q = db.query(Question).filter(Question.id == r.question_id).first()
        if not q:
            continue
        try:
            opts = json.loads(q.options) if isinstance(q.options, str) else q.options
        except Exception:
            opts = [q.options]

        top = db.query(Topic).filter(Topic.id == q.topic_id).first()
        if not r.is_correct and top and top.name not in weak_topics:
            weak_topics.append(top.name)

        reviews.append(
            QuestionReviewOut(
                id=q.id,
                question_text=q.question_text,
                options=opts,
                selected_answer=r.selected_answer,
                correct_answer=q.correct_answer,
                is_correct=r.is_correct,
                explanation=q.explanation or "Standard concept evaluation.",
                topic_id=q.topic_id,
                topic_name=top.name if top else "General"
            )
        )

    status_str = "PASSED" if attempt.percentage >= 70.0 else ("NEEDS_IMPROVEMENT" if attempt.percentage >= 40.0 else "FAILED")

    return QuizResultOut(
        attempt_id=attempt.id,
        quiz_id=quiz.id if quiz else 0,
        quiz_title=quiz.title if quiz else "Quiz",
        score=attempt.score,
        total_questions=len(responses),
        percentage=attempt.percentage,
        status=status_str,
        questions_review=reviews,
        weak_topics=weak_topics,
        recommendations_generated=["Review weak topics in learning plan"]
    )
