from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.core.config import settings
from app.db.database import create_tables

from app.routers import (
    auth_router,
    student_router,
    subjects_router,
    lessons_router,
    quizzes_router,
    performance_router,
    recommendations_router,
    ai_router,
    teacher_router,
    admin_router,
    health_router,
    puzzles_router,
    knowledge_dna_router,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Ensure database schema is ready on startup
    create_tables()
    yield


app = FastAPI(
    title=settings.PROJECT_NAME,
    description=(
        "SPECTRA is an Intelligent Educational System that analyzes "
        "student learning performance and continuously personalizes "
        "the student's next learning activity through an adaptive "
        "knowledge-gap detection and recommendation loop."
    ),
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan,
)


# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_origin_regex=r"^https?://(localhost|127\.0\.0\.1)(:\d+)?$",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Exception handler for friendly JSON errors
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    import traceback

    print(
        f"[Error] Unhandled exception at "
        f"{request.method} {request.url.path}: {exc}"
    )

    traceback.print_exc()

    origin = request.headers.get("origin")

    headers = {}

    if origin:
        headers["Access-Control-Allow-Origin"] = origin
        headers["Access-Control-Allow-Credentials"] = "true"

    return JSONResponse(
        status_code=500,
        content={
            "detail": "An internal server error occurred. Please try again later."
        },
        headers=headers,
    )


# API prefix
api_prefix = settings.API_V1_STR


# Include API routers
app.include_router(auth_router, prefix=api_prefix)
app.include_router(student_router, prefix=api_prefix)
app.include_router(subjects_router, prefix=api_prefix)
app.include_router(lessons_router, prefix=api_prefix)
app.include_router(quizzes_router, prefix=api_prefix)
app.include_router(performance_router, prefix=api_prefix)
app.include_router(recommendations_router, prefix=api_prefix)
app.include_router(ai_router, prefix=api_prefix)
app.include_router(teacher_router, prefix=api_prefix)
app.include_router(admin_router, prefix=api_prefix)
app.include_router(puzzles_router, prefix=api_prefix)
app.include_router(knowledge_dna_router, prefix=api_prefix)
app.include_router(health_router, prefix=api_prefix)


# Root-level health endpoint
app.include_router(health_router)


@app.get("/")
def root():
    return {
        "system": settings.PROJECT_NAME,
        "status": "online",
        "documentation": "/docs",
        "health": "/health",
    }