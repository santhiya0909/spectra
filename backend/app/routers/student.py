from typing import List, Dict, Any, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.db.database import get_db
from app.core.dependencies import get_current_user, get_current_student
from app.db.models.user import User, StudentProfile
from app.db.models.academic import Subject, Topic, Lesson, LessonProgress, Enrollment
from app.db.models.quiz import QuizAttempt, Quiz
from app.db.models.performance import StudentTopicPerformance
from app.db.models.recommendation import Recommendation, LearningPlan, LearningPlanItem
from app.schemas.auth import StudentProfileOut
from app.schemas.recommendation import RecommendationOut, LearningPlanOut, LearningPlanItemOut

router = APIRouter(prefix="/students", tags=["Student"])

@router.get("/me", response_model=StudentProfileOut)
def get_student_profile(student: StudentProfile = Depends(get_current_student)):
    """Fetch current student's academic profile."""
    return student

@router.get("/me/dashboard")
def get_student_dashboard(
    student: StudentProfile = Depends(get_current_student),
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Returns complete student dashboard data:
    Greeting, Today's learning plan, Overall progress, Average quiz score,
    Lessons completed, Current streak, Subject progress, Weak topics,
    Recommended next activity, Recent quiz results, Upcoming activities.
    """
    # 1. Quizzes & Attempts
    attempts = (
        db.query(QuizAttempt)
        .filter(QuizAttempt.student_id == student.id)
        .order_by(QuizAttempt.started_at.desc())
        .all()
    )
    avg_score = round(sum(a.percentage for a in attempts) / len(attempts), 1) if attempts else 0.0

    recent_results = []
    for a in attempts[:5]:
        quiz = db.query(Quiz).filter(Quiz.id == a.quiz_id).first()
        subj = db.query(Subject).filter(Subject.id == quiz.subject_id).first() if quiz else None
        recent_results.append({
            "attempt_id": a.id,
            "quiz_id": a.quiz_id,
            "quiz_title": quiz.title if quiz else "Quiz",
            "subject_name": subj.name if subj else "General",
            "score": a.score,
            "percentage": a.percentage,
            "completed_at": a.completed_at
        })

    # 2. Lessons & Progress
    completed_lessons = (
        db.query(LessonProgress)
        .filter(LessonProgress.student_id == student.id, LessonProgress.status == "COMPLETED")
        .count()
    )
    total_lessons = db.query(Lesson).count()
    overall_progress = round((completed_lessons / total_lessons * 100.0), 1) if total_lessons > 0 else 0.0

    # 3. Topic Performance & Weak Topics
    topic_perfs = (
        db.query(StudentTopicPerformance)
        .filter(StudentTopicPerformance.student_id == student.id)
        .all()
    )
    weak_topics = []
    for tp in topic_perfs:
        if tp.mastery_score < 60.0 or tp.accuracy < 60.0:
            top = db.query(Topic).filter(Topic.id == tp.topic_id).first()
            weak_topics.append({
                "topic_id": tp.topic_id,
                "topic_name": top.name if top else "Topic",
                "accuracy": tp.accuracy,
                "mastery_score": tp.mastery_score,
                "status": "WEAK"
            })

    # 4. Active Recommendations & Next Activity
    recommendations = (
        db.query(Recommendation)
        .filter(Recommendation.student_id == student.id, Recommendation.status == "ACTIVE")
        .order_by(Recommendation.priority.desc(), Recommendation.created_at.desc())
        .all()
    )
    rec_list = []
    for r in recommendations:
        top = db.query(Topic).filter(Topic.id == r.topic_id).first()
        subj = top.subject if top else None
        rec_list.append({
            "id": r.id,
            "topic_id": r.topic_id,
            "topic_name": top.name if top else "Topic",
            "subject_name": subj.name if subj else "General",
            "recommendation_type": r.recommendation_type,
            "title": r.title,
            "reason": r.reason,
            "priority": r.priority,
            "resource_id": r.resource_id,
            "status": r.status,
            "created_at": r.created_at
        })

    recommended_next_activity = rec_list[0] if rec_list else {
        "title": "Start Java Functions Diagnostic",
        "reason": "Complete your baseline assessment to unlock personalized recommendations.",
        "priority": "HIGH",
        "resource_id": 1,
        "recommendation_type": "ASSESSMENT"
    }

    # 5. Subject Progress
    subjects = db.query(Subject).all()
    subject_progress = []
    for s in subjects:
        subj_lessons = db.query(Lesson).filter(Lesson.subject_id == s.id).all()
        subj_lesson_ids = [l.id for l in subj_lessons]
        done = db.query(LessonProgress).filter(
            LessonProgress.student_id == student.id,
            LessonProgress.lesson_id.in_(subj_lesson_ids),
            LessonProgress.status == "COMPLETED"
        ).count() if subj_lesson_ids else 0
        pct = round((done / len(subj_lessons) * 100.0), 1) if subj_lessons else 0.0
        subject_progress.append({
            "subject_id": s.id,
            "subject_name": s.name,
            "code": s.code,
            "completed_lessons": done,
            "total_lessons": len(subj_lessons),
            "percentage": pct
        })

    # 6. Today's Learning Plan
    learning_plan = db.query(LearningPlan).filter(
        LearningPlan.student_id == student.id,
        LearningPlan.active == True
    ).first()
    plan_items = []
    if learning_plan:
        for item in learning_plan.items:
            title = "Resource Item"
            desc = ""
            if item.resource_type == "LESSON":
                les = db.query(Lesson).filter(Lesson.id == item.resource_id).first()
                if les:
                    title = f"Lesson: {les.title}"
                    desc = f"{les.estimated_minutes} min read"
            elif item.resource_type == "QUIZ":
                qz = db.query(Quiz).filter(Quiz.id == item.resource_id).first()
                if qz:
                    title = f"Quiz: {qz.title}"
                    desc = f"{qz.question_count} questions"

            plan_items.append({
                "id": item.id,
                "resource_type": item.resource_type,
                "resource_id": item.resource_id,
                "title": title,
                "description": desc,
                "order_index": item.order_index,
                "completed": item.completed
            })

    # 7. Continue Learning Card
    from app.db.models.puzzle import Puzzle, PuzzleAttempt
    active_prog = (
        db.query(LessonProgress)
        .filter(LessonProgress.student_id == student.id, LessonProgress.status == "IN_PROGRESS")
        .order_by(LessonProgress.completion_percentage.desc())
        .first()
    )
    if active_prog:
        active_lesson = db.query(Lesson).filter(Lesson.id == active_prog.lesson_id).first()
        active_subj = db.query(Subject).filter(Subject.id == active_lesson.subject_id).first() if active_lesson else None
        continue_card = {
            "subject_name": active_subj.name if active_subj else "Java Programming",
            "subject_code": active_subj.code if active_subj else "JAVA",
            "lesson_id": active_lesson.id if active_lesson else 1,
            "lesson_title": active_lesson.title if active_lesson else "Functions & Methods",
            "progress": active_prog.completion_percentage,
            "progress_percentage": round(active_prog.completion_percentage, 1),
            "lesson_order": active_lesson.lesson_order if active_lesson else 1,
            "next_action": f"Continue Lesson {active_lesson.lesson_order if active_lesson else 1}"
        }
    else:
        first_lesson = db.query(Lesson).order_by(Lesson.id.asc()).first()
        first_subj = db.query(Subject).filter(Subject.id == first_lesson.subject_id).first() if first_lesson else None
        continue_card = {
            "subject_name": first_subj.name if first_subj else "Java Programming",
            "subject_code": first_subj.code if first_subj else "JAVA",
            "lesson_id": first_lesson.id if first_lesson else 1,
            "lesson_title": first_lesson.title if first_lesson else "Functions & Methods",
            "progress": 65.0,
            "progress_percentage": 65.0,
            "lesson_order": first_lesson.lesson_order if first_lesson else 1,
            "next_action": "Begin your first adaptive module"
        }

    # 8. Today's Learning Path
    next_les_id = min(total_lessons, continue_card["lesson_id"] + 1)
    today_learning_path = [
        {
            "id": 1,
            "step": 1,
            "title": "Review Java Functions",
            "type": "LESSON",
            "resource_id": continue_card["lesson_id"],
            "completed": True,
            "status": "COMPLETED",
            "xp_reward": 50,
            "duration_minutes": 15,
            "url": f"/student/lessons/{continue_card['lesson_id']}",
            "is_current": False,
        },
        {
            "id": 2,
            "step": 2,
            "title": "Solve Function Puzzle",
            "type": "PUZZLE",
            "resource_id": continue_card["lesson_id"],
            "completed": False,
            "status": "IN_PROGRESS",
            "xp_reward": 75,
            "duration_minutes": 10,
            "url": "/student/progress",
            "is_current": True,
        },
        {
            "id": 3,
            "step": 3,
            "title": "Complete Functions Quiz",
            "type": "QUIZ",
            "resource_id": continue_card["lesson_id"],
            "completed": False,
            "status": "NOT_STARTED",
            "xp_reward": 100,
            "duration_minutes": 20,
            "url": f"/student/quizzes/{continue_card['lesson_id']}",
            "is_current": False,
        },
        {
            "id": 4,
            "step": 4,
            "title": "Study Arrays",
            "type": "LESSON",
            "resource_id": next_les_id,
            "completed": False,
            "status": "NOT_STARTED",
            "xp_reward": 50,
            "duration_minutes": 15,
            "url": f"/student/lessons/{next_les_id}",
            "is_current": False,
        },
        {
            "id": 5,
            "step": 5,
            "title": "Practice Arrays Quiz",
            "type": "QUIZ",
            "resource_id": next_les_id,
            "completed": False,
            "status": "NOT_STARTED",
            "xp_reward": 100,
            "duration_minutes": 20,
            "url": f"/student/quizzes/{next_les_id}",
            "is_current": False,
        },
    ]

    # 9. Puzzles Solved & Topics Mastered
    puzzles_solved = (
        db.query(PuzzleAttempt.puzzle_id)
        .filter(PuzzleAttempt.student_id == student.id, PuzzleAttempt.is_correct == True)
        .distinct()
        .count()
    )
    topics_mastered = (
        db.query(StudentTopicPerformance)
        .filter(StudentTopicPerformance.student_id == student.id, StudentTopicPerformance.mastery_score >= 80.0)
        .count()
    )

    # 10. Achievements
    streak_val = student.current_streak or 4
    xp_val = student.xp if (student.xp and student.xp > 0) else 145
    achievements = [
        {"id": "java_explorer", "title": "Java Explorer", "icon": "Compass", "description": "Completed first Java fundamentals", "unlocked": True, "date": "2 days ago"},
        {"id": "functions_mastery", "title": "Functions Mastery", "icon": "Award", "description": "Scored 90%+ on Java Methods assessment", "unlocked": True, "date": "Yesterday"},
        {"id": "streak_master", "title": f"{streak_val}-Day Streak", "icon": "Flame", "description": f"Maintained a {streak_val} day active study consistency", "unlocked": True, "date": "Today"},
        {"id": "puzzle_ace", "title": "Puzzle Solver", "icon": "Zap", "description": f"Successfully completed {puzzles_solved} interactive puzzles", "unlocked": puzzles_solved > 0, "date": "Today"},
    ]

    first_name = user.name.split()[0] if user.name else "Alex"

    return {
        "greeting": f"Good morning, {first_name} 👋",
        "subtitle": "Continue your personalized learning journey.",
        "student": {
            "name": user.name,
            "student_id": student.student_id,
            "department": student.department,
            "semester": student.semester
        },
        "overall_progress": overall_progress,
        "average_quiz_score": avg_score,
        "lessons_completed": completed_lessons,
        "total_lessons": total_lessons,
        "current_streak": streak_val,
        "xp": xp_val,
        "puzzles_solved": puzzles_solved,
        "topics_mastered": topics_mastered,
        "continue_learning_card": continue_card,
        "today_learning_path": today_learning_path,
        "recent_achievements": achievements,
        "weak_topics": weak_topics,
        "recommended_next_activity": recommended_next_activity,
        "recent_quiz_results": recent_results,
        "subject_progress": subject_progress,
        "today_learning_plan": plan_items if plan_items else today_learning_path,
        "active_recommendations": rec_list
    }

@router.get("/me/recommendations", response_model=List[RecommendationOut])
def get_student_recommendations(
    student: StudentProfile = Depends(get_current_student),
    db: Session = Depends(get_db)
):
    """Retrieve personalized recommendations for the student."""
    recs = (
        db.query(Recommendation)
        .filter(Recommendation.student_id == student.id, Recommendation.status == "ACTIVE")
        .order_by(Recommendation.priority.desc(), Recommendation.created_at.desc())
        .all()
    )
    result = []
    for r in recs:
        top = db.query(Topic).filter(Topic.id == r.topic_id).first()
        subj = top.subject if top else None
        result.append(
            RecommendationOut(
                id=r.id,
                topic_id=r.topic_id,
                topic_name=top.name if top else "Topic",
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
    return result

@router.get("/me/learning-plan")
def get_student_learning_plan(
    student: StudentProfile = Depends(get_current_student),
    db: Session = Depends(get_db)
):
    """Fetch active adaptive learning plan."""
    plan = db.query(LearningPlan).filter(
        LearningPlan.student_id == student.id,
        LearningPlan.active == True
    ).first()
    if not plan:
        return {"id": 0, "title": "Self-Paced Plan", "active": True, "items": []}

    items = []
    for it in plan.items:
        title = "Activity"
        desc = ""
        if it.resource_type == "LESSON":
            les = db.query(Lesson).filter(Lesson.id == it.resource_id).first()
            if les:
                title = f"Lesson: {les.title}"
                desc = f"{les.difficulty} difficulty · {les.estimated_minutes} min"
        elif it.resource_type == "QUIZ":
            qz = db.query(Quiz).filter(Quiz.id == it.resource_id).first()
            if qz:
                title = f"Quiz: {qz.title}"
                desc = f"{qz.question_count} practice questions"

        items.append({
            "id": it.id,
            "resource_type": it.resource_type,
            "resource_id": it.resource_id,
            "title": title,
            "description": desc,
            "order_index": it.order_index,
            "completed": it.completed
        })

    return {
        "id": plan.id,
        "title": plan.title,
        "generated_at": plan.generated_at,
        "active": plan.active,
        "items": items
    }
