from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Float, Boolean
from sqlalchemy.orm import relationship
from app.db.database import Base

class Subject(Base):
    __tablename__ = "subjects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, index=True, nullable=False)
    code = Column(String(20), unique=True, index=True, nullable=False)
    description = Column(Text, nullable=True)
    category = Column(String(50), default="COMPUTER_SCIENCE", nullable=True)
    difficulty_level = Column(String(20), default="BEGINNER", nullable=True)
    thumbnail_url = Column(String(255), nullable=True)
    display_order = Column(Integer, default=0, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)

    topics = relationship("Topic", back_populates="subject", cascade="all, delete-orphan")
    lessons = relationship("Lesson", back_populates="subject", cascade="all, delete-orphan", order_by="Lesson.lesson_order")
    quizzes = relationship("Quiz", back_populates="subject", cascade="all, delete-orphan")
    enrollments = relationship("Enrollment", back_populates="subject", cascade="all, delete-orphan")
    puzzles = relationship("Puzzle", back_populates="subject", cascade="all, delete-orphan")

class Lesson(Base):
    __tablename__ = "lessons"

    id = Column(Integer, primary_key=True, index=True)
    subject_id = Column(Integer, ForeignKey("subjects.id", ondelete="CASCADE"), nullable=False, index=True)
    topic_id = Column(Integer, ForeignKey("topics.id", ondelete="SET NULL"), nullable=True, index=True)
    title = Column(String(150), nullable=False, index=True)
    short_description = Column(String(255), nullable=True)
    detailed_description = Column(Text, nullable=True)
    description = Column(Text, nullable=True)
    content = Column(Text, nullable=True)  # Rich markdown or educational content
    resource_url = Column(String(255), nullable=True)
    difficulty = Column(String(20), default="MEDIUM")  # EASY, MEDIUM, HARD
    difficulty_level = Column(String(20), default="MEDIUM")
    estimated_minutes = Column(Integer, default=15)
    estimated_duration = Column(Integer, default=15)
    lesson_order = Column(Integer, default=0, nullable=False)
    display_order = Column(Integer, default=0, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)

    subject = relationship("Subject", back_populates="lessons")
    topic = relationship("Topic", back_populates="lessons", foreign_keys=[topic_id])
    topics = relationship("Topic", back_populates="lesson", foreign_keys="[Topic.lesson_id]", cascade="all, delete-orphan", order_by="Topic.display_order")
    study_resources = relationship("StudyResource", back_populates="lesson", cascade="all, delete-orphan", order_by="StudyResource.display_order")
    progresses = relationship("LessonProgress", back_populates="lesson", cascade="all, delete-orphan")
    puzzles = relationship("Puzzle", back_populates="lesson", cascade="all, delete-orphan", order_by="Puzzle.display_order")
    quizzes = relationship("Quiz", back_populates="lesson", cascade="all, delete-orphan")
    questions = relationship("Question", back_populates="lesson", cascade="all, delete-orphan")
    youtube_recommendations = relationship("LessonYouTubeVideo", back_populates="lesson", cascade="all, delete-orphan", order_by="LessonYouTubeVideo.rank.asc()")

class Topic(Base):
    __tablename__ = "topics"

    id = Column(Integer, primary_key=True, index=True)
    subject_id = Column(Integer, ForeignKey("subjects.id", ondelete="CASCADE"), nullable=False, index=True)
    lesson_id = Column(Integer, ForeignKey("lessons.id", ondelete="SET NULL"), nullable=True, index=True)
    name = Column(String(100), nullable=False, index=True)
    description = Column(Text, nullable=True)
    difficulty_level = Column(String(20), default="MEDIUM")  # EASY, MEDIUM, HARD
    display_order = Column(Integer, default=0, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)

    subject = relationship("Subject", back_populates="topics")
    lesson = relationship("Lesson", back_populates="topics", foreign_keys=[lesson_id])
    lessons = relationship("Lesson", back_populates="topic", foreign_keys="[Lesson.topic_id]")
    study_resources = relationship("StudyResource", back_populates="topic")
    questions = relationship("Question", back_populates="topic", cascade="all, delete-orphan")
    performances = relationship("StudentTopicPerformance", back_populates="topic", cascade="all, delete-orphan")
    recommendations = relationship("Recommendation", back_populates="topic", cascade="all, delete-orphan")
    teacher_alerts = relationship("TeacherAlert", back_populates="topic", cascade="all, delete-orphan")
    puzzles = relationship("Puzzle", back_populates="topic", cascade="all, delete-orphan")
    quizzes = relationship("Quiz", back_populates="topic", cascade="all, delete-orphan")

class StudyResource(Base):
    __tablename__ = "study_resources"

    id = Column(Integer, primary_key=True, index=True)
    lesson_id = Column(Integer, ForeignKey("lessons.id", ondelete="CASCADE"), nullable=False, index=True)
    topic_id = Column(Integer, ForeignKey("topics.id", ondelete="SET NULL"), nullable=True, index=True)
    title = Column(String(200), nullable=False, index=True)
    description = Column(Text, nullable=True)
    url = Column(String(500), nullable=False)
    resource_type = Column(String(50), default="DOCUMENTATION", nullable=False)  # DOCUMENTATION, ARTICLE, VIDEO, TUTORIAL, CHEATSHEET, PRACTICE
    provider = Column(String(100), default="EXTERNAL", nullable=False)  # MDN, W3Schools, Python Docs, etc.
    display_order = Column(Integer, default=0, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)

    lesson = relationship("Lesson", back_populates="study_resources")
    topic = relationship("Topic", back_populates="study_resources")

class Enrollment(Base):
    __tablename__ = "enrollments"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("student_profiles.id", ondelete="CASCADE"), nullable=False, index=True)
    subject_id = Column(Integer, ForeignKey("subjects.id", ondelete="CASCADE"), nullable=False, index=True)
    enrolled_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    student = relationship("StudentProfile", back_populates="enrollments")
    subject = relationship("Subject", back_populates="enrollments")

class LessonProgress(Base):
    __tablename__ = "lesson_progress"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("student_profiles.id", ondelete="CASCADE"), nullable=False, index=True)
    lesson_id = Column(Integer, ForeignKey("lessons.id", ondelete="CASCADE"), nullable=False, index=True)
    status = Column(String(20), default="NOT_STARTED")  # NOT_STARTED, IN_PROGRESS, COMPLETED
    completion_percentage = Column(Float, default=0.0)
    topics_completed = Column(Integer, default=0)
    puzzles_completed = Column(Integer, default=0)
    quiz_completed = Column(Boolean, default=False)
    quiz_score = Column(Float, default=0.0)
    xp_earned = Column(Integer, default=0)
    completed_at = Column(DateTime(timezone=True), nullable=True)

    student = relationship("StudentProfile", back_populates="lesson_progresses")
    lesson = relationship("Lesson", back_populates="progresses")

class LessonYouTubeVideo(Base):
    __tablename__ = "lesson_youtube_videos"

    id = Column(Integer, primary_key=True, index=True)
    lesson_id = Column(Integer, ForeignKey("lessons.id", ondelete="CASCADE"), nullable=False, index=True)
    video_id = Column(String(50), nullable=False, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    thumbnail_url = Column(String(500), nullable=True)
    channel_name = Column(String(150), nullable=True)
    duration = Column(String(50), nullable=True)
    url = Column(String(500), nullable=False)
    published_at = Column(String(50), nullable=True)
    rank = Column(Integer, default=0, nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    lesson = relationship("Lesson", back_populates="youtube_recommendations")

class TopicPrerequisite(Base):
    __tablename__ = "topic_prerequisites"

    id = Column(Integer, primary_key=True, index=True)
    topic_id = Column(Integer, ForeignKey("topics.id", ondelete="CASCADE"), nullable=False, index=True)
    prerequisite_topic_id = Column(Integer, ForeignKey("topics.id", ondelete="CASCADE"), nullable=False, index=True)
    description = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    topic = relationship("Topic", foreign_keys=[topic_id], backref="prerequisite_associations")
    prerequisite_topic = relationship("Topic", foreign_keys=[prerequisite_topic_id])
