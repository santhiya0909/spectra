import json
from typing import List, Dict, Any, Optional
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.db.models.quiz import Quiz, Question, QuizQuestion, QuizAttempt, QuizResponse
from app.db.models.academic import Topic, Subject
from app.db.models.performance import StudentTopicPerformance
from app.schemas.quiz import QuizSubmission, QuizResultOut, QuestionReviewOut, QuestionOut
from app.services.gap_detection_service import update_topic_performance, detect_knowledge_gaps
from app.services.recommendation_service import generate_recommendations_for_student

def get_questions_for_quiz(db: Session, quiz_id: int, student_id: Optional[int] = None) -> List[QuestionOut]:
    """Retrieves questions for a quiz, adapting difficulty if it is an adaptive assessment."""
    quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")

    selected_questions: List[Question] = []

    # If adaptive quiz type and student is known, tailor question selection to student's mastery
    if quiz.quiz_type == "ADAPTIVE" and student_id:
        topics = db.query(Topic).filter(Topic.subject_id == quiz.subject_id).all()
        for t in topics:
            perf = db.query(StudentTopicPerformance).filter(
                StudentTopicPerformance.student_id == student_id,
                StudentTopicPerformance.topic_id == t.id
            ).first()
            mastery = perf.mastery_score if perf else 50.0

            if mastery < 40.0:
                target_diff = "EASY"
            elif mastery < 70.0:
                target_diff = "MEDIUM"
            else:
                target_diff = "HARD"

            # Query questions matching target difficulty
            topic_q = db.query(Question).filter(
                Question.topic_id == t.id,
                Question.difficulty == target_diff
            ).limit(2).all()

            if not topic_q:
                topic_q = db.query(Question).filter(Question.topic_id == t.id).limit(2).all()
            selected_questions.extend(topic_q)

        # Cap at quiz question count
        selected_questions = selected_questions[:quiz.question_count]
    else:
        # Standard curated quiz
        assoc_questions = (
            db.query(Question)
            .join(QuizQuestion, QuizQuestion.question_id == Question.id)
            .filter(QuizQuestion.quiz_id == quiz.id)
            .order_by(QuizQuestion.order_index)
            .all()
        )
        if assoc_questions:
            selected_questions = assoc_questions
        else:
            # Fallback: grab questions from the quiz's subject
            selected_questions = db.query(Question).filter(
                Question.subject_id == quiz.subject_id
            ).limit(quiz.question_count).all()

    result = []
    for q in selected_questions:
        try:
            options_list = json.loads(q.options) if isinstance(q.options, str) else q.options
        except Exception:
            options_list = [q.options] if q.options else []

        topic = db.query(Topic).filter(Topic.id == q.topic_id).first()
        result.append(
            QuestionOut(
                id=q.id,
                subject_id=q.subject_id,
                topic_id=q.topic_id,
                topic_name=topic.name if topic else "General",
                question_text=q.question_text,
                question_type=q.question_type,
                options=options_list,
                difficulty=q.difficulty
            )
        )
    return result

def submit_quiz_attempt(
    db: Session,
    quiz_id: int,
    student_id: int,
    submission: QuizSubmission
) -> QuizResultOut:
    """
    Evaluates quiz submission, computes score, persists attempt & individual responses,
    updates topic mastery, detects gaps, and triggers recommendations.
    """
    quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")

    # Map submission answers by question_id
    answers_map = {ans.question_id: ans for ans in submission.answers}
    question_ids = list(answers_map.keys())

    if not question_ids:
        raise HTTPException(status_code=400, detail="No answers provided in quiz submission.")

    questions = db.query(Question).filter(Question.id.in_(question_ids)).all()
    q_dict = {q.id: q for q in questions}

    total_questions = len(question_ids)
    correct_count = 0
    questions_review: List[QuestionReviewOut] = []
    topic_tally: Dict[int, Dict[str, int]] = {}  # topic_id -> {total, correct}

    for q_id, user_ans in answers_map.items():
        question = q_dict.get(q_id)
        if not question:
            continue

        selected = user_ans.selected_answer.strip() if user_ans.selected_answer else ""
        correct = question.correct_answer.strip()
        
        # Check correctness (handling letter prefix like "A) ..." or exact answer match)
        is_corr = False
        if selected:
            if selected.lower() == correct.lower():
                is_corr = True
            elif selected[0:2].upper() == correct[0:2].upper():
                is_corr = True
            elif selected.split(")")[0].strip().upper() == correct.split(")")[0].strip().upper():
                is_corr = True

        if is_corr:
            correct_count += 1

        # Track per-topic performance
        if question.topic_id not in topic_tally:
            topic_tally[question.topic_id] = {"total": 0, "correct": 0}
        topic_tally[question.topic_id]["total"] += 1
        if is_corr:
            topic_tally[question.topic_id]["correct"] += 1

        # Options for review
        try:
            options_list = json.loads(question.options) if isinstance(question.options, str) else question.options
        except Exception:
            options_list = [question.options]

        topic = db.query(Topic).filter(Topic.id == question.topic_id).first()

        questions_review.append(
            QuestionReviewOut(
                id=question.id,
                question_text=question.question_text,
                options=options_list,
                selected_answer=selected,
                correct_answer=correct,
                is_correct=is_corr,
                explanation=question.explanation or "Standard answer evaluation.",
                topic_id=question.topic_id,
                topic_name=topic.name if topic else "General"
            )
        )

    score = float(correct_count)
    percentage = round((score / total_questions) * 100.0, 1) if total_questions > 0 else 0.0

    # Save Attempt
    attempt = QuizAttempt(
        student_id=student_id,
        quiz_id=quiz.id,
        score=score,
        percentage=percentage,
        started_at=datetime.now(timezone.utc),
        completed_at=datetime.now(timezone.utc)
    )
    db.add(attempt)
    db.flush()

    # Save Individual Responses
    for q_id, user_ans in answers_map.items():
        question = q_dict.get(q_id)
        if not question:
            continue
        selected = user_ans.selected_answer.strip() if user_ans.selected_answer else ""
        review_item = next((r for r in questions_review if r.id == q_id), None)
        is_corr = review_item.is_correct if review_item else False

        resp = QuizResponse(
            attempt_id=attempt.id,
            question_id=q_id,
            selected_answer=selected,
            is_correct=is_corr,
            time_taken=user_ans.time_taken
        )
        db.add(resp)

    db.commit()

    # Update Topic Performance for each involved topic
    for topic_id, tally in topic_tally.items():
        update_topic_performance(
            db=db,
            student_id=student_id,
            topic_id=topic_id,
            questions_count=tally["total"],
            correct_count=tally["correct"]
        )

    # Detect Knowledge Gaps & Trigger Recommendations
    gap_data = detect_knowledge_gaps(db, student_id)
    weak_topic_names = [w["topic_name"] for w in gap_data["weak_topics"]]

    # Run Recommendation Engine
    new_recs = generate_recommendations_for_student(db, student_id)
    rec_titles = [r.title for r in new_recs]

    status_str = "PASSED" if percentage >= 70.0 else ("NEEDS_IMPROVEMENT" if percentage >= 40.0 else "FAILED")

    return QuizResultOut(
        attempt_id=attempt.id,
        quiz_id=quiz.id,
        quiz_title=quiz.title,
        score=score,
        total_questions=total_questions,
        percentage=percentage,
        status=status_str,
        questions_review=questions_review,
        weak_topics=weak_topic_names,
        recommendations_generated=rec_titles
    )
