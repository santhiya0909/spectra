from typing import List, Optional
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from app.db.models.performance import StudentTopicPerformance
from app.db.models.academic import Topic, Lesson, LessonProgress
from app.db.models.quiz import Quiz, Question
from app.db.models.recommendation import Recommendation, LearningPlan, LearningPlanItem
from app.db.models.teacher import TeacherAlert

def generate_recommendations_for_student(
    db: Session,
    student_id: int,
    trigger_topic_id: Optional[int] = None
) -> List[Recommendation]:
    """
    Evaluates student's topic mastery and generates tailored recommendations
    following the SPECTRA personalization rules engine:
    - Mastery < 40%: Foundational lesson + easy practice
    - Mastery 40% - 70%: Concept revision + targeted practice (10 questions) + retake quiz
    - Mastery >= 70%: Advanced content + challenge quiz
    """
    query = db.query(StudentTopicPerformance).filter(
        StudentTopicPerformance.student_id == student_id
    )
    if trigger_topic_id:
        query = query.filter(StudentTopicPerformance.topic_id == trigger_topic_id)
        
    performances = query.all()
    created_recommendations = []

    for perf in performances:
        topic = db.query(Topic).filter(Topic.id == perf.topic_id).first()
        if not topic:
            continue

        mastery = perf.mastery_score
        accuracy = perf.accuracy

        # Find relevant lessons for this topic
        topic_lessons = db.query(Lesson).filter(Lesson.topic_id == topic.id).all()
        foundational_lesson = next((l for l in topic_lessons if l.difficulty == "EASY"), topic_lessons[0] if topic_lessons else None)
        standard_lesson = next((l for l in topic_lessons if l.difficulty in ["MEDIUM", "EASY"]), foundational_lesson)

        # Deactivate old active recommendations for this topic to keep recommendations fresh
        db.query(Recommendation).filter(
            Recommendation.student_id == student_id,
            Recommendation.topic_id == topic.id,
            Recommendation.status == "ACTIVE"
        ).update({"status": "SUPERSEDED"})

        if mastery < 40.0:
            rec = Recommendation(
                student_id=student_id,
                topic_id=topic.id,
                recommendation_type="FOUNDATIONAL_LESSON",
                title=f"Review Foundational Concepts: {topic.name}",
                reason=f"Your current mastery in {topic.name} is {mastery}%. A foundational review will strengthen your core understanding before attempting more questions.",
                priority="HIGH",
                resource_id=foundational_lesson.id if foundational_lesson else None,
                status="ACTIVE"
            )
            db.add(rec)
            created_recommendations.append(rec)

            # Trigger teacher alert for critical low performance
            create_or_update_teacher_alert(
                db, student_id, topic.id,
                alert_type="LOW_PERFORMANCE",
                severity="HIGH",
                message=f"Student has critically low mastery ({mastery}%) in {topic.name}. Needs foundational intervention."
            )

        elif 40.0 <= mastery < 70.0:
            rec = Recommendation(
                student_id=student_id,
                topic_id=topic.id,
                recommendation_type="CONCEPT_REVISION",
                title=f"Targeted Revision & 10 Practice Questions: {topic.name}",
                reason=f"Your accuracy in {topic.name} is {accuracy}%. Review the core lesson and complete 10 targeted practice questions to solidify your knowledge before retaking the assessment.",
                priority="HIGH",
                resource_id=standard_lesson.id if standard_lesson else None,
                status="ACTIVE"
            )
            db.add(rec)
            created_recommendations.append(rec)

            if perf.attempts >= 2 and mastery < 55.0:
                create_or_update_teacher_alert(
                    db, student_id, topic.id,
                    alert_type="REPEATED_FAILURE",
                    severity="MEDIUM",
                    message=f"Student attempted {topic.name} {perf.attempts} times with stagnant accuracy ({accuracy}%). Targeted practice advised."
                )

        else:  # mastery >= 70.0
            rec = Recommendation(
                student_id=student_id,
                topic_id=topic.id,
                recommendation_type="ADVANCED_CHALLENGE",
                title=f"Advance to Next Level: {topic.name}",
                reason=f"Great work! You have achieved {mastery}% mastery in {topic.name}. You are ready for advanced problems and next subject topics.",
                priority="LOW",
                resource_id=standard_lesson.id if standard_lesson else None,
                status="ACTIVE"
            )
            db.add(rec)
            created_recommendations.append(rec)

            if mastery >= 80.0:
                create_or_update_teacher_alert(
                    db, student_id, topic.id,
                    alert_type="MASTERY_ACHIEVED",
                    severity="LOW",
                    message=f"Student achieved strong mastery ({mastery}%) in {topic.name}."
                )

    db.commit()
    
    # Sync with Active Learning Plan
    update_student_learning_plan(db, student_id)
    return created_recommendations

def create_or_update_teacher_alert(
    db: Session,
    student_id: int,
    topic_id: int,
    alert_type: str,
    severity: str,
    message: str
):
    """Generates an actionable alert for teachers."""
    existing = db.query(TeacherAlert).filter(
        TeacherAlert.student_id == student_id,
        TeacherAlert.topic_id == topic_id,
        TeacherAlert.status == "ACTIVE"
    ).first()

    if existing:
        existing.alert_type = alert_type
        existing.severity = severity
        existing.message = message
        existing.created_at = datetime.now(timezone.utc)
    else:
        new_alert = TeacherAlert(
            student_id=student_id,
            topic_id=topic_id,
            alert_type=alert_type,
            severity=severity,
            message=message,
            status="ACTIVE"
        )
        db.add(new_alert)
    db.commit()

def update_student_learning_plan(db: Session, student_id: int):
    """Builds an active personalized sequence of study items based on latest recommendations."""
    plan = db.query(LearningPlan).filter(
        LearningPlan.student_id == student_id,
        LearningPlan.active == True
    ).first()

    if not plan:
        plan = LearningPlan(
            student_id=student_id,
            title="Personalized Adaptive Learning Path",
            active=True
        )
        db.add(plan)
        db.flush()

    # Clear old items
    db.query(LearningPlanItem).filter(LearningPlanItem.learning_plan_id == plan.id).delete()

    # Fetch active recommendations
    recs = db.query(Recommendation).filter(
        Recommendation.student_id == student_id,
        Recommendation.status == "ACTIVE"
    ).order_by(Recommendation.priority.desc()).all()

    order = 1
    for r in recs:
        # Step 1: Lesson Review
        if r.resource_id:
            lesson_item = LearningPlanItem(
                learning_plan_id=plan.id,
                resource_type="LESSON",
                resource_id=r.resource_id,
                order_index=order,
                completed=False
            )
            db.add(lesson_item)
            order += 1

        # Step 2: Practice Quiz for Topic
        quiz = db.query(Quiz).filter(Quiz.subject_id == r.topic.subject_id).first()
        if quiz:
            quiz_item = LearningPlanItem(
                learning_plan_id=plan.id,
                resource_type="QUIZ",
                resource_id=quiz.id,
                order_index=order,
                completed=False
            )
            db.add(quiz_item)
            order += 1

    db.commit()
