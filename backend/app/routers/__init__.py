from app.routers.auth import router as auth_router
from app.routers.student import router as student_router
from app.routers.subjects import router as subjects_router
from app.routers.lessons import router as lessons_router
from app.routers.quizzes import router as quizzes_router
from app.routers.performance import router as performance_router
from app.routers.recommendations import router as recommendations_router
from app.routers.ai import router as ai_router
from app.routers.teacher import router as teacher_router
from app.routers.admin import router as admin_router
from app.routers.health import router as health_router

__all__ = [
    "auth_router",
    "student_router",
    "subjects_router",
    "lessons_router",
    "quizzes_router",
    "performance_router",
    "recommendations_router",
    "ai_router",
    "teacher_router",
    "admin_router",
    "health_router",
]
