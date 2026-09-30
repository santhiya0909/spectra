"""
Seed realistic Knowledge DNA demo data for students on Subject 12 and Subject 3.
Establishes:
1. Topic prerequisites in topic_prerequisites table
2. Realistic topic performances (Mastered, Developing, Weak, Not Started, Locked)
3. Associated quiz attempts to provide tangible learning evidence
"""
import sys
import os
from datetime import datetime, timezone, timedelta

backend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, backend_dir)

from app.db.database import SessionLocal, create_tables
from app.db.models.user import User, StudentProfile
from app.db.models.academic import Subject, Topic, Lesson, LessonProgress, TopicPrerequisite
from app.db.models.quiz import Quiz, QuizAttempt, QuizResponse, Question
from app.db.models.performance import StudentTopicPerformance


def seed_knowledge_dna_demo():
    print("=" * 60)
    print("SPECTRA — Seeding Knowledge DNA Demo Data & Prerequisites")
    print("=" * 60)

    db = SessionLocal()
    try:
        # 1. Ensure tables exist
        create_tables()

        # 2. Get students to seed for
        students = db.query(StudentProfile).all()
        if not students:
            print("[WARN] No student profiles found. Creating default student.")
            test_user = db.query(User).filter(User.role == "STUDENT").first()
            if not test_user:
                print("[ERROR] No student user exists.")
                return
            student = StudentProfile(
                user_id=test_user.id,
                student_id="STU-0001",
                department="Computer Science",
                semester=4,
                academic_year="2025-2026"
            )
            db.add(student)
            db.commit()
            db.refresh(student)
            students = [student]

        # 3. Setup Prerequisites for Subject 12 (Mathematics for Computing)
        s12 = db.query(Subject).filter(Subject.id == 12).first()
        if s12:
            s12_lessons = (
                db.query(Lesson)
                .filter(Lesson.subject_id == 12)
                .order_by(Lesson.lesson_order.asc())
                .all()
            )
            # Link sequential topic prerequisites
            for i in range(1, len(s12_lessons)):
                prev_l = s12_lessons[i - 1]
                curr_l = s12_lessons[i]
                if prev_l.topic_id and curr_l.topic_id:
                    exists = db.query(TopicPrerequisite).filter(
                        TopicPrerequisite.topic_id == curr_l.topic_id,
                        TopicPrerequisite.prerequisite_topic_id == prev_l.topic_id
                    ).first()
                    if not exists:
                        prereq = TopicPrerequisite(
                            topic_id=curr_l.topic_id,
                            prerequisite_topic_id=prev_l.topic_id,
                            description=f"{prev_l.title} provides foundational knowledge for {curr_l.title}"
                        )
                        db.add(prereq)
            db.commit()
            print(f"[OK] Seeded prerequisites for Subject 12 ({len(s12_lessons)} lessons)")

        # 4. Setup Prerequisites for Subject 3 (DBMS)
        s3 = db.query(Subject).filter(Subject.id == 3).first()
        if s3:
            s3_lessons = (
                db.query(Lesson)
                .filter(Lesson.subject_id == 3)
                .order_by(Lesson.lesson_order.asc())
                .all()
            )
            for i in range(1, len(s3_lessons)):
                prev_l = s3_lessons[i - 1]
                curr_l = s3_lessons[i]
                if prev_l.topic_id and curr_l.topic_id:
                    exists = db.query(TopicPrerequisite).filter(
                        TopicPrerequisite.topic_id == curr_l.topic_id,
                        TopicPrerequisite.prerequisite_topic_id == prev_l.topic_id
                    ).first()
                    if not exists:
                        prereq = TopicPrerequisite(
                            topic_id=curr_l.topic_id,
                            prerequisite_topic_id=prev_l.topic_id,
                            description=f"{prev_l.title} provides foundational knowledge for {curr_l.title}"
                        )
                        db.add(prereq)
            db.commit()
            print(f"[OK] Seeded prerequisites for Subject 3 ({len(s3_lessons)} lessons)")

        # 5. Seed realistic Knowledge DNA mastery states for the primary test students
        # We will configure Subject 12 topics with:
        # Lesson 1 (Topic 1): MASTERED (88.0%)
        # Lesson 2 (Topic 2): MASTERED (84.0%)
        # Lesson 3 (Topic 3): DEVELOPING (64.0%)
        # Lesson 4 (Topic 4): WEAK (42.0%) -> Triggering Prerequisite Gap!
        # Lesson 5 (Topic 5): DEVELOPING (54.0%)
        # Lesson 6 (Topic 6): NOT_STARTED
        # Lesson 7 (Topic 7): LOCKED
        demo_profiles = [s for s in students if s.id in [1, 2, 5]] or [students[0]]

        for s in demo_profiles:
            if s12 and s12_lessons:
                scores_pattern = [88.0, 84.0, 64.0, 42.0, 54.0, None, None]
                for idx, lesson in enumerate(s12_lessons):
                    if idx >= len(scores_pattern):
                        break
                    score = scores_pattern[idx]
                    t_id = lesson.topic_id
                    if not t_id:
                        continue

                    # Update Lesson Progress
                    prog = db.query(LessonProgress).filter(
                        LessonProgress.student_id == s.id,
                        LessonProgress.lesson_id == lesson.id
                    ).first()
                    if score is not None:
                        is_comp = score >= 50.0
                        if not prog:
                            prog = LessonProgress(
                                student_id=s.id,
                                lesson_id=lesson.id,
                                status="COMPLETED" if is_comp else "IN_PROGRESS",
                                completion_percentage=100.0 if is_comp else 60.0,
                                quiz_completed=True,
                                quiz_score=score,
                                completed_at=datetime.now(timezone.utc) if is_comp else None
                            )
                            db.add(prog)
                        else:
                            prog.status = "COMPLETED" if is_comp else "IN_PROGRESS"
                            prog.completion_percentage = 100.0 if is_comp else 60.0
                            prog.quiz_completed = True
                            prog.quiz_score = score

                        # Update or Create StudentTopicPerformance
                        perf = db.query(StudentTopicPerformance).filter(
                            StudentTopicPerformance.student_id == s.id,
                            StudentTopicPerformance.topic_id == t_id
                        ).first()
                        if not perf:
                            perf = StudentTopicPerformance(
                                student_id=s.id,
                                topic_id=t_id,
                                attempts=2 if score >= 80.0 else 1,
                                correct_answers=int(round((score / 100.0) * 5)),
                                total_questions=5,
                                accuracy=score,
                                mastery_score=score,
                                last_attempt_at=datetime.now(timezone.utc) - timedelta(hours=idx * 6)
                            )
                            db.add(perf)
                        else:
                            perf.mastery_score = score
                            perf.accuracy = score
                            perf.attempts = 2 if score >= 80.0 else 1

                        # Create QuizAttempt record so recent quiz score is accurately reflected
                        quiz = db.query(Quiz).filter(Quiz.lesson_id == lesson.id).first()
                        if quiz:
                            existing_att = db.query(QuizAttempt).filter(
                                QuizAttempt.student_id == s.id,
                                QuizAttempt.quiz_id == quiz.id
                            ).first()
                            if not existing_att:
                                att = QuizAttempt(
                                    student_id=s.id,
                                    quiz_id=quiz.id,
                                    score=score / 20.0,
                                    percentage=score,
                                    started_at=datetime.now(timezone.utc) - timedelta(hours=idx * 6 + 1),
                                    completed_at=datetime.now(timezone.utc) - timedelta(hours=idx * 6)
                                )
                                db.add(att)
                            else:
                                existing_att.percentage = score
                                existing_att.score = score / 20.0

            db.commit()
            print(f"[OK] Seeded demo performance data for Student {s.id} ({s.student_id})")

        print("\n[SUCCESS] Knowledge DNA demo data seeding complete!")

    except Exception as exc:
        db.rollback()
        print(f"[ERROR] Seeding failed: {exc}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()


if __name__ == "__main__":
    seed_knowledge_dna_demo()
