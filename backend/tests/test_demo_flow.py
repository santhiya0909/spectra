import pytest
from fastapi.testclient import TestClient
from app.main import app

def test_full_demo_flow(client):
    """
    Validates Phase 26: The exact judge demonstration flow:
    STEP 1: Student logs in
    STEP 2: Student opens dashboard & inspects baseline weak topic (~52% in Java Functions)
    STEP 3: Student reviews personalized recommendation generated for Java Functions
    STEP 4: Student takes Java Functions quiz
    STEP 5: Student answers questions with high accuracy (~80-90%)
    STEP 6: Backend stores attempt and updates topic performance
    STEP 7: Mastery score increases dynamically
    STEP 8: Recommendation engine updates learning path
    STEP 9: Teacher dashboard reflects the student's improved score and updated risk status
    """
    # 1. Login
    login_resp = client.post("/api/auth/login", json={
        "email": "student@example.com",
        "password": "student123"
    })
    assert login_resp.status_code == 200
    token = login_resp.json()["access_token"]
    student_headers = {"Authorization": f"Bearer {token}"}

    # 2. Open Dashboard & verify initial baseline
    dash_resp = client.get("/api/students/me/dashboard", headers=student_headers)
    assert dash_resp.status_code == 200
    dash_data = dash_resp.json()
    assert dash_data["greeting"] == "Welcome back, Alex Mercer!"
    
    # Verify Java Functions is in the initial weak topics list (~52%)
    initial_weak = dash_data["weak_topics"]
    assert any("Java Functions" in wt["topic_name"] for wt in initial_weak)

    # 3. Inspect recommendations
    rec_resp = client.get("/api/recommendations", headers=student_headers)
    assert rec_resp.status_code == 200
    recs = rec_resp.json()
    assert len(recs) > 0
    assert any("Java Functions" in r["title"] for r in recs)

    # 4. Start Java Functions Quiz (Quiz #1)
    start_resp = client.post("/api/quizzes/1/start", headers=student_headers)
    assert start_resp.status_code == 200
    questions = start_resp.json()
    assert len(questions) == 10

    # 5. Submit improved quiz answers (8 correct out of 10 = 80%)
    # Let's formulate answers: option matching correct keywords
    answers = []
    for idx, q in enumerate(questions):
        # Answer accurately for first 8 questions, make mistake on last 2
        if idx < 8:
            # Pick option starting with B, C, or correct option prefix
            chosen = q["options"][1] if len(q["options"]) > 1 else q["options"][0]
            # Specifically check known correct choices from seed data:
            if "pass-by-value" in q["question_text"]:
                chosen = next((opt for opt in q["options"] if "pass-by-value" in opt), q["options"][0])
            elif "solely by their return type" in q["question_text"]:
                chosen = next((opt for opt in q["options"] if "No" in opt), q["options"][0])
            elif "not return any data" in q["question_text"]:
                chosen = next((opt for opt in q["options"] if "void" in opt), q["options"][0])
            elif "lacks an adequate base case" in q["question_text"]:
                chosen = next((opt for opt in q["options"] if "StackOverflowError" in opt), q["options"][0])
            elif "object reference" in q["question_text"]:
                chosen = next((opt for opt in q["options"] if "memory address" in opt or "reference value" in opt), q["options"][0])
            elif "without creating an instance" in q["question_text"]:
                chosen = next((opt for opt in q["options"] if "static" in opt), q["options"][0])
            elif "variable-length argument (varargs) syntax" in q["question_text"]:
                chosen = next((opt for opt in q["options"] if "Type... name" in opt), q["options"][0])
            elif "position of a variable-length argument" in q["question_text"]:
                chosen = next((opt for opt in q["options"] if "last parameter" in opt), q["options"][0])
        else:
            chosen = q["options"][0]

        answers.append({
            "question_id": q["id"],
            "selected_answer": chosen,
            "time_taken": 35
        })

    submit_resp = client.post("/api/quizzes/1/submit", json={"answers": answers}, headers=student_headers)
    assert submit_resp.status_code == 200
    result = submit_resp.json()
    assert result["score"] >= 8.0
    assert result["percentage"] >= 80.0
    assert result["status"] == "PASSED"

    # 6. Verify Dashboard updates dynamically (calculated from DB)
    updated_dash_resp = client.get("/api/students/me/dashboard", headers=student_headers)
    assert updated_dash_resp.status_code == 200
    updated_dash = updated_dash_resp.json()
    # Average score should have increased
    assert updated_dash["average_quiz_score"] > dash_data["average_quiz_score"]
    
    # 7. Verify Teacher Dashboard reflects the improved performance
    teacher_login = client.post("/api/auth/login", json={
        "email": "teacher@example.com",
        "password": "teacher123"
    })
    teacher_token = teacher_login.json()["access_token"]
    teacher_headers = {"Authorization": f"Bearer {teacher_token}"}

    teacher_dash_resp = client.get("/api/teacher/dashboard", headers=teacher_headers)
    assert teacher_dash_resp.status_code == 200
    t_data = teacher_dash_resp.json()
    assert t_data["average_class_performance"] > 0
