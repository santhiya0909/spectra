from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Float, Boolean
from sqlalchemy.orm import relationship
from app.db.database import Base

class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    subject_id = Column(Integer, ForeignKey("subjects.id", ondelete="CASCADE"), nullable=False, index=True)
    topic_id = Column(Integer, ForeignKey("topics.id", ondelete="CASCADE"), nullable=False, index=True)
    lesson_id = Column(Integer, ForeignKey("lessons.id", ondelete="CASCADE"), nullable=True, index=True)
    question_text = Column(Text, nullable=False)
    question_type = Column(String(20), default="MCQ")  # MCQ, MULTI_SELECT
    options = Column(Text, nullable=False)  # JSON-encoded array of options: ["A) ...", "B) ..."]
    correct_answer = Column(Text, nullable=False)  # Answer key or exact string
    explanation = Column(Text, nullable=True)  # Detailed feedback for student improvement
    difficulty = Column(String(20), default="MEDIUM", index=True)  # EASY, MEDIUM, HARD
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    topic = relationship("Topic", back_populates="questions")
    lesson = relationship("Lesson", back_populates="questions")
    quiz_associations = relationship("QuizQuestion", back_populates="question", cascade="all, delete-orphan")
    responses = relationship("QuizResponse", back_populates="question")

class Quiz(Base):
    __tablename__ = "quizzes"

    id = Column(Integer, primary_key=True, index=True)
    subject_id = Column(Integer, ForeignKey("subjects.id", ondelete="CASCADE"), nullable=False, index=True)
    lesson_id = Column(Integer, ForeignKey("lessons.id", ondelete="CASCADE"), nullable=True, index=True)
    topic_id = Column(Integer, ForeignKey("topics.id", ondelete="CASCADE"), nullable=True, index=True)
    title = Column(String(150), nullable=False)
    description = Column(Text, nullable=True)
    quiz_type = Column(String(30), default="LESSON")  # LESSON, TOPIC, ASSESSMENT, PRACTICE, ADAPTIVE
    difficulty = Column(String(20), default="MEDIUM")
    question_count = Column(Integer, default=5)

    subject = relationship("Subject", back_populates="quizzes")
    lesson = relationship("Lesson", back_populates="quizzes")
    topic = relationship("Topic", back_populates="quizzes")
    quiz_questions = relationship("QuizQuestion", back_populates="quiz", cascade="all, delete-orphan", order_by="QuizQuestion.order_index")
    attempts = relationship("QuizAttempt", back_populates="quiz", cascade="all, delete-orphan")

class QuizQuestion(Base):
    __tablename__ = "quiz_questions"

    id = Column(Integer, primary_key=True, index=True)
    quiz_id = Column(Integer, ForeignKey("quizzes.id", ondelete="CASCADE"), nullable=False, index=True)
    question_id = Column(Integer, ForeignKey("questions.id", ondelete="CASCADE"), nullable=False, index=True)
    order_index = Column(Integer, default=0)

    quiz = relationship("Quiz", back_populates="quiz_questions")
    question = relationship("Question", back_populates="quiz_associations")

class QuizAttempt(Base):
    __tablename__ = "quiz_attempts"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("student_profiles.id", ondelete="CASCADE"), nullable=False, index=True)
    quiz_id = Column(Integer, ForeignKey("quizzes.id", ondelete="CASCADE"), nullable=False, index=True)
    score = Column(Float, nullable=False, default=0.0)
    percentage = Column(Float, nullable=False, default=0.0)
    started_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    completed_at = Column(DateTime(timezone=True), nullable=True)

    student = relationship("StudentProfile", back_populates="attempts")
    quiz = relationship("Quiz", back_populates="attempts")
    responses = relationship("QuizResponse", back_populates="attempt", cascade="all, delete-orphan")

class QuizResponse(Base):
    __tablename__ = "quiz_responses"

    id = Column(Integer, primary_key=True, index=True)
    attempt_id = Column(Integer, ForeignKey("quiz_attempts.id", ondelete="CASCADE"), nullable=False, index=True)
    question_id = Column(Integer, ForeignKey("questions.id", ondelete="CASCADE"), nullable=False, index=True)
    selected_answer = Column(Text, nullable=True)
    is_correct = Column(Boolean, nullable=False, default=False)
    time_taken = Column(Integer, default=0)  # Seconds spent on question

    attempt = relationship("QuizAttempt", back_populates="responses")
    question = relationship("Question", back_populates="responses")
