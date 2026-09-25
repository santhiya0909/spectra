from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.db.database import Base

class Recommendation(Base):
    __tablename__ = "recommendations"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("student_profiles.id", ondelete="CASCADE"), nullable=False, index=True)
    topic_id = Column(Integer, ForeignKey("topics.id", ondelete="CASCADE"), nullable=False, index=True)
    recommendation_type = Column(String(50), nullable=False)  # CONCEPT_REVISION, TARGETED_PRACTICE, RETAKE_QUIZ, ADVANCED_TOPIC
    title = Column(String(200), nullable=False)
    reason = Column(Text, nullable=False)
    priority = Column(String(20), default="MEDIUM")  # HIGH, MEDIUM, LOW
    resource_id = Column(Integer, nullable=True)  # ID of lesson, quiz, or practice set
    status = Column(String(20), default="ACTIVE")  # ACTIVE, COMPLETED, DISMISSED
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    student = relationship("StudentProfile", back_populates="recommendations")
    topic = relationship("Topic", back_populates="recommendations")

class LearningPlan(Base):
    __tablename__ = "learning_plans"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("student_profiles.id", ondelete="CASCADE"), nullable=False, index=True)
    title = Column(String(150), nullable=False)
    generated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    active = Column(Boolean, default=True)

    student = relationship("StudentProfile", back_populates="learning_plans")
    items = relationship("LearningPlanItem", back_populates="learning_plan", cascade="all, delete-orphan", order_by="LearningPlanItem.order_index")

class LearningPlanItem(Base):
    __tablename__ = "learning_plan_items"

    id = Column(Integer, primary_key=True, index=True)
    learning_plan_id = Column(Integer, ForeignKey("learning_plans.id", ondelete="CASCADE"), nullable=False, index=True)
    resource_type = Column(String(50), nullable=False)  # LESSON, QUIZ, PRACTICE
    resource_id = Column(Integer, nullable=False)
    order_index = Column(Integer, default=0)
    completed = Column(Boolean, default=False)

    learning_plan = relationship("LearningPlan", back_populates="items")
