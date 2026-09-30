from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.db.database import Base

class Puzzle(Base):
    __tablename__ = "puzzles"

    id = Column(Integer, primary_key=True, index=True)
    subject_id = Column(Integer, ForeignKey("subjects.id", ondelete="CASCADE"), nullable=False, index=True)
    lesson_id = Column(Integer, ForeignKey("lessons.id", ondelete="CASCADE"), nullable=False, index=True)
    topic_id = Column(Integer, ForeignKey("topics.id", ondelete="SET NULL"), nullable=True, index=True)
    title = Column(String(150), nullable=False, index=True)
    description = Column(Text, nullable=True)
    puzzle_type = Column(String(30), nullable=False)  # MULTIPLE_CHOICE, FILL_BLANK, CODE_OUTPUT, ORDERING, MATCHING, TRUE_FALSE
    question = Column(Text, nullable=False)
    puzzle_data = Column(Text, nullable=False)  # JSON payload: options, match pairs, order list, code snippet
    correct_answer = Column(Text, nullable=False)  # JSON payload: correct answer structure (NEVER leaked to student before submission)
    explanation = Column(Text, nullable=True)
    difficulty = Column(String(20), default="MEDIUM")  # EASY, MEDIUM, HARD
    xp_reward = Column(Integer, default=10)
    display_order = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)

    subject = relationship("Subject", back_populates="puzzles")
    lesson = relationship("Lesson", back_populates="puzzles")
    topic = relationship("Topic", back_populates="puzzles")
    attempts = relationship("PuzzleAttempt", back_populates="puzzle", cascade="all, delete-orphan")

class PuzzleAttempt(Base):
    __tablename__ = "puzzle_attempts"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("student_profiles.id", ondelete="CASCADE"), nullable=False, index=True)
    puzzle_id = Column(Integer, ForeignKey("puzzles.id", ondelete="CASCADE"), nullable=False, index=True)
    submitted_answer = Column(Text, nullable=False)  # JSON string
    is_correct = Column(Boolean, nullable=False, default=False)
    attempts_count = Column(Integer, default=1)
    xp_earned = Column(Integer, default=0)
    completed_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    time_taken = Column(Integer, default=0)  # Seconds

    student = relationship("StudentProfile", back_populates="puzzle_attempts")
    puzzle = relationship("Puzzle", back_populates="attempts")
