from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base

class TeacherAlert(Base):
    __tablename__ = "teacher_alerts"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("student_profiles.id", ondelete="CASCADE"), nullable=False, index=True)
    topic_id = Column(Integer, ForeignKey("topics.id", ondelete="CASCADE"), nullable=False, index=True)
    alert_type = Column(String(50), nullable=False)  # LOW_PERFORMANCE, REPEATED_FAILURE, LOW_ACTIVITY, IMPROVING, MASTERY_ACHIEVED
    severity = Column(String(20), default="MEDIUM")  # HIGH, MEDIUM, LOW
    message = Column(Text, nullable=False)
    status = Column(String(20), default="ACTIVE")  # ACTIVE, REVIEWED, RESOLVED
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    student = relationship("StudentProfile", back_populates="teacher_alerts")
    topic = relationship("Topic", back_populates="teacher_alerts")
