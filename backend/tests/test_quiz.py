def test_student_dashboard_metrics(client):
    login_resp = client.post("/api/auth/login", json={
        "email": "student@example.com",
        "password": "student123"
    })
    token = login_resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    response = client.get("/api/students/me/dashboard", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert "greeting" in data
    assert "overall_progress" in data
    assert "weak_topics" in data
    # Verify Java Functions is in the initial weak topics list from the baseline 52% data
    weak_names = [w["topic_name"] for w in data["weak_topics"]]
    assert any("Java Functions" in name for name in weak_names)

def test_quiz_start_and_submission(client):
    login_resp = client.post("/api/auth/login", json={
        "email": "student@example.com",
        "password": "student123"
    })
    token = login_resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Fetch quizzes
    quizzes_resp = client.get("/api/quizzes", headers=headers)
    assert quizzes_resp.status_code == 200
    quizzes = quizzes_resp.json()
    assert len(quizzes) > 0
    quiz_id = quizzes[0]["id"]

    # Start quiz
    start_resp = client.post(f"/api/quizzes/{quiz_id}/start", headers=headers)
    assert start_resp.status_code == 200
    questions = start_resp.json()
    assert len(questions) > 0

    # Ensure correct answers are NOT leaked in QuestionOut
    for q in questions:
        assert "correct_answer" not in q

    # Submit answers
    answers = []
    for q in questions:
        answers.append({
            "question_id": q["id"],
            "selected_answer": q["options"][0] if q["options"] else "A",
            "time_taken": 25
        })

    submit_resp = client.post(f"/api/quizzes/{quiz_id}/submit", json={"answers": answers}, headers=headers)
    assert submit_resp.status_code == 200
    result = submit_resp.json()
    assert "percentage" in result
    assert "score" in result
    assert "questions_review" in result
    assert len(result["questions_review"]) == len(questions)
