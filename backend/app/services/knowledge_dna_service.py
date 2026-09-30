"""
Knowledge DNA Intelligence Service for SPECTRA
Connects: Subjects -> Lessons -> Topics -> Quiz Results -> Mastery Calculation -> Prerequisite Gaps -> Focus Recommendations
"""
from typing import List, Dict, Any, Optional
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_

from app.db.models.academic import Subject, Topic, Lesson, LessonProgress, Enrollment, TopicPrerequisite
from app.db.models.quiz import Quiz, Question, QuizAttempt, QuizResponse
from app.db.models.performance import StudentTopicPerformance
from app.schemas.knowledge_dna import (
    KnowledgeDNANode,
    KnowledgeDNAEdge,
    KnowledgeDNAFocusRecommendation,
    KnowledgeDNASummary,
    KnowledgeDNAResponse,
    TopicKnowledgeDNADetail
)
from app.schemas.academic import YouTubeVideoOut
from app.services.youtube_service import get_or_create_lesson_youtube_recommendations


def determine_mastery_state(mastery_score: float, attempts: int, lesson_completed: bool, is_locked: bool = False) -> str:
    """
    Standard SPECTRA Mastery Thresholds:
    - 80.0% - 100.0%: MASTERED (Green)
    - 50.0% - 79.9%:  DEVELOPING (Yellow)
    - 1.0%  - 49.9%:  WEAK (Red)
    - 0 attempts & no activity: NOT_STARTED (Gray)
    - Prerequisite unstarted: LOCKED (Lock/Indigo)
    """
    if is_locked and attempts == 0 and not lesson_completed:
        return "LOCKED"
    if attempts == 0 and not lesson_completed:
        return "NOT_STARTED"
    if mastery_score >= 80.0:
        return "MASTERED"
    if mastery_score >= 50.0:
        return "DEVELOPING"
    return "WEAK"


def get_student_primary_subject_id(db: Session, student_id: int) -> int:
    """Find the student's active or primary enrolled subject (defaults to 12 or 3)."""
    enrollment = db.query(Enrollment).filter(Enrollment.student_id == student_id).order_by(Enrollment.enrolled_at.desc()).first()
    if enrollment:
        # Prefer subject 12 if enrolled, or the latest enrolled
        math_e = db.query(Enrollment).filter(Enrollment.student_id == student_id, Enrollment.subject_id == 12).first()
        if math_e:
            return 12
        return enrollment.subject_id
    
    # Fallback to subject 12 or subject 3
    subj12 = db.query(Subject).filter(Subject.id == 12).first()
    if subj12:
        return 12
    subj3 = db.query(Subject).filter(Subject.id == 3).first()
    if subj3:
        return 3
    first_subj = db.query(Subject).filter(Subject.is_active == True).first()
    return first_subj.id if first_subj else 1


def get_knowledge_dna_for_student(
    db: Session,
    student_id: int,
    subject_id: Optional[int] = None
) -> KnowledgeDNAResponse:
    """
    Constructs the complete Knowledge DNA graph for a student within a subject:
    1. Loads all subject topics and linked lessons.
    2. Computes topic mastery scores and states based on quiz evidence and lesson progress.
    3. Traces prerequisite links and identifies prerequisite gaps.
    4. Evaluates downstream impact and determines the highest-priority AI learning focus.
    """
    if not subject_id:
        subject_id = get_student_primary_subject_id(db, student_id)

    subject = None
    if subject_id:
        subject = db.query(Subject).filter(Subject.id == subject_id).first()

    if not subject:
        # 1. Prefer subject from student's most recent quiz attempt
        recent_att = (
            db.query(QuizAttempt)
            .join(Quiz, Quiz.id == QuizAttempt.quiz_id)
            .filter(QuizAttempt.student_id == student_id)
            .order_by(QuizAttempt.completed_at.desc(), QuizAttempt.id.desc())
            .first()
        )
        if recent_att:
            quiz_obj = db.query(Quiz).filter(Quiz.id == recent_att.quiz_id).first()
            if quiz_obj and quiz_obj.subject_id:
                subject = db.query(Subject).filter(Subject.id == quiz_obj.subject_id).first()

        # 2. Prefer subject where student has topic performance recorded
        if not subject:
            latest_perf = (
                db.query(StudentTopicPerformance)
                .join(Topic, Topic.id == StudentTopicPerformance.topic_id)
                .filter(StudentTopicPerformance.student_id == student_id)
                .order_by(StudentTopicPerformance.last_attempt_at.desc(), StudentTopicPerformance.id.desc())
                .first()
            )
            if latest_perf:
                topic_obj = db.query(Topic).filter(Topic.id == latest_perf.topic_id).first()
                if topic_obj and topic_obj.subject_id:
                    subject = db.query(Subject).filter(Subject.id == topic_obj.subject_id).first()

        # 3. Prefer subject where student has lesson progress
        if not subject:
            latest_prog = (
                db.query(LessonProgress)
                .join(Lesson, Lesson.id == LessonProgress.lesson_id)
                .filter(LessonProgress.student_id == student_id)
                .order_by(LessonProgress.last_accessed.desc())
                .first()
            )
            if latest_prog:
                lesson_obj = db.query(Lesson).filter(Lesson.id == latest_prog.lesson_id).first()
                if lesson_obj and lesson_obj.subject_id:
                    subject = db.query(Subject).filter(Subject.id == lesson_obj.subject_id).first()

        # 4. Fallback to first available subject with active topics
        if not subject:
            subject = db.query(Subject).join(Topic, Topic.subject_id == Subject.id).first()
            if not subject:
                subject = db.query(Subject).first()

        if not subject:
            return KnowledgeDNAResponse(
                subject_id=0,
                subject_name="Curriculum",
                subject_code="NONE",
                overall_mastery=0.0
            )

    # 1. Fetch all active topics and lessons
    topics = (
        db.query(Topic)
        .filter(Topic.subject_id == subject.id, Topic.is_active == True)
        .order_by(Topic.display_order.asc(), Topic.id.asc())
        .all()
    )

    lessons = (
        db.query(Lesson)
        .filter(Lesson.subject_id == subject.id, Lesson.is_active == True)
        .order_by(Lesson.lesson_order.asc(), Lesson.id.asc())
        .all()
    )

    lesson_by_id = {l.id: l for l in lessons}
    lesson_by_topic_id = {}
    for l in lessons:
        if l.topic_id:
            lesson_by_topic_id[l.topic_id] = l

    # 2. Fetch student performance records for these topics (latest per topic)
    topic_ids = [t.id for t in topics]
    performances = (
        db.query(StudentTopicPerformance)
        .filter(
            StudentTopicPerformance.student_id == student_id,
            StudentTopicPerformance.topic_id.in_(topic_ids)
        )
        .order_by(StudentTopicPerformance.last_attempt_at.desc(), StudentTopicPerformance.id.desc())
        .all()
    )
    perf_by_topic = {}
    for p in performances:
        if p.topic_id not in perf_by_topic:
            perf_by_topic[p.topic_id] = p

    # 3. Fetch lesson progress for these lessons
    lesson_ids = [l.id for l in lessons]
    progresses = (
        db.query(LessonProgress)
        .filter(
            LessonProgress.student_id == student_id,
            LessonProgress.lesson_id.in_(lesson_ids)
        )
        .all()
    )
    prog_by_lesson = {p.lesson_id: p for p in progresses}

    # 4. Fetch recent quiz attempts for accuracy verification
    recent_attempts = (
        db.query(QuizAttempt)
        .join(Quiz, Quiz.id == QuizAttempt.quiz_id)
        .filter(
            QuizAttempt.student_id == student_id,
            Quiz.subject_id == subject.id
        )
        .order_by(QuizAttempt.completed_at.desc())
        .all()
    )
    # Map attempt score by quiz.lesson_id and quiz.topic_id
    quiz_score_by_topic = {}
    for att in recent_attempts:
        q = db.query(Quiz).filter(Quiz.id == att.quiz_id).first()
        if q and q.topic_id and q.topic_id not in quiz_score_by_topic:
            quiz_score_by_topic[q.topic_id] = att.percentage
        if q and q.lesson_id:
            l = lesson_by_id.get(q.lesson_id)
            if l and l.topic_id and l.topic_id not in quiz_score_by_topic:
                quiz_score_by_topic[l.topic_id] = att.percentage

    # 5. Build Prerequisite Graph
    # Check explicit DB prerequisites
    explicit_prereqs = (
        db.query(TopicPrerequisite)
        .filter(TopicPrerequisite.topic_id.in_(topic_ids))
        .all()
    )
    prereq_map: Dict[int, List[int]] = {t.id: [] for t in topics}
    dependent_map: Dict[int, List[int]] = {t.id: [] for t in topics}

    for ep in explicit_prereqs:
        if ep.topic_id in prereq_map and ep.prerequisite_topic_id in prereq_map:
            prereq_map[ep.topic_id].append(ep.prerequisite_topic_id)
            dependent_map[ep.prerequisite_topic_id].append(ep.topic_id)

    # If no explicit prerequisites exist in table, establish natural sequential curriculum flow
    has_any_explicit = len(explicit_prereqs) > 0
    if not has_any_explicit and len(topics) > 1:
        for idx in range(1, len(topics)):
            curr_id = topics[idx].id
            prev_id = topics[idx - 1].id
            prereq_map[curr_id].append(prev_id)
            dependent_map[prev_id].append(curr_id)

    topic_by_id = {t.id: t for t in topics}

    # 6. First Pass: Compute Initial Mastery and State for each Topic
    raw_node_data = {}
    for idx, topic in enumerate(topics):
        perf = perf_by_topic.get(topic.id)
        linked_lesson = lesson_by_topic_id.get(topic.id)
        if not linked_lesson and topic.lesson_id:
            linked_lesson = lesson_by_id.get(topic.lesson_id)
        if not linked_lesson and idx < len(lessons):
            linked_lesson = lessons[idx]

        lesson_prog = prog_by_lesson.get(linked_lesson.id) if linked_lesson else None
        is_completed = (lesson_prog.status == "COMPLETED") if lesson_prog else False

        recent_quiz = quiz_score_by_topic.get(topic.id)

        # Calculate Mastery Score
        if perf and perf.attempts > 0:
            m_score = perf.mastery_score
            attempts_cnt = perf.attempts
            corr_ans = perf.correct_answers
            tot_q = perf.total_questions
        elif recent_quiz is not None:
            m_score = recent_quiz
            attempts_cnt = 1
            corr_ans = int(round(recent_quiz / 20.0))
            tot_q = 5
        elif is_completed:
            m_score = 65.0  # Completed lesson material without quiz checkpoint yet
            attempts_cnt = 0
            corr_ans = 0
            tot_q = 0
        else:
            m_score = 0.0
            attempts_cnt = 0
            corr_ans = 0
            tot_q = 0

        raw_node_data[topic.id] = {
            "topic": topic,
            "lesson": linked_lesson,
            "mastery_score": round(m_score, 1),
            "recent_quiz": recent_quiz,
            "attempts": attempts_cnt,
            "correct_answers": corr_ans,
            "total_questions": tot_q,
            "lesson_completed": is_completed,
            "lesson_order": linked_lesson.lesson_order if linked_lesson else (idx + 1),
            "display_order": topic.display_order or (idx + 1)
        }

    # 7. Second Pass: Evaluate Prerequisites, Gaps, and Locked States
    nodes: List[KnowledgeDNANode] = []
    edges: List[KnowledgeDNAEdge] = []

    for topic in topics:
        d = raw_node_data[topic.id]
        t_id = topic.id
        m_score = d["mastery_score"]
        attempts = d["attempts"]
        l_comp = d["lesson_completed"]

        prereq_ids = prereq_map.get(t_id, [])
        dep_ids = dependent_map.get(t_id, [])

        prereq_names = [topic_by_id[pid].name for pid in prereq_ids if pid in topic_by_id]
        dep_names = [topic_by_id[did].name for did in dep_ids if did in topic_by_id]

        # Check if locked: all prerequisites are NOT_STARTED, and this topic has no attempts
        is_locked = False
        if prereq_ids and attempts == 0 and not l_comp:
            all_prereqs_unstarted = all(
                raw_node_data[pid]["attempts"] == 0 and not raw_node_data[pid]["lesson_completed"]
                for pid in prereq_ids if pid in raw_node_data
            )
            # If the immediate prior is not even started or completed
            if all_prereqs_unstarted:
                is_locked = True

        m_state = determine_mastery_state(m_score, attempts, l_comp, is_locked)

        # Detect prerequisite gaps
        has_prereq_gap = False
        weak_prereq_details = []
        for pid in prereq_ids:
            if pid in raw_node_data:
                p_data = raw_node_data[pid]
                p_score = p_data["mastery_score"]
                p_state = determine_mastery_state(p_score, p_data["attempts"], p_data["lesson_completed"])
                if p_state in ["WEAK", "DEVELOPING"]:
                    has_prereq_gap = True
                    weak_prereq_details.append(f"{p_data['topic'].name} ({p_state.title()}, {p_score}%)")

        # Formulate "Why is this weak?" evidence-based explanation
        why_weak = None
        action_plan_str = None

        if m_state == "WEAK":
            if has_prereq_gap and d["recent_quiz"] is not None:
                why_weak = (
                    f"Your recent quiz score of {d['recent_quiz']}% is below the 50% developing threshold. "
                    f"Additionally, prerequisite {', '.join(weak_prereq_details)} needs reinforcement, directly limiting your conceptual readiness here."
                )
                action_plan_str = f"Review {weak_prereq_details[0].split('(')[0].strip()} -> Practice {topic.name} -> Retake Mastery Check"
            elif d["recent_quiz"] is not None:
                why_weak = (
                    f"Your recent quiz score on {topic.name} is {d['recent_quiz']}%, indicating fundamental gaps in core concepts."
                )
                action_plan_str = f"Re-read {topic.name} concepts -> Watch visual explanation -> Retake Quiz"
            elif has_prereq_gap:
                why_weak = (
                    f"Prerequisite {', '.join(weak_prereq_details)} has an unaddressed knowledge gap affecting downstream readiness."
                )
                action_plan_str = f"Master prerequisite concepts before starting {topic.name}"
            else:
                why_weak = "Early assessment indicates foundational misconceptions on this topic."
                action_plan_str = f"Complete the interactive puzzle and lesson for {topic.name}"

        elif m_state == "DEVELOPING":
            if has_prereq_gap:
                why_weak = (
                    f"Mastery is progressing ({m_score}%), but upstream concept {', '.join(weak_prereq_details)} needs reinforcement to secure reliable retention."
                )
            else:
                why_weak = f"You are building proficiency ({m_score}%). Scoring 80%+ on the checkpoint quiz will promote this topic to Mastered."
            action_plan_str = f"Targeted practice on {topic.name} checkpoint questions"

        elif m_state == "NOT_STARTED":
            why_weak = "No quiz attempts or lesson completion evidence recorded yet."
            action_plan_str = f"Start reading {topic.name} lesson and solve the interactive concept puzzle"

        elif m_state == "LOCKED":
            why_weak = f"Locked until foundational prerequisite '{prereq_names[0] if prereq_names else 'Prior Topic'}' is begun."
            action_plan_str = f"Begin with {prereq_names[0] if prereq_names else 'foundations'}"

        node = KnowledgeDNANode(
            id=topic.id,
            name=topic.name,
            description=topic.description,
            lesson_id=d["lesson"].id if d["lesson"] else None,
            lesson_title=d["lesson"].title if d["lesson"] else None,
            lesson_order=d["lesson_order"],
            display_order=d["display_order"],
            difficulty_level=topic.difficulty_level or "MEDIUM",
            mastery_score=m_score,
            mastery_state=m_state,
            recent_quiz_score=d["recent_quiz"],
            attempts_count=attempts,
            correct_answers=d["correct_answers"],
            total_questions=d["total_questions"],
            lesson_completed=l_comp,
            prerequisite_gap=has_prereq_gap,
            prerequisite_names=prereq_names,
            prerequisite_ids=prereq_ids,
            dependent_names=dep_names,
            why_weak_explanation=why_weak,
            recommended_action=action_plan_str
        )
        nodes.append(node)

        # Build Edges
        for pid in prereq_ids:
            if pid in topic_by_id:
                p_node_data = raw_node_data.get(pid, {})
                p_score = p_node_data.get("mastery_score", 0.0)
                if p_score >= 80.0:
                    e_status = "SATISFIED"
                elif p_score >= 50.0:
                    e_status = "GAP"
                else:
                    e_status = "GAP" if p_node_data.get("attempts", 0) > 0 else "LOCKED"

                edges.append(
                    KnowledgeDNAEdge(
                        source=pid,
                        target=t_id,
                        source_name=topic_by_id[pid].name,
                        target_name=topic.name,
                        status=e_status
                    )
                )

    # 8. Categorize Nodes
    strong_areas = [n for n in nodes if n.mastery_state == "MASTERED"]
    developing_areas = [n for n in nodes if n.mastery_state == "DEVELOPING"]
    weak_areas = [n for n in nodes if n.mastery_state == "WEAK"]
    not_started_areas = [n for n in nodes if n.mastery_state in ["NOT_STARTED", "LOCKED"]]

    # 9. Compute Overall Mastery
    active_assessed = [n.mastery_score for n in nodes if n.attempts_count > 0 or n.lesson_completed]
    overall_mastery = round(sum(active_assessed) / len(active_assessed), 1) if active_assessed else 0.0

    # 10. Intelligent "SPECTRA Recommends" Focus Determination
    recommended_focus = None

    # Priority 1: A WEAK topic that has dependent topics (highest leverage)
    weak_with_dependents = [n for n in weak_areas if len(n.dependent_names) > 0]
    # Priority 2: Any WEAK topic
    # Priority 3: A DEVELOPING topic with lowest score
    # Priority 4: The first NOT_STARTED topic whose prerequisites are completed
    focus_node = None
    if weak_with_dependents:
        focus_node = min(weak_with_dependents, key=lambda x: x.mastery_score)
    elif weak_areas:
        focus_node = min(weak_areas, key=lambda x: x.mastery_score)
    elif developing_areas:
        focus_node = min(developing_areas, key=lambda x: x.mastery_score)
    elif not_started_areas:
        focus_node = not_started_areas[0]
    elif nodes:
        focus_node = nodes[0]

    if focus_node:
        dep_str = f"Blocking {len(focus_node.dependent_names)} downstream topics ({', '.join(focus_node.dependent_names[:2])})." if focus_node.dependent_names else "Essential foundational topic."
        
        if focus_node.mastery_state == "WEAK":
            f_reason = f"This is currently your weakest concept ({focus_node.mastery_score}% mastery). {dep_str}"
        elif focus_node.mastery_state == "DEVELOPING":
            f_reason = f"Proficiency is developing ({focus_node.mastery_score}%). Closing this gap will elevate your overall track mastery to 80%+."
        else:
            f_reason = f"Next scheduled milestone in your curriculum path: {focus_node.name}."

        action_plan = [
            f"Review lesson: {focus_node.lesson_title or focus_node.name}",
            "Watch curated visual explanation video",
            "Solve the interactive concept puzzle",
            "Pass the 5-question Checkpoint Quiz (>= 80% to master)"
        ]

        recommended_focus = KnowledgeDNAFocusRecommendation(
            topic_id=focus_node.id,
            topic_name=focus_node.name,
            lesson_id=focus_node.lesson_id,
            lesson_title=focus_node.lesson_title,
            mastery_score=focus_node.mastery_score,
            mastery_state=focus_node.mastery_state,
            reason=f_reason,
            prerequisite_impact=dep_str,
            action_plan=action_plan
        )

    return KnowledgeDNAResponse(
        subject_id=subject.id,
        subject_name=subject.name,
        subject_code=subject.code,
        overall_mastery=overall_mastery,
        mastered_count=len(strong_areas),
        developing_count=len(developing_areas),
        weak_count=len(weak_areas),
        not_started_count=len([n for n in nodes if n.mastery_state == "NOT_STARTED"]),
        locked_count=len([n for n in nodes if n.mastery_state == "LOCKED"]),
        total_topics=len(nodes),
        recommended_focus=recommended_focus,
        nodes=nodes,
        edges=edges,
        strong_areas=strong_areas,
        developing_areas=developing_areas,
        weak_areas=weak_areas,
        not_started_areas=not_started_areas
    )


def get_knowledge_dna_summary(
    db: Session,
    student_id: int,
    subject_id: Optional[int] = None
) -> KnowledgeDNASummary:
    """Lightweight summary query designed specifically for compact dashboard cards."""
    full = get_knowledge_dna_for_student(db, student_id, subject_id)
    return KnowledgeDNASummary(
        subject_id=full.subject_id,
        subject_name=full.subject_name,
        subject_code=full.subject_code,
        overall_mastery=full.overall_mastery,
        mastered_count=full.mastered_count,
        developing_count=full.developing_count,
        weak_count=full.weak_count,
        not_started_count=full.not_started_count,
        locked_count=full.locked_count,
        total_topics=full.total_topics,
        recommended_focus=full.recommended_focus
    )


def get_topic_knowledge_dna_detail(
    db: Session,
    student_id: int,
    topic_id: int
) -> TopicKnowledgeDNADetail:
    """Detailed topic drill-down view including learning evidence, prerequisites, and YouTube recommendations."""
    topic = db.query(Topic).filter(Topic.id == topic_id).first()
    if not topic:
        raise ValueError("Topic not found")

    full_dna = get_knowledge_dna_for_student(db, student_id, topic.subject_id)
    target_node = next((n for n in full_dna.nodes if n.id == topic_id), None)
    if not target_node:
        raise ValueError("Topic node not found in Knowledge DNA graph")

    # Fetch YouTube recommendations for this lesson
    yt_videos = []
    if target_node.lesson_id:
        try:
            yt_res = get_or_create_lesson_youtube_recommendations(db, target_node.lesson_id)
            yt_videos = yt_res.videos
        except Exception:
            yt_videos = []

    # Format prerequisites detail
    prereq_details = []
    for pid in target_node.prerequisite_ids:
        p_node = next((n for n in full_dna.nodes if n.id == pid), None)
        if p_node:
            prereq_details.append({
                "topic_id": p_node.id,
                "name": p_node.name,
                "mastery_score": p_node.mastery_score,
                "mastery_state": p_node.mastery_state,
                "lesson_id": p_node.lesson_id
            })

    # Format dependents detail
    dep_details = []
    for node in full_dna.nodes:
        if target_node.id in node.prerequisite_ids:
            dep_details.append({
                "topic_id": node.id,
                "name": node.name,
                "mastery_score": node.mastery_score,
                "mastery_state": node.mastery_state,
                "lesson_id": node.lesson_id
            })

    # Recent quiz attempts for this topic
    attempts_records = []
    q_attempts = (
        db.query(QuizAttempt)
        .join(Quiz, Quiz.id == QuizAttempt.quiz_id)
        .filter(
            QuizAttempt.student_id == student_id,
            Quiz.topic_id == topic_id
        )
        .order_by(QuizAttempt.completed_at.desc())
        .limit(5)
        .all()
    )
    for a in q_attempts:
        attempts_records.append({
            "attempt_id": a.id,
            "score": a.score,
            "percentage": a.percentage,
            "completed_at": a.completed_at.isoformat() if a.completed_at else None
        })

    # Recent puzzle attempts for this topic
    from app.db.models.puzzle import Puzzle, PuzzleAttempt
    p_attempts = (
        db.query(PuzzleAttempt)
        .join(Puzzle, Puzzle.id == PuzzleAttempt.puzzle_id)
        .filter(
            PuzzleAttempt.student_id == student_id,
            Puzzle.topic_id == topic_id
        )
        .order_by(PuzzleAttempt.completed_at.desc())
        .limit(5)
        .all()
    )
    puzzle_records = []
    puzzle_correct = 0
    for pa in p_attempts:
        if pa.is_correct:
            puzzle_correct += 1
        p_obj = db.query(Puzzle).filter(Puzzle.id == pa.puzzle_id).first()
        puzzle_records.append({
            "attempt_id": pa.id,
            "puzzle_id": pa.puzzle_id,
            "puzzle_title": p_obj.title if p_obj else "Challenge",
            "is_correct": pa.is_correct,
            "xp_earned": pa.xp_earned,
            "completed_at": pa.completed_at.isoformat() if pa.completed_at else None
        })

    total_topic_puzzles = db.query(Puzzle).filter(Puzzle.topic_id == topic_id, Puzzle.is_active == True).count()
    solved_topic_puzzles = db.query(PuzzleAttempt.puzzle_id).join(Puzzle).filter(
        Puzzle.topic_id == topic_id,
        PuzzleAttempt.student_id == student_id,
        PuzzleAttempt.is_correct == True
    ).distinct().count()
    puzzle_acc = round((puzzle_correct / len(p_attempts) * 100.0), 1) if p_attempts else None

    return TopicKnowledgeDNADetail(
        node=target_node,
        prerequisites=prereq_details,
        dependents=dep_details,
        recent_attempts=attempts_records,
        puzzle_attempts=puzzle_records,
        puzzle_accuracy=puzzle_acc,
        puzzle_solved_count=solved_topic_puzzles,
        puzzle_total_count=total_topic_puzzles,
        youtube_videos=yt_videos
    )
