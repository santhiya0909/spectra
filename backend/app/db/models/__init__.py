from app.db.database import Base
from app.db.models.user import User, StudentProfile, TeacherProfile, AuditLog
from app.db.models.academic import Subject, Topic, Enrollment, Lesson, LessonProgress, StudyResource
from app.db.models.quiz import Question, Quiz, QuizQuestion, QuizAttempt, QuizResponse
from app.db.models.performance import StudentTopicPerformance
from app.db.models.recommendation import Recommendation, LearningPlan, LearningPlanItem
from app.db.models.ai import AIConversation, AIMessage
from app.db.models.teacher import TeacherAlert

__all__ = [
    "Base",
    "User",
    "StudentProfile",
    "TeacherProfile",
    "AuditLog",
    "Subject",
    "Topic",
    "Enrollment",
    "Lesson",
    "LessonProgress",
    "StudyResource",
    "Question",
    "Quiz",
    "QuizQuestion",
    "QuizAttempt",
    "QuizResponse",
    "StudentTopicPerformance",
    "Recommendation",
    "LearningPlan",
    "LearningPlanItem",
    "AIConversation",
    "AIMessage",
    "TeacherAlert"
]

