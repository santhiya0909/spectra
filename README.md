# SPECTRA – Intelligent Educational System

[![Next.js](https://img.shields.io/badge/Frontend-Next.js%2014-black?logo=next.js)](https://nextjs.org/)
[![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688?logo=fastapi)](https://fastapi.tiangolo.com/)
[![PostgreSQL](https://img.shields.io/badge/Database-PostgreSQL-336791?logo=postgresql)](https://www.postgresql.org/)
[![TypeScript](https://img.shields.io/badge/Language-TypeScript-3178C6?logo=typescript)](https://www.typescriptlang.org/)
[![Python](https://img.shields.io/badge/Language-Python%203.11+-3776AB?logo=python)](https://www.python.org/)

SPECTRA is an enterprise-grade intelligent educational system that analyzes student learning performance in real time and continuously personalizes each student's next learning activity through an adaptive knowledge-gap detection and recommendation loop.

---

## The Closed-Loop Learning Engine

```
       ┌───────────┐
       │  ASSESS   │  Diagnostic & Adaptive Quizzes
       └─────┬─────┘
             │
       ┌─────▼─────┐
       │  ANALYZE  │  Evaluate Responses & Calculate Topic Mastery Scores
       └─────┬─────┘
             │
       ┌─────▼─────┐
       │PERSONALIZE│  Rules Engine Detects Knowledge Gaps & Recommends Actions
       └─────┬─────┘
             │
       ┌─────▼─────┐
       │  IMPROVE  │  Targeted Lessons, AI Tutoring & 10 Practice Questions
       └─────┬─────┘
             │
       ┌─────▼─────┐
       │ REASSESS  │  Post-Intervention Adaptive Reassessment
       └─────┬─────┘
             │
       ┌─────▼─────┐
       │UPDATE PATH│  Mastery Status Updates & Unlocks Next Learning Phase
       └───────────┘
```

---

## 1. System Architecture

```
                    ┌─────────────────────────┐
                    │       NEXT.JS APP       │
                    │   (Port 3000 / React)   │
                    │                         │
                    │  Student Experience     │
                    │  Teacher Dashboard      │
                    │  Admin System Console   │
                    │  Adaptive Quiz Engine   │
                    │  Socratic AI Tutor      │
                    └────────────┬────────────┘
                                 │
                           REST API / JSON
                                 │
                    ┌────────────▼────────────┐
                    │         FASTAPI         │
                    │  (Port 8000 / Python)   │
                    │                         │
                    │  Auth & RBAC (JWT)      │
                    │  Knowledge Gap Engine   │
                    │  Rules-Based Rec Engine │
                    │  Quiz Evaluation Engine │
                    │  AI Tutor Service       │
                    └────────────┬────────────┘
                                 │
                          SQLAlchemy ORM
                                 │
                    ┌────────────▼────────────┐
                    │       PostgreSQL        │
                    │  (Port 5432 / Relational)│
                    │                         │
                    │  Users & RBAC Profiles  │
                    │  Curriculum & Lessons   │
                    │  Questions & Attempts   │
                    │  Topic Performances     │
                    │  Adaptive Learning Path │
                    └─────────────────────────┘
```

---

## 2. Technology Stack

- **Frontend**:
  - Framework: Next.js 14 (App Router)
  - UI Library: React 18, Tailwind CSS, Lucide React
  - Visualizations: Recharts
  - Server State: TanStack Query v5
  - Validation: Zod & React Hook Form
- **Backend**:
  - Framework: FastAPI (Python 3.11+)
  - ORM: SQLAlchemy 2.0
  - Migrations: Alembic
  - Data Validation: Pydantic v2
  - Authentication: JWT (python-jose), bcrypt password hashing
  - Database Driver: psycopg2-binary
- **Database**:
  - PostgreSQL 15 (with automated local SQLite fallback for standalone zero-dependency testing)

---

## 3. Project Directory Structure

```
d:/spectra/
├── .env.example                     # Environment template (NO secrets)
├── .gitignore                       # Git ignore covering secrets and dependencies
├── docker-compose.yml               # Multi-container stack (Postgres + Backend + Frontend)
├── README.md                        # Complete system documentation
│
├── backend/
│   ├── alembic.ini                  # Alembic migration configuration
│   ├── Dockerfile                   # Python container definition
│   ├── requirements.txt             # Backend dependencies
│   ├── alembic/                     # Database migrations
│   │   ├── env.py
│   │   └── versions/
│   ├── app/
│   │   ├── main.py                  # FastAPI application entry point
│   │   ├── core/
│   │   │   ├── config.py            # Environment settings & defaults
│   │   │   ├── dependencies.py      # Auth & RBAC dependencies
│   │   │   └── security.py          # Bcrypt hashing & JWT issuance
│   │   ├── db/
│   │   │   ├── database.py          # SQLAlchemy engine & session factory
│   │   │   └── models/              # Normalized relational models
│   │   │       ├── academic.py      # Subject, Topic, Lesson, LessonProgress
│   │   │       ├── ai.py            # AIConversation, AIMessage
│   │   │       ├── performance.py   # StudentTopicPerformance
│   │   │       ├── quiz.py          # Question, Quiz, Attempt, Response
│   │   │       ├── recommendation.py# Recommendation, LearningPlan
│   │   │       ├── teacher.py       # TeacherAlert
│   │   │       └── user.py          # User, StudentProfile, TeacherProfile, AuditLog
│   │   ├── routers/                 # Modular API endpoints
│   │   ├── schemas/                 # Pydantic validation schemas
│   │   └── services/                # Business logic & algorithms
│   │       ├── ai_tutor_service.py  # Socratic AI tutor with fallback
│   │       ├── auth_service.py      # User authentication & registration
│   │       ├── gap_detection_service.py # Knowledge gap detector
│   │       ├── quiz_service.py      # Adaptive quiz evaluator & scoring
│   │       ├── recommendation_service.py # Multi-tiered rules engine
│   │       ├── teacher_service.py   # Class telemetry & alert dispatch
│   │       └── admin_service.py     # System metrics & entity management
│   ├── scripts/
│   │   └── seed_data.py             # Realistic database seeder
│   └── tests/                       # Pytest unit & integration tests
│
└── frontend/
    ├── package.json                 # Node dependencies & build scripts
    ├── tsconfig.json                # TypeScript compiler configuration
    ├── tailwind.config.ts           # Academic SaaS design system
    ├── Dockerfile                   # Node production container definition
    └── src/
        ├── app/                     # Next.js App Router
        │   ├── layout.tsx           # Root layout with Query & Auth providers
        │   ├── page.tsx             # Landing hero & quick launch portal
        │   ├── login/               # Interactive login with demo picker
        │   ├── register/            # Role-based account creation
        │   ├── student/             # 8+ dedicated student screens
        │   ├── teacher/             # 4 dedicated teacher screens
        │   └── admin/               # 6 dedicated admin management screens
        ├── components/              # Reusable UI cards, badges, navbar, sidebar
        ├── lib/
        │   ├── api.ts               # Centralized fetch client with JWT
        │   └── auth.tsx             # React Auth context & hooks
        └── services/                # Type-safe client service layer
```

---

## 4. Database Schema Entities

| Entity | Description | Key Fields |
|---|---|---|
| `users` | Core user identity & role | `id`, `name`, `email`, `password_hash`, `role` (`STUDENT`, `TEACHER`, `ADMIN`) |
| `student_profiles` | Academic student metadata | `id`, `user_id`, `student_id`, `department`, `semester`, `academic_year` |
| `teacher_profiles` | Academic instructor metadata | `id`, `user_id`, `employee_id`, `department` |
| `subjects` | Curriculum subject domains | `id`, `name`, `code`, `description` |
| `topics` | Fine-grained subject nodes | `id`, `subject_id`, `name`, `description`, `difficulty_level` |
| `lessons` | Conceptual reading units | `id`, `subject_id`, `topic_id`, `title`, `content`, `estimated_minutes` |
| `lesson_progress` | Student lesson completion | `id`, `student_id`, `lesson_id`, `status`, `completion_percentage` |
| `questions` | Question bank items | `id`, `subject_id`, `topic_id`, `question_text`, `options`, `correct_answer`, `explanation` |
| `quizzes` | Assessments | `id`, `subject_id`, `title`, `quiz_type` (`TOPIC_ASSESSMENT`, `ADAPTIVE`), `question_count` |
| `quiz_attempts` | Recorded test submissions | `id`, `student_id`, `quiz_id`, `score`, `percentage`, `started_at`, `completed_at` |
| `quiz_responses` | Per-question answer logs | `id`, `attempt_id`, `question_id`, `selected_answer`, `is_correct`, `time_taken` |
| `student_topic_performance` | Real-time mastery score | `id`, `student_id`, `topic_id`, `attempts`, `accuracy`, `mastery_score` |
| `recommendations` | Targeted prescriptive tasks | `id`, `student_id`, `topic_id`, `recommendation_type`, `priority`, `status` |
| `learning_plans` | Ordered study roadmaps | `id`, `student_id`, `title`, `active`, `generated_at` |
| `ai_conversations` / `ai_messages` | Socratic tutoring logs | `id`, `student_id`, `role`, `content`, `created_at` |
| `teacher_alerts` | Real-time instructor alerts | `id`, `student_id`, `alert_type`, `severity`, `message`, `status` |
| `audit_logs` | Platform audit trail | `id`, `user_id`, `action`, `entity`, `entity_id`, `created_at` |

---

## 5. API Routes Overview

FastAPI provides interactive Swagger documentation at `http://localhost:8000/docs`.

### Authentication
- `POST /api/auth/register` — Create account with role-specific profile
- `POST /api/auth/login` — Authenticate and receive JWT Bearer token
- `GET  /api/auth/me` — Retrieve active session profile
- `POST /api/auth/logout` — End session

### Student Portal
- `GET /api/students/me/dashboard` — Full metrics, weak topics, and active recommendations
- `GET /api/students/me/recommendations` — Active personalized recommendations
- `GET /api/students/me/learning-plan` — Ordered sequence of study activities

### Curriculum & Content
- `GET /api/subjects` — Subjects with topic counts and completion ratios
- `GET /api/subjects/{id}` — Subject details and topic list
- `GET /api/lessons` — Filterable lessons by subject and topic
- `GET /api/lessons/{id}` — Full lesson content with reading instructions
- `POST /api/lessons/{id}/progress` — Record lesson completion status

### Quiz Engine
- `GET  /api/quizzes` — Quiz catalog with attempts count and highest score
- `POST /api/quizzes/{id}/start` — Serve questions (answers concealed)
- `POST /api/quizzes/{id}/submit` — Grade answers, calculate mastery, update gap analysis
- `GET  /api/quizzes/attempts` — Student quiz history
- `GET  /api/quizzes/attempts/{id}` — Post-assessment review with question-by-question explanations

### Performance & Analytics
- `GET /api/performance/overview` — Aggregated cognitive metrics
- `GET /api/performance/topics` — Accuracy and mastery scores per topic
- `GET /api/performance/history` — Temporal trend series for Recharts graphs

### Recommendations & AI Tutor
- `POST /api/recommendations/generate` — Trigger algorithmic re-evaluation
- `POST /api/recommendations/{id}/complete` — Mark recommendation satisfied
- `POST /api/ai/chat` — Context-aware Socratic tutor conversation

### Teacher Portal
- `GET   /api/teacher/dashboard` — Class-wide metrics, topic gaps, and alerts
- `GET   /api/teacher/students` — Student roster with risk indicators
- `GET   /api/teacher/students/{id}` — Deep-dive inspection into individual student
- `GET   /api/teacher/topic-gaps` — Aggregated topic difficulty distribution
- `GET   /api/teacher/alerts` — Real-time intervention alerts
- `PATCH /api/teacher/alerts/{id}` — Update alert status (`REVIEWED`, `RESOLVED`)

### Admin Console
- `GET    /api/admin/dashboard` — System telemetry and audit logs
- `GET    /api/admin/users` — User listing & role configuration
- `POST   /api/admin/subjects` — Create curriculum subject
- `POST   /api/admin/topics` — Create topic
- `POST   /api/admin/questions` — Add question to question bank
- `POST   /api/admin/quizzes` — Publish assessment quiz

---

## 6. Personalization & Recommendation Engine Logic

The recommendation engine implements a multi-tier rules-based algorithm to drive the student's mastery curve:

```python
# Topic Accuracy & Mastery Classification
IF mastery_score < 40%:
    priority = "HIGH"
    recommendation_type = "FOUNDATIONAL_LESSON"
    action = "Review foundational concept lesson + complete easy practice"
    trigger_alert("LOW_PERFORMANCE", severity="HIGH")

ELIF 40% <= mastery_score < 70%:
    priority = "HIGH"
    recommendation_type = "CONCEPT_REVISION"
    action = "Review core lesson + complete 10 targeted practice questions"
    IF attempts >= 2:
        trigger_alert("REPEATED_FAILURE", severity="MEDIUM")

ELSE:  # mastery_score >= 70%
    priority = "LOW"
    recommendation_type = "ADVANCED_CHALLENGE"
    action = "Unlock advanced challenges and next curriculum module"
    trigger_alert("MASTERY_ACHIEVED", severity="LOW")
```

Mastery scores utilize a weighted moving average (60% historical + 40% recent attempt) to ensure sustained retention rather than single-guess variance.

---

## 7. AI Tutor Implementation & Fallback Architecture

The AI tutor implements a provider abstraction:
- **`ExternalLLMProvider`**: Leverages standard OpenAI-compatible endpoints configured via `AI_API_KEY`, `AI_BASE_URL`, and `AI_MODEL`.
- **`FallbackTutorProvider`**: A built-in, context-aware pedagogical engine that operates without external keys. It reads student diagnostic performance, identifies weak topics, provides code examples, and enforces Socratic guidelines.
- **Assessment Integrity**: When a student interacts with the AI tutor while taking an active quiz (`is_during_quiz=True`), the system refuses to leak direct answers, instead providing conceptual hints and guiding questions.

---

## 8. Demo Credentials (Created by Seed Script)

| Role | Email | Password | Purpose |
|---|---|---|---|
| **Student** | `student@example.com` | `student123` | Full student experience, quiz taking, adaptive learning path |
| **Teacher** | `teacher@example.com` | `teacher123` | Classroom telemetry, student risk inspection, alert review |
| **Admin** | `admin@example.com` | `admin123` | User role management, curriculum CRUD, audit trail |

*(Note: These passwords are provided strictly for local development and demonstration).*

---

## 9. Local Setup & Execution Guide

### Prerequisites
- Python 3.11+
- Node.js 18+ & npm
- (Optional) Docker & Docker Compose

### Step 1: Environment Configuration
Create your local `.env` file from `.env.example`:
```bash
cp .env.example .env
```
*(Configure `DATABASE_URL` with your PostgreSQL instance, or leave blank to automatically utilize the built-in SQLite database).*

### Step 2: Backend Setup
```bash
cd backend

# Install dependencies
pip install -r requirements.txt

# Run database migrations
alembic upgrade head

# Seed realistic demo data (Java Functions @ 52%, users, curriculum)
python scripts/seed_data.py

# Run test suite
pytest tests

# Start FastAPI server
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```
*The API is now live at `http://localhost:8000` (Swagger docs: `http://localhost:8000/docs`).*

### Step 3: Frontend Setup
```bash
cd frontend

# Install dependencies
npm install

# Build production bundle
npm run build

# Start Next.js application
npm run start
```
*The web application is now live at `http://localhost:3000`.*

---

## 10. Docker Deployment

Deploy the entire stack with a single command:
```bash
docker-compose up --build
```
Services spun up:
- `spectra_postgres`: PostgreSQL 15 database on port 5432
- `spectra_backend`: FastAPI API server on port 8000
- `spectra_frontend`: Next.js web application on port 3000

---

## 11. Exact Demo Flow for Evaluators & Judges

To showcase the closed-loop learning engine end-to-end:

1. **Step 1 — Sign In**:
   - Navigate to `http://localhost:3000/login`.
   - Click the **"🎓 Student"** demo button to auto-fill `student@example.com` / `student123`. Click **Sign In**.
2. **Step 2 — Inspect Baseline Diagnostic**:
   - The student dashboard loads with real data calculated from the database.
   - Observe **Identified Knowledge Gaps**: **Java Functions & Parameters** is flagged as a **Weak Topic** with **52.0% accuracy**.
   - Note the **Recommended Next Focus**: *"Review the Functions Basics lesson and complete 10 targeted questions before retaking the quiz."*
3. **Step 3 — Start Assessment**:
   - Click **"Practice 10 Questions"** or navigate to **Adaptive Quizzes** &bull; select **Java Functions & Parameters Assessment**.
   - Answer the 10 questions. Notice the live timer, question navigation pills, and option selections.
4. **Step 4 — Submit Assessment with High Accuracy**:
   - Answer accurately (e.g. choose correct answers on pass-by-value, method overloading, void, StackOverflowError, etc.).
   - Click **Finish & Submit** &bull; confirm submission.
5. **Step 5 — View Instant Analytics & Recommendations**:
   - The results screen reveals your updated score (e.g. **80% - 90%**), question-by-question review, and explanations.
   - The system indicates that your mastery score has increased.
6. **Step 6 — Verify Real-Time Propagation**:
   - Return to the **Dashboard**: The overall average quiz score and topic mastery bars have dynamically updated.
   - Visit the **Progress Analytics** page to inspect the Recharts trend line and mastery distribution.
7. **Step 7 — Inspect Teacher Dashboard**:
   - Sign out and log in with the **"👩‍🏫 Teacher"** demo button (`teacher@example.com` / `teacher123`).
   - The teacher dashboard immediately reflects the student's updated class average and refreshed alert statuses.
#   s p e c t r a  
 