from datetime import datetime, timezone
from sqlalchemy import Column, Integer, DateTime, ForeignKey, Float
from sqlalchemy.orm import relationship
from app.db.database import Base

class StudentTopicPerformance(Base):
    __tablename__ = "student_topic_performance"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("student_profiles.id", ondelete="CASCADE"), nullable=False, index=True)
    topic_id = Column(Integer, ForeignKey("topics.id", ondelete="CASCADE"), nullable=False, index=True)
    attempts = Column(Integer, default=0)
    correct_answers = Column(Integer, default=0)
    total_questions = Column(Integer, default=0)
    accuracy = Column(Float, default=0.0)  # Percentage 0.0 - 100.0
    mastery_score = Column(Float, default=0.0)  # Adaptive mastery level 0.0 - 100.0
    last_attempt_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    student = relationship("StudentProfile", back_populates="topic_performances")
    topic = relationship("Topic", back_populates="performances")
