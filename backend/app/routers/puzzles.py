from typing import List, Optional, Any
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
import json

from app.db.database import get_db
from app.db.models.puzzle import Puzzle, PuzzleAttempt
from app.db.models.academic import Subject, Lesson, Topic, LessonProgress
from app.db.models.performance import StudentTopicPerformance
from app.db.models.user import User, StudentProfile
from app.core.dependencies import get_current_user, get_current_student, require_admin
from app.schemas.puzzle import (
    PuzzleOut, PuzzleAdminOut, PuzzleCreate, PuzzleUpdate,
    PuzzleSubmission, PuzzleSubmissionResult, StudentPuzzleProgressOut, PuzzleAttemptSummary
)
from app.services.puzzle_service import submit_puzzle_solution

router = APIRouter(tags=["Puzzles"])

def format_puzzle_out(puzzle: Puzzle, student_id: Optional[int] = None, db: Optional[Session] = None) -> PuzzleOut:
    """Safely format a puzzle for student consumption, strictly omitting correct_answer."""
    try:
        p_data = json.loads(puzzle.puzzle_data) if isinstance(puzzle.puzzle_data, str) else puzzle.puzzle_data
    except Exception:
        p_data = puzzle.puzzle_data

    user_solved = False
    user_attempts = 0
    if student_id and db:
        attempts = db.query(PuzzleAttempt).filter(
            PuzzleAttempt.puzzle_id == puzzle.id,
            PuzzleAttempt.student_id == student_id
        ).all()
        user_attempts = len(attempts)
        user_solved = any(a.is_correct for a in attempts)

    # Contextual metadata
    topic_name = puzzle.topic.name if puzzle.topic else (puzzle.lesson.topic.name if puzzle.lesson and puzzle.lesson.topic else None)
    lesson_title = puzzle.lesson.title if puzzle.lesson else None
    subject_name = puzzle.subject.name if puzzle.subject else None

    # Calculate index in lesson
    puzzle_index = 1
    total_in_lesson = 1
    if db and puzzle.lesson_id:
        lesson_puzzles = db.query(Puzzle.id).filter(
            Puzzle.lesson_id == puzzle.lesson_id,
            Puzzle.is_active == True
        ).order_by(Puzzle.display_order.asc(), Puzzle.id.asc()).all()
        total_in_lesson = len(lesson_puzzles) or 1
        ids = [lp[0] for lp in lesson_puzzles]
        if puzzle.id in ids:
            puzzle_index = ids.index(puzzle.id) + 1

    ptype = (puzzle.puzzle_type or "").upper()
    instructions = "Choose the best answer to complete this challenge."
    if ptype == "ORDERING":
        instructions = "Drag or use the up/down controls to arrange the items into the correct sequence."
    elif ptype == "MATCHING":
        instructions = "Pair each concept on the left with its matching definition or counterpart."
    elif ptype == "FILL_BLANK":
        instructions = "Fill in the missing term, syntax token, or value to solve this challenge."
    elif ptype == "CODE_OUTPUT":
        instructions = "Examine the code snippet carefully and determine its exact runtime behavior."
    elif ptype == "TRUE_FALSE":
        instructions = "Evaluate the statement and select whether it is conceptually True or False."

    diff = (puzzle.difficulty or "MEDIUM").upper()
    est_time = "2 min" if diff == "EASY" else ("3 min" if diff == "MEDIUM" else "5 min")

    return PuzzleOut(
        id=puzzle.id,
        subject_id=puzzle.subject_id,
        lesson_id=puzzle.lesson_id,
        topic_id=puzzle.topic_id,
        title=puzzle.title,
        description=puzzle.description,
        puzzle_type=puzzle.puzzle_type,
        question=puzzle.question,
        puzzle_data=p_data,
        difficulty=puzzle.difficulty or "MEDIUM",
        xp_reward=puzzle.xp_reward or 10,
        display_order=puzzle.display_order or 0,
        is_active=puzzle.is_active,
        user_solved=user_solved,
        user_attempts=user_attempts,
        topic_name=topic_name,
        lesson_title=lesson_title,
        subject_name=subject_name,
        estimated_time=est_time,
        instructions=instructions,
        puzzle_index=puzzle_index,
        total_in_lesson=total_in_lesson
    )

@router.get("/puzzles", response_model=List[PuzzleOut])
def list_student_puzzles(
    subject_id: Optional[int] = Query(None),
    lesson_id: Optional[int] = Query(None),
    topic_id: Optional[int] = Query(None),
    filter: Optional[str] = Query("all", description="all, weak, developing, unsolved, completed"),
    student: StudentProfile = Depends(get_current_student),
    db: Session = Depends(get_db)
):
    """
    List puzzles with rich learning filters:
    - all: all available puzzles
    - unsolved: puzzles not yet completed
    - completed: puzzles solved by the student
    - weak: puzzles tied to topics where student accuracy/mastery is <50%
    - developing: puzzles tied to topics where student mastery is between 50% and 79%
    """
    query = db.query(Puzzle).filter(Puzzle.is_active == True)
    if subject_id:
        query = query.filter(Puzzle.subject_id == subject_id)
    if lesson_id:
        query = query.filter(Puzzle.lesson_id == lesson_id)
    if topic_id:
        query = query.filter(Puzzle.topic_id == topic_id)

    puzzles = query.order_by(Puzzle.subject_id.asc(), Puzzle.lesson_id.asc(), Puzzle.display_order.asc()).all()

    # Apply learning state filters
    solved_ids = set(
        pa.puzzle_id for pa in db.query(PuzzleAttempt.puzzle_id).filter(
            PuzzleAttempt.student_id == student.id,
            PuzzleAttempt.is_correct == True
        ).all()
    )

    if filter == "unsolved":
        puzzles = [p for p in puzzles if p.id not in solved_ids]
    elif filter == "completed":
        puzzles = [p for p in puzzles if p.id in solved_ids]
    elif filter in ["weak", "developing"]:
        # Find topics in this state
        perfs = db.query(StudentTopicPerformance).filter(
            StudentTopicPerformance.student_id == student.id
        ).all()
        target_topic_ids = set()
        for p in perfs:
            if filter == "weak" and (p.mastery_score < 50.0 or p.accuracy < 50.0):
                target_topic_ids.add(p.topic_id)
            elif filter == "developing" and (50.0 <= p.mastery_score < 80.0):
                target_topic_ids.add(p.topic_id)
        puzzles = [p for p in puzzles if p.topic_id in target_topic_ids or (p.lesson and p.lesson.topic_id in target_topic_ids)]

    return [format_puzzle_out(p, student_id=student.id, db=db) for p in puzzles]

@router.get("/puzzles/recommended", response_model=Optional[PuzzleOut])
def get_recommended_puzzle(
    student: StudentProfile = Depends(get_current_student),
    db: Session = Depends(get_db)
):
    """
    Smart next challenge recommendation engine:
    1. Identifies weak topics (<50% mastery) and returns an unsolved puzzle.
    2. Identifies developing topics (50-79% mastery) and returns an unsolved puzzle.
    3. Identifies the student's active in-progress lesson and returns an unsolved puzzle.
    4. Falls back to the earliest unsolved puzzle in enrolled curriculum.
    """
    solved_ids = set(
        pa.puzzle_id for pa in db.query(PuzzleAttempt.puzzle_id).filter(
            PuzzleAttempt.student_id == student.id,
            PuzzleAttempt.is_correct == True
        ).all()
    )

    # 1. Weak topics (<50% mastery)
    weak_perfs = (
        db.query(StudentTopicPerformance)
        .filter(StudentTopicPerformance.student_id == student.id, StudentTopicPerformance.mastery_score < 50.0)
        .order_by(StudentTopicPerformance.mastery_score.asc())
        .all()
    )
    for wp in weak_perfs:
        cand = db.query(Puzzle).filter(
            Puzzle.topic_id == wp.topic_id,
            Puzzle.is_active == True,
            Puzzle.id.notin_(solved_ids) if solved_ids else True
        ).first()
        if cand:
            return format_puzzle_out(cand, student_id=student.id, db=db)

    # 2. Developing topics (50-79% mastery)
    dev_perfs = (
        db.query(StudentTopicPerformance)
        .filter(StudentTopicPerformance.student_id == student.id, StudentTopicPerformance.mastery_score >= 50.0, StudentTopicPerformance.mastery_score < 80.0)
        .order_by(StudentTopicPerformance.mastery_score.asc())
        .all()
    )
    for dp in dev_perfs:
        cand = db.query(Puzzle).filter(
            Puzzle.topic_id == dp.topic_id,
            Puzzle.is_active == True,
            Puzzle.id.notin_(solved_ids) if solved_ids else True
        ).first()
        if cand:
            return format_puzzle_out(cand, student_id=student.id, db=db)

    # 3. Active in-progress lesson
    active_prog = (
        db.query(LessonProgress)
        .filter(LessonProgress.student_id == student.id, LessonProgress.status == "IN_PROGRESS")
        .order_by(LessonProgress.last_accessed.desc())
        .first()
    )
    if active_prog:
        cand = db.query(Puzzle).filter(
            Puzzle.lesson_id == active_prog.lesson_id,
            Puzzle.is_active == True,
            Puzzle.id.notin_(solved_ids) if solved_ids else True
        ).first()
        if cand:
            return format_puzzle_out(cand, student_id=student.id, db=db)

    # 4. First unsolved puzzle in Subject 12 or 3
    cand = db.query(Puzzle).filter(
        Puzzle.subject_id.in_([12, 3]),
        Puzzle.is_active == True,
        Puzzle.id.notin_(solved_ids) if solved_ids else True
    ).first()
    if cand:
        return format_puzzle_out(cand, student_id=student.id, db=db)

    # 5. Any unsolved puzzle
    cand = db.query(Puzzle).filter(
        Puzzle.is_active == True,
        Puzzle.id.notin_(solved_ids) if solved_ids else True
    ).first()
    if cand:
        return format_puzzle_out(cand, student_id=student.id, db=db)

    # Fallback to any puzzle
    first_p = db.query(Puzzle).filter(Puzzle.is_active == True).first()
    return format_puzzle_out(first_p, student_id=student.id, db=db) if first_p else None

@router.get("/lessons/{lesson_id}/puzzles", response_model=List[PuzzleOut])
def get_lesson_puzzles(
    lesson_id: int,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user)
):
    """Retrieve all interactive puzzles for a specific lesson."""
    lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")

    student_id = None
    if current_user and current_user.role == "STUDENT":
        profile = db.query(StudentProfile).filter(StudentProfile.user_id == current_user.id).first()
        if profile:
            student_id = profile.id

    puzzles = db.query(Puzzle).filter(
        Puzzle.lesson_id == lesson_id,
        Puzzle.is_active == True
    ).order_by(Puzzle.display_order.asc(), Puzzle.id.asc()).all()

    return [format_puzzle_out(p, student_id=student_id, db=db) for p in puzzles]

@router.get("/puzzles/{puzzle_id}", response_model=PuzzleOut)
def get_puzzle(
    puzzle_id: int,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user)
):
    """Get a single puzzle by ID. Strips correct_answer for students."""
    puzzle = db.query(Puzzle).filter(Puzzle.id == puzzle_id).first()
    if not puzzle:
        raise HTTPException(status_code=404, detail="Puzzle not found")

    student_id = None
    if current_user and current_user.role == "STUDENT":
        profile = db.query(StudentProfile).filter(StudentProfile.user_id == current_user.id).first()
        if profile:
            student_id = profile.id

    return format_puzzle_out(puzzle, student_id=student_id, db=db)

@router.post("/puzzles/{puzzle_id}/submit", response_model=PuzzleSubmissionResult)
def submit_puzzle(
    puzzle_id: int,
    submission: PuzzleSubmission,
    student: StudentProfile = Depends(get_current_student),
    db: Session = Depends(get_db)
):
    """
    Submits student's solution for a puzzle:
    - Answer checked securely on server
    - Awards +10 XP on first correct attempt
    - Updates lesson progress
    - Detects struggle and triggers recommendations
    """
    return submit_puzzle_solution(
        db=db,
        puzzle_id=puzzle_id,
        student_id=student.id,
        submitted_answer=submission.submitted_answer,
        time_taken=submission.time_taken
    )

@router.get("/students/me/puzzle-progress", response_model=StudentPuzzleProgressOut)
def get_student_puzzle_progress(
    student: StudentProfile = Depends(get_current_student),
    db: Session = Depends(get_db)
):
    """Retrieve gamified puzzle progress, total solved, accuracy, topics strengthened, and recent attempts."""
    total_puzzles = db.query(Puzzle).filter(Puzzle.is_active == True).count()
    attempts = db.query(PuzzleAttempt).filter(PuzzleAttempt.student_id == student.id).order_by(PuzzleAttempt.completed_at.desc()).all()
    
    unique_solved_ids = set()
    total_xp = 0
    correct_count = 0
    recent = []

    # Track topics strengthened (distinct topics with at least one correct puzzle)
    strengthened_topics = set()

    for a in attempts:
        total_xp += (a.xp_earned or 0)
        if a.is_correct:
            correct_count += 1
            unique_solved_ids.add(a.puzzle_id)
            p_obj = db.query(Puzzle).filter(Puzzle.id == a.puzzle_id).first()
            if p_obj and p_obj.topic_id:
                strengthened_topics.add(p_obj.topic_id)

    total_attempts = len(attempts)
    accuracy = round((correct_count / total_attempts * 100.0), 1) if total_attempts > 0 else 0.0

    for a in attempts[:10]:
        p = db.query(Puzzle).filter(Puzzle.id == a.puzzle_id).first()
        recent.append(
            PuzzleAttemptSummary(
                puzzle_id=a.puzzle_id,
                puzzle_title=p.title if p else "Puzzle",
                is_correct=a.is_correct,
                attempts_count=a.attempts_count,
                xp_earned=a.xp_earned,
                completed_at=a.completed_at
            )
        )

    return StudentPuzzleProgressOut(
        total_solved=len(unique_solved_ids),
        total_puzzles=total_puzzles,
        total_xp=total_xp,
        accuracy=accuracy,
        topics_strengthened=len(strengthened_topics),
        total_attempts=total_attempts,
        recent_attempts=recent
    )

# Admin Endpoints
@router.get("/admin/puzzles", response_model=List[PuzzleAdminOut])
def admin_list_puzzles(
    lesson_id: Optional[int] = Query(None),
    subject_id: Optional[int] = Query(None),
    admin: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Admin lists all puzzles with optional lesson or subject filtering."""
    query = db.query(Puzzle)
    if lesson_id:
        query = query.filter(Puzzle.lesson_id == lesson_id)
    if subject_id:
        query = query.filter(Puzzle.subject_id == subject_id)
    puzzles = query.order_by(Puzzle.lesson_id.asc(), Puzzle.display_order.asc()).all()

    outs = []
    for p in puzzles:
        try:
            p_data = json.loads(p.puzzle_data)
        except Exception:
            p_data = p.puzzle_data
        try:
            c_ans = json.loads(p.correct_answer)
        except Exception:
            c_ans = p.correct_answer
        outs.append(
            PuzzleAdminOut(
                id=p.id,
                subject_id=p.subject_id,
                lesson_id=p.lesson_id,
                topic_id=p.topic_id,
                title=p.title,
                description=p.description,
                puzzle_type=p.puzzle_type,
                question=p.question,
                puzzle_data=p_data,
                correct_answer=c_ans,
                explanation=p.explanation,
                difficulty=p.difficulty,
                xp_reward=p.xp_reward,
                display_order=p.display_order,
                is_active=p.is_active,
                created_at=p.created_at,
                updated_at=p.updated_at
            )
        )
    return outs

@router.post("/admin/puzzles", response_model=PuzzleAdminOut, status_code=status.HTTP_201_CREATED)
def admin_create_puzzle(
    puzzle_in: PuzzleCreate,
    admin: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Admin creates a new puzzle with full solution."""
    p_data_str = json.dumps(puzzle_in.puzzle_data) if not isinstance(puzzle_in.puzzle_data, str) else puzzle_in.puzzle_data
    c_ans_str = json.dumps(puzzle_in.correct_answer) if not isinstance(puzzle_in.correct_answer, str) else puzzle_in.correct_answer

    puzzle = Puzzle(
        subject_id=puzzle_in.subject_id,
        lesson_id=puzzle_in.lesson_id,
        topic_id=puzzle_in.topic_id,
        title=puzzle_in.title,
        description=puzzle_in.description,
        puzzle_type=puzzle_in.puzzle_type,
        question=puzzle_in.question,
        puzzle_data=p_data_str,
        correct_answer=c_ans_str,
        explanation=puzzle_in.explanation,
        difficulty=puzzle_in.difficulty,
        xp_reward=puzzle_in.xp_reward,
        display_order=puzzle_in.display_order,
        is_active=puzzle_in.is_active
    )
    db.add(puzzle)
    db.commit()
    db.refresh(puzzle)

    return PuzzleAdminOut(
        id=puzzle.id,
        subject_id=puzzle.subject_id,
        lesson_id=puzzle.lesson_id,
        topic_id=puzzle.topic_id,
        title=puzzle.title,
        description=puzzle.description,
        puzzle_type=puzzle.puzzle_type,
        question=puzzle.question,
        puzzle_data=puzzle_in.puzzle_data,
        correct_answer=puzzle_in.correct_answer,
        explanation=puzzle.explanation,
        difficulty=puzzle.difficulty,
        xp_reward=puzzle.xp_reward,
        display_order=puzzle.display_order,
        is_active=puzzle.is_active,
        created_at=puzzle.created_at,
        updated_at=puzzle.updated_at
    )

@router.patch("/admin/puzzles/{puzzle_id}", response_model=PuzzleAdminOut)
def admin_update_puzzle(
    puzzle_id: int,
    puzzle_in: PuzzleUpdate,
    admin: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Admin updates an existing puzzle."""
    puzzle = db.query(Puzzle).filter(Puzzle.id == puzzle_id).first()
    if not puzzle:
        raise HTTPException(status_code=404, detail="Puzzle not found")

    update_data = puzzle_in.model_dump(exclude_unset=True)
    for field, val in update_data.items():
        if field in ["puzzle_data", "correct_answer"] and val is not None:
            val = json.dumps(val) if not isinstance(val, str) else val
        setattr(puzzle, field, val)

    db.commit()
    db.refresh(puzzle)

    try:
        p_data = json.loads(puzzle.puzzle_data)
    except Exception:
        p_data = puzzle.puzzle_data

    try:
        c_ans = json.loads(puzzle.correct_answer)
    except Exception:
        c_ans = puzzle.correct_answer

    return PuzzleAdminOut(
        id=puzzle.id,
        subject_id=puzzle.subject_id,
        lesson_id=puzzle.lesson_id,
        topic_id=puzzle.topic_id,
        title=puzzle.title,
        description=puzzle.description,
        puzzle_type=puzzle.puzzle_type,
        question=puzzle.question,
        puzzle_data=p_data,
        correct_answer=c_ans,
        explanation=puzzle.explanation,
        difficulty=puzzle.difficulty,
        xp_reward=puzzle.xp_reward,
        display_order=puzzle.display_order,
        is_active=puzzle.is_active,
        created_at=puzzle.created_at,
        updated_at=puzzle.updated_at
    )

@router.delete("/admin/puzzles/{puzzle_id}")
def admin_delete_puzzle(
    puzzle_id: int,
    admin: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Admin deletes a puzzle."""
    puzzle = db.query(Puzzle).filter(Puzzle.id == puzzle_id).first()
    if not puzzle:
        raise HTTPException(status_code=404, detail="Puzzle not found")

    db.delete(puzzle)
    db.commit()
    return {"message": f"Puzzle {puzzle_id} deleted successfully"}
