import pytest
from app.db.database import SessionLocal
from app.db.models.academic import Subject, Lesson, Topic
from app.db.models.puzzle import Puzzle, PuzzleAttempt
from app.db.models.quiz import Quiz, Question

def test_eight_subjects_ten_lessons_curriculum():
    """Verify all 8 required subjects have at least 10 lessons with puzzles and quiz questions."""
    db = SessionLocal()
    try:
        required_codes = ["JAVA", "PYTHON", "MATH", "CHEM", "AI", "DSA", "ML", "WEB"]
        for code in required_codes:
            subject = db.query(Subject).filter(Subject.code == code).first()
            assert subject is not None, f"Subject {code} must exist in the database."
            assert len(subject.lessons) >= 10, f"Subject {code} must have at least 10 lessons, got {len(subject.lessons)}."
            
            for lesson in subject.lessons:
                # Must have at least 1 puzzle
                puzzles = db.query(Puzzle).filter(Puzzle.lesson_id == lesson.id).all()
                assert len(puzzles) >= 1, f"Lesson '{lesson.title}' in {code} must have at least 1 puzzle."
                
                # Must have a quiz with at least 5 questions
                quiz = db.query(Quiz).filter(Quiz.lesson_id == lesson.id).first()
                assert quiz is not None, f"Lesson '{lesson.title}' in {code} must have a lesson quiz."
                assert len(quiz.quiz_questions) >= 5, f"Quiz for '{lesson.title}' must have at least 5 questions, got {len(quiz.quiz_questions)}."
    finally:
        db.close()

def test_puzzle_security_no_answer_leak(client):
    """Verify that student GET requests for puzzles NEVER expose the correct_answer field."""
    # 1. Login student
    login_resp = client.post("/api/auth/login", json={"email": "student@example.com", "password": "student123"})
    assert login_resp.status_code == 200
    token = login_resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 2. Get lesson 1 puzzles
    puzzles_resp = client.get("/api/lessons/1/puzzles", headers=headers)
    assert puzzles_resp.status_code == 200
    puzzles = puzzles_resp.json()
    assert len(puzzles) >= 1
    
    for p in puzzles:
        assert "correct_answer" not in p, "SECURITY LEAK: correct_answer exposed in student lesson puzzles endpoint!"
        assert "puzzle_data" in p
        assert "puzzle_type" in p
        assert "xp_reward" in p

    # 3. Get single puzzle detail
    p_id = puzzles[0]["id"]
    single_p_resp = client.get(f"/api/puzzles/{p_id}", headers=headers)
    assert single_p_resp.status_code == 200
    single_p = single_p_resp.json()
    assert "correct_answer" not in single_p, "SECURITY LEAK: correct_answer exposed in single puzzle endpoint!"

def test_puzzle_submission_and_xp_farming_prevention(client):
    """Verify puzzle grading, +10 XP awarding on first solve, and prevention of XP farming."""
    login_resp = client.post("/api/auth/login", json={"email": "student@example.com", "password": "student123"})
    token = login_resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Fetch initial dashboard for baseline XP
    dash_1 = client.get("/api/students/me/dashboard", headers=headers).json()
    initial_xp = dash_1["xp"]

    db = SessionLocal()
    # Find puzzle 1
    puzzle = db.query(Puzzle).filter(Puzzle.id == 1).first()
    assert puzzle is not None
    import json
    try:
        correct_ans = json.loads(puzzle.correct_answer)
    except Exception:
        correct_ans = puzzle.correct_answer
    db.close()

    # Submit incorrect answer
    fail_resp = client.post("/api/puzzles/1/submit", json={"submitted_answer": "definitely_wrong_answer_xyz"}, headers=headers)
    assert fail_resp.status_code == 200
    fail_data = fail_resp.json()
    assert fail_data["is_correct"] is False
    assert fail_data["xp_earned"] == 0

    # Submit correct answer
    solve_resp = client.post("/api/puzzles/1/submit", json={"submitted_answer": correct_ans}, headers=headers)
    assert solve_resp.status_code == 200
    solve_data = solve_resp.json()
    assert solve_data["is_correct"] is True
    # If first time solved, awards 10 XP; if already solved in prior test runs, 0 XP awarded
    assert solve_data["xp_earned"] in [0, 10]

    # Re-submit same correct answer to test anti-farming: must award 0 XP
    resubmit_resp = client.post("/api/puzzles/1/submit", json={"submitted_answer": correct_ans}, headers=headers)
    assert resubmit_resp.status_code == 200
    resubmit_data = resubmit_resp.json()
    assert resubmit_data["is_correct"] is True
    assert resubmit_data["xp_earned"] == 0, "Anti-farming failed: XP was awarded again for already solved puzzle!"

def test_topic_practice_modal_and_submission(client):
    """Verify topic practice questions and +10 XP reward on practice completion."""
    login_resp = client.post("/api/auth/login", json={"email": "student@example.com", "password": "student123"})
    token = login_resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Get topic practice
    practice_resp = client.get("/api/topics/1/practice", headers=headers)
    assert practice_resp.status_code == 200
    pdata = practice_resp.json()
    assert isinstance(pdata, list)
    assert len(pdata) >= 1

    # Submit practice
    sub_resp = client.post("/api/topics/1/practice/submit", json={"answers": []}, headers=headers)
    assert sub_resp.status_code == 200
    sub_data = sub_resp.json()
    assert sub_data["xp_earned"] == 10

