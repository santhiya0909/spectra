import json
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.db.models.puzzle import Puzzle, PuzzleAttempt
from app.db.models.academic import Lesson, LessonProgress, Topic
from app.db.models.performance import StudentTopicPerformance
from app.db.models.user import StudentProfile
from app.db.models.recommendation import Recommendation
from app.schemas.puzzle import PuzzleOut, PuzzleSubmissionResult
from app.services.gap_detection_service import update_topic_performance
from app.services.knowledge_dna_service import determine_mastery_state
from app.services.youtube_service import get_or_create_lesson_youtube_recommendations

def normalize_val(val: Any) -> str:
    """Helper to normalize string values for answer checking."""
    if val is None:
        return ""
    if isinstance(val, bool):
        return str(val).lower()
    return str(val).strip().lower()

def check_puzzle_answer(puzzle: Puzzle, submitted_answer: Any) -> bool:
    """
    Evaluates whether the submitted answer matches the puzzle's correct answer.
    Never exposes internal logic to client.
    """
    ptype = puzzle.puzzle_type.upper()
    try:
        correct_data = json.loads(puzzle.correct_answer) if isinstance(puzzle.correct_answer, str) else puzzle.correct_answer
    except Exception:
        correct_data = puzzle.correct_answer

    # Normalize submitted_answer if it was passed as json string
    if isinstance(submitted_answer, str):
        try:
            submitted_json = json.loads(submitted_answer)
            # If successfully decoded into a list or dict, use it
            if isinstance(submitted_json, (dict, list)):
                submitted_answer = submitted_json
        except Exception:
            pass

    if ptype == "MULTIPLE_CHOICE":
        if isinstance(correct_data, list):
            # Could be list of acceptable answers or single choice
            return any(normalize_val(submitted_answer) == normalize_val(c) for c in correct_data)
        return normalize_val(submitted_answer) == normalize_val(correct_data)

    elif ptype == "TRUE_FALSE":
        sub_str = normalize_val(submitted_answer)
        corr_str = normalize_val(correct_data)
        if sub_str in ["true", "t", "1"] and corr_str in ["true", "t", "1"]:
            return True
        if sub_str in ["false", "f", "0"] and corr_str in ["false", "f", "0"]:
            return True
        return False

    elif ptype == "FILL_BLANK":
        sub_str = normalize_val(submitted_answer)
        if isinstance(correct_data, list):
            return any(sub_str == normalize_val(c) for c in correct_data)
        return sub_str == normalize_val(correct_data)

    elif ptype == "CODE_OUTPUT":
        sub_str = str(submitted_answer).strip().replace("\r\n", "\n")
        corr_str = str(correct_data).strip().replace("\r\n", "\n")
        return sub_str == corr_str

    elif ptype == "ORDERING":
        if not isinstance(submitted_answer, list) or not isinstance(correct_data, list):
            return False
        if len(submitted_answer) != len(correct_data):
            return False
        return [str(item).strip() for item in submitted_answer] == [str(item).strip() for item in correct_data]

    elif ptype == "MATCHING":
        # Submitted can be dict or list of [k, v] pairs
        if isinstance(submitted_answer, list):
            sub_dict = {str(k).strip(): str(v).strip() for k, v in submitted_answer if len(k) and len(v)}
        elif isinstance(submitted_answer, dict):
            sub_dict = {str(k).strip(): str(v).strip() for k, v in submitted_answer.items()}
        else:
            return False

        if isinstance(correct_data, list):
            corr_dict = {str(k).strip(): str(v).strip() for k, v in correct_data}
        elif isinstance(correct_data, dict):
            corr_dict = {str(k).strip(): str(v).strip() for k, v in correct_data.items()}
        else:
            return False

        return sub_dict == corr_dict

    # Default fallback equality
    return normalize_val(submitted_answer) == normalize_val(correct_data)


def submit_puzzle_solution(
    db: Session,
    puzzle_id: int,
    student_id: int,
    submitted_answer: Any,
    time_taken: int = 0
) -> PuzzleSubmissionResult:
    """
    Validates submission, updates attempt count, awards XP (no repeated farming),
    updates lesson progress, and checks for knowledge gap recommendations.
    """
    puzzle = db.query(Puzzle).filter(Puzzle.id == puzzle_id).first()
    if not puzzle:
        raise HTTPException(status_code=404, detail="Puzzle not found")

    student = db.query(StudentProfile).filter(StudentProfile.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student profile not found")

    now = datetime.now(timezone.utc)
    # Check prior attempts
    prior_attempts = db.query(PuzzleAttempt).filter(
        PuzzleAttempt.puzzle_id == puzzle_id,
        PuzzleAttempt.student_id == student_id
    ).all()

    already_solved = any(a.is_correct for a in prior_attempts)
    attempts_count = len(prior_attempts) + 1

    is_correct = check_puzzle_answer(puzzle, submitted_answer)
    xp_to_award = 0

    if is_correct:
        if not already_solved:
            # First correct solve -> award XP!
            xp_to_award = puzzle.xp_reward or 10
            student.xp = (student.xp or 0) + xp_to_award
            student.last_active_date = now
    else:
        # Check if student is struggling (2+ failed attempts on this puzzle)
        failed_count = sum(1 for a in prior_attempts if not a.is_correct) + 1
        if failed_count >= 2 and puzzle.topic_id:
            # Ensure targeted recommendation exists
            existing_rec = db.query(Recommendation).filter(
                Recommendation.student_id == student_id,
                Recommendation.topic_id == puzzle.topic_id,
                Recommendation.status == "ACTIVE"
            ).first()
            if not existing_rec:
                topic = db.query(Topic).filter(Topic.id == puzzle.topic_id).first()
                topic_name = topic.name if topic else "concept"
                rec = Recommendation(
                    student_id=student_id,
                    topic_id=puzzle.topic_id,
                    recommendation_type="TARGETED_PRACTICE",
                    title=f"Review {topic_name}",
                    reason=f"You had multiple unsuccessful attempts on the '{puzzle.title}' puzzle.",
                    priority="HIGH",
                    resource_id=puzzle.lesson_id,
                    status="ACTIVE"
                )
                db.add(rec)

    # Record attempt
    attempt = PuzzleAttempt(
        student_id=student_id,
        puzzle_id=puzzle_id,
        submitted_answer=json.dumps(submitted_answer) if not isinstance(submitted_answer, str) else submitted_answer,
        is_correct=is_correct,
        attempts_count=attempts_count,
        xp_earned=xp_to_award,
        completed_at=now,
        time_taken=time_taken
    )
    db.add(attempt)

    # Recalculate Lesson Progress
    prog = db.query(LessonProgress).filter(
        LessonProgress.student_id == student_id,
        LessonProgress.lesson_id == puzzle.lesson_id
    ).first()

    if not prog:
        prog = LessonProgress(
            student_id=student_id,
            lesson_id=puzzle.lesson_id,
            status="IN_PROGRESS",
            completion_percentage=20.0 if is_correct else 10.0,
            puzzles_completed=1 if is_correct else 0
        )
        db.add(prog)
    else:
        if is_correct and not already_solved:
            prog.puzzles_completed = (prog.puzzles_completed or 0) + 1

    # Calculate overall completion percentage for this lesson:
    # Topic Content = 40%, Puzzle = 20%, Practice = 10%, Quiz = 30%
    lesson = db.query(Lesson).filter(Lesson.id == puzzle.lesson_id).first()
    total_lesson_puzzles = db.query(Puzzle).filter(Puzzle.lesson_id == puzzle.lesson_id, Puzzle.is_active == True).count() or 1
    
    # Check how many unique puzzles student has solved for this lesson
    solved_puzzles_count = db.query(PuzzleAttempt.puzzle_id).join(Puzzle).filter(
        Puzzle.lesson_id == puzzle.lesson_id,
        PuzzleAttempt.student_id == student_id,
        PuzzleAttempt.is_correct == True
    ).distinct().count()

    puzzle_pct = min(20.0, (solved_puzzles_count / total_lesson_puzzles) * 20.0)
    topic_pct = 40.0 if (prog.topics_completed and prog.topics_completed > 0) or prog.completion_percentage >= 40.0 else 20.0
    practice_pct = 10.0 if prog.completion_percentage >= 70.0 else 0.0
    quiz_pct = 30.0 if prog.quiz_completed else 0.0

    calculated_pct = min(100.0, round(topic_pct + puzzle_pct + practice_pct + quiz_pct, 1))
    prog.completion_percentage = max(prog.completion_percentage or 0.0, calculated_pct)

    lesson_completed = False
    if prog.completion_percentage >= 95.0 or (prog.quiz_completed and solved_puzzles_count >= total_lesson_puzzles):
        if prog.status != "COMPLETED":
            prog.status = "COMPLETED"
            prog.completed_at = now
            # Award lesson completion XP (+30 XP)
            student.xp = (student.xp or 0) + 30
            prog.xp_earned = (prog.xp_earned or 0) + 30
            lesson_completed = True
    # Identify associated topic
    topic_id = puzzle.topic_id or (lesson.topic_id if lesson else None)
    topic = db.query(Topic).filter(Topic.id == topic_id).first() if topic_id else None
    topic_name = topic.name if topic else (puzzle.title or "this concept")

    # Read topic mastery state before update
    mastery_before = 0.0
    mastery_state_before = "NOT_STARTED"
    if topic_id:
        perf_before = db.query(StudentTopicPerformance).filter(
            StudentTopicPerformance.student_id == student_id,
            StudentTopicPerformance.topic_id == topic_id
        ).order_by(StudentTopicPerformance.last_attempt_at.desc(), StudentTopicPerformance.id.desc()).first()
        if perf_before:
            mastery_before = perf_before.mastery_score
            mastery_state_before = determine_mastery_state(mastery_before, perf_before.attempts, False)

    # Update Student Topic Performance for Knowledge DNA calculation
    mastery_after = mastery_before
    mastery_state_after = mastery_state_before
    if topic_id:
        updated_perf = update_topic_performance(
            db=db,
            student_id=student_id,
            topic_id=topic_id,
            questions_count=1,
            correct_count=1 if is_correct else 0
        )
        mastery_after = updated_perf.mastery_score
        mastery_state_after = determine_mastery_state(mastery_after, updated_perf.attempts, True)

    db.commit()
    db.refresh(prog)

    # Find next puzzle in the same lesson or next lesson
    next_p = db.query(Puzzle).filter(
        Puzzle.lesson_id == puzzle.lesson_id,
        Puzzle.id != puzzle.id,
        Puzzle.display_order >= puzzle.display_order,
        Puzzle.is_active == True
    ).order_by(Puzzle.display_order.asc(), Puzzle.id.asc()).first()
    next_puzzle_id = next_p.id if next_p else None

    next_l = db.query(Lesson).filter(
        Lesson.subject_id == puzzle.subject_id,
        Lesson.lesson_order > (lesson.lesson_order if lesson else 0),
        Lesson.is_active == True
    ).order_by(Lesson.lesson_order.asc()).first() if lesson else None
    next_lesson_id = next_l.id if next_l else None

    # Check for curated YouTube video recommendation if struggling
    recommended_video = None
    if not is_correct and puzzle.lesson_id:
        try:
            yt_res = get_or_create_lesson_youtube_recommendations(db, puzzle.lesson_id)
            if yt_res and yt_res.videos:
                v = yt_res.videos[0]
                recommended_video = {
                    "video_id": v.video_id,
                    "title": v.title,
                    "thumbnail_url": v.thumbnail_url,
                    "channel_name": v.channel_name,
                    "url": v.url
                }
        except Exception:
            pass

    # Determine intelligent SPECTRA feedback and recommended next action
    if is_correct:
        if mastery_after >= 80.0:
            spectra_feedback = f"Outstanding! You demonstrated robust conceptual mastery in {topic_name}. You are fully prepared to advance."
            recommended_action = "NEXT_LESSON" if next_lesson_id else "ANOTHER_PUZZLE"
        else:
            spectra_feedback = f"Great solve! You understood how {topic_name} behaves in practice. Topic mastery climbed from {mastery_before}% to {mastery_after}%."
            recommended_action = "ANOTHER_PUZZLE" if next_puzzle_id else "NEXT_LESSON"
    else:
        if recommended_video:
            spectra_feedback = f"SPECTRA detected a conceptual gap in {topic_name}. Watching a targeted walkthrough will help solidify the foundation."
            recommended_action = "WATCH_VIDEO"
        else:
            spectra_feedback = f"Not quite. Reviewing key concepts in {topic_name} will help cement the pattern and prepare you for subsequent assessments."
            recommended_action = "REVIEW_LESSON"

    hint = None
    if not is_correct:
        hint = puzzle.description or f"Think carefully about how {puzzle.title} works in practice. Try reviewing the lesson concept."

    return PuzzleSubmissionResult(
        is_correct=is_correct,
        xp_earned=xp_to_award,
        explanation=puzzle.explanation if is_correct else None,
        hint=hint,
        attempts_count=attempts_count,
        lesson_progress_percentage=prog.completion_percentage,
        lesson_completed=prog.status == "COMPLETED",
        topic_id=topic_id,
        topic_name=topic_name,
        mastery_before=mastery_before,
        mastery_after=mastery_after,
        mastery_state_before=mastery_state_before,
        mastery_state_after=mastery_state_after,
        spectra_feedback=spectra_feedback,
        recommended_action=recommended_action,
        recommended_video=recommended_video,
        next_puzzle_id=next_puzzle_id,
        next_lesson_id=next_lesson_id
    )
