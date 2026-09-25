from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from app.db.models.user import User, StudentProfile, TeacherProfile, AuditLog
from app.db.models.academic import Subject, Topic, Lesson
from app.db.models.quiz import Question, Quiz
from app.schemas.admin import AdminDashboardOut, AuditLogOut

def get_admin_dashboard_stats(db: Session) -> AdminDashboardOut:
    """Aggregates high-level system usage statistics for platform administration."""
    total_users = db.query(User).count()
    total_students = db.query(StudentProfile).count()
    total_teachers = db.query(TeacherProfile).count()
    total_subjects = db.query(Subject).count()
    total_quizzes = db.query(Quiz).count()
    total_questions = db.query(Question).count()

    recent_logs_db = db.query(AuditLog).order_by(AuditLog.created_at.desc()).limit(20).all()
    logs_out = []
    for l in recent_logs_db:
        user = db.query(User).filter(User.id == l.user_id).first() if l.user_id else None
        logs_out.append(
            AuditLogOut(
                id=l.id,
                user_id=l.user_id,
                user_name=user.name if user else "System",
                action=l.action,
                entity=l.entity,
                entity_id=l.entity_id,
                created_at=l.created_at
            )
        )

    return AdminDashboardOut(
        total_users=total_users,
        total_students=total_students,
        total_teachers=total_teachers,
        total_subjects=total_subjects,
        total_quizzes=total_quizzes,
        total_questions=total_questions,
        recent_logs=logs_out
    )
