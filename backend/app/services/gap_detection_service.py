from typing import List, Dict, Any, Tuple
from sqlalchemy.orm import Session
from datetime import datetime, timezone
from app.db.models.performance import StudentTopicPerformance
from app.db.models.academic import Topic
from app.db.models.quiz import QuizAttempt, QuizResponse, Question

def update_topic_performance(
    db: Session,
    student_id: int,
    topic_id: int,
    questions_count: int,
    correct_count: int
) -> StudentTopicPerformance:
    """Updates or creates a student's topic performance record using exponential moving average / weighted calculation."""
    perf = db.query(StudentTopicPerformance).filter(
        StudentTopicPerformance.student_id == student_id,
        StudentTopicPerformance.topic_id == topic_id
    ).first()

    current_accuracy = (correct_count / questions_count * 100.0) if questions_count > 0 else 0.0

    if not perf:
        perf = StudentTopicPerformance(
            student_id=student_id,
            topic_id=topic_id,
            attempts=1,
            correct_answers=correct_count,
            total_questions=questions_count,
            accuracy=round(current_accuracy, 1),
            mastery_score=round(current_accuracy, 1),
            last_attempt_at=datetime.now(timezone.utc)
        )
        db.add(perf)
    else:
        perf.attempts += 1
        perf.correct_answers += correct_count
        perf.total_questions += questions_count
        
        # Cumulative accuracy
        cumulative_acc = (perf.correct_answers / perf.total_questions) * 100.0
        perf.accuracy = round(cumulative_acc, 1)

        # Mastery score blends historical accuracy with recent attempt (60% historical + 40% recent)
        new_mastery = (0.6 * perf.mastery_score) + (0.4 * current_accuracy)
        perf.mastery_score = round(max(0.0, min(100.0, new_mastery)), 1)
        perf.last_attempt_at = datetime.now(timezone.utc)

    db.commit()
    db.refresh(perf)
    return perf

def detect_knowledge_gaps(db: Session, student_id: int) -> Dict[str, Any]:
    """
    Analyzes student topic performances to classify:
    - Weak topics (mastery < 60% or accuracy < 60%)
    - Moderate / In-progress topics (60% <= mastery < 75%)
    - Mastered / Strong topics (mastery >= 75%)
    """
    performances = db.query(StudentTopicPerformance).filter(
        StudentTopicPerformance.student_id == student_id
    ).all()

    weak = []
    moderate = []
    strong = []

    for p in performances:
        topic = db.query(Topic).filter(Topic.id == p.topic_id).first()
        topic_name = topic.name if topic else f"Topic {p.topic_id}"
        
        data = {
            "topic_id": p.topic_id,
            "topic_name": topic_name,
            "accuracy": p.accuracy,
            "mastery_score": p.mastery_score,
            "attempts": p.attempts,
            "total_questions": p.total_questions,
            "last_attempt_at": p.last_attempt_at
        }

        if p.mastery_score < 60.0 or p.accuracy < 60.0:
            data["status"] = "WEAK"
            weak.append(data)
        elif p.mastery_score < 75.0:
            data["status"] = "NEEDS_PRACTICE"
            moderate.append(data)
        else:
            data["status"] = "MASTERED"
            strong.append(data)

    return {
        "weak_topics": weak,
        "moderate_topics": moderate,
        "strong_topics": strong,
        "total_assessed_topics": len(performances)
    }
