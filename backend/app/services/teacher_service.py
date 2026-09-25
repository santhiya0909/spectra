from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.db.models.user import User, StudentProfile
from app.db.models.academic import Topic, Subject, LessonProgress
from app.db.models.quiz import QuizAttempt, Quiz
from app.db.models.performance import StudentTopicPerformance
from app.db.models.teacher import TeacherAlert
from app.db.models.recommendation import Recommendation
from app.schemas.teacher import TeacherDashboardOut, TeacherAlertOut, TopicGapOut, StudentSummaryOut

def get_teacher_dashboard(db: Session) -> TeacherDashboardOut:
    """Calculates real class-wide metrics, at-risk alerts, and topic gaps across all enrolled students."""
    students = db.query(StudentProfile).all()
    total_students = len(students)

    # Class average performance across all attempts
    avg_perf_row = db.query(func.avg(QuizAttempt.percentage)).scalar()
    avg_performance = round(float(avg_perf_row), 1) if avg_perf_row is not None else 0.0

    # Completion rate
    total_progress_items = db.query(LessonProgress).count()
    completed_progress_items = db.query(LessonProgress).filter(LessonProgress.status == "COMPLETED").count()
    completion_rate = round((completed_progress_items / total_progress_items * 100.0), 1) if total_progress_items > 0 else 0.0

    # Active alerts
    alerts = db.query(TeacherAlert).order_by(TeacherAlert.created_at.desc()).limit(15).all()
    alert_outs = []
    at_risk_student_ids = set()

    for a in alerts:
        stu = db.query(StudentProfile).filter(StudentProfile.id == a.student_id).first()
        stu_user = db.query(User).filter(User.id == stu.user_id).first() if stu else None
        top = db.query(Topic).filter(Topic.id == a.topic_id).first()
        
        if a.status == "ACTIVE" and a.severity in ["HIGH", "MEDIUM"]:
            at_risk_student_ids.add(a.student_id)

        alert_outs.append(
            TeacherAlertOut(
                id=a.id,
                student_id=a.student_id,
                student_name=stu_user.name if stu_user else "Student",
                topic_id=a.topic_id,
                topic_name=top.name if top else "Topic",
                alert_type=a.alert_type,
                severity=a.severity,
                message=a.message,
                status=a.status,
                created_at=a.created_at
            )
        )

    # Topic Gaps across all students
    topics = db.query(Topic).all()
    topic_gaps = []
    for t in topics:
        perfs = db.query(StudentTopicPerformance).filter(StudentTopicPerformance.topic_id == t.id).all()
        if perfs:
            avg_acc = sum(p.accuracy for p in perfs) / len(perfs)
            interventions = sum(1 for p in perfs if p.accuracy < 60.0 or p.mastery_score < 60.0)
            topic_gaps.append(
                TopicGapOut(
                    topic_id=t.id,
                    topic_name=t.name,
                    subject_name=t.subject.name if t.subject else "General",
                    class_average_accuracy=round(avg_acc, 1),
                    total_students_assessed=len(perfs),
                    students_needing_intervention=interventions,
                    difficulty=t.difficulty_level
                )
            )

    return TeacherDashboardOut(
        total_students=total_students,
        average_class_performance=avg_performance,
        completion_rate=completion_rate,
        students_needing_attention=len(at_risk_student_ids),
        recent_alerts=alert_outs,
        topic_gaps=sorted(topic_gaps, key=lambda x: x.class_average_accuracy)
    )

def get_all_students_summary(db: Session) -> List[StudentSummaryOut]:
    """Retrieves roster of students with performance indicators and risk status."""
    students = db.query(StudentProfile).all()
    roster = []

    for s in students:
        u = db.query(User).filter(User.id == s.user_id).first()
        if not u:
            continue

        attempts = db.query(QuizAttempt).filter(QuizAttempt.student_id == s.id).all()
        avg_score = round(sum(a.percentage for a in attempts) / len(attempts), 1) if attempts else 0.0

        perfs = db.query(StudentTopicPerformance).filter(StudentTopicPerformance.student_id == s.id).all()
        weak_count = sum(1 for p in perfs if p.mastery_score < 60.0 or p.accuracy < 60.0)

        active_alerts = db.query(TeacherAlert).filter(
            TeacherAlert.student_id == s.id,
            TeacherAlert.status == "ACTIVE",
            TeacherAlert.severity.in_(["HIGH", "MEDIUM"])
        ).count()

        roster.append(
            StudentSummaryOut(
                id=u.id,
                student_profile_id=s.id,
                name=u.name,
                email=u.email,
                student_id=s.student_id,
                department=s.department,
                average_score=avg_score,
                quizzes_completed=len(attempts),
                weak_topics_count=weak_count,
                at_risk=(weak_count > 0 or active_alerts > 0)
            )
        )
    return roster

def get_student_detail_for_teacher(db: Session, student_id: int) -> Dict[str, Any]:
    """Deep-dive student analytics for teacher inspection."""
    student = db.query(StudentProfile).filter(StudentProfile.id == student_id).first()
    if not student:
        # Check by user_id if needed
        student = db.query(StudentProfile).filter(StudentProfile.user_id == student_id).first()
        if not student:
            return {}

    user = db.query(User).filter(User.id == student.user_id).first()
    attempts = db.query(QuizAttempt).filter(QuizAttempt.student_id == student.id).order_by(QuizAttempt.started_at.desc()).all()
    performances = db.query(StudentTopicPerformance).filter(StudentTopicPerformance.student_id == student.id).all()
    recommendations = db.query(Recommendation).filter(Recommendation.student_id == student.id).all()
    alerts = db.query(TeacherAlert).filter(TeacherAlert.student_id == student.id).all()

    perf_list = []
    for p in performances:
        topic = db.query(Topic).filter(Topic.id == p.topic_id).first()
        perf_list.append({
            "topic_id": p.topic_id,
            "topic_name": topic.name if topic else "Topic",
            "accuracy": p.accuracy,
            "mastery_score": p.mastery_score,
            "attempts": p.attempts,
            "status": "WEAK" if p.mastery_score < 60 else ("NEEDS_PRACTICE" if p.mastery_score < 75 else "MASTERED")
        })

    attempts_list = []
    for a in attempts:
        quiz = db.query(Quiz).filter(Quiz.id == a.quiz_id).first()
        attempts_list.append({
            "attempt_id": a.id,
            "quiz_title": quiz.title if quiz else "Quiz",
            "percentage": a.percentage,
            "completed_at": a.completed_at
        })

    return {
        "student": {
            "id": user.id if user else 0,
            "name": user.name if user else "Student",
            "email": user.email if user else "",
            "student_id": student.student_id,
            "department": student.department,
            "semester": student.semester
        },
        "topic_performances": perf_list,
        "recent_attempts": attempts_list,
        "recommendations": [{"id": r.id, "title": r.title, "reason": r.reason, "priority": r.priority} for r in recommendations],
        "alerts": [{"id": al.id, "type": al.alert_type, "message": al.message, "severity": al.severity, "status": al.status} for al in alerts]
    }
