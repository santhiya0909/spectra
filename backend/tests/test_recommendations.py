def test_recommendations_and_ai_fallback(client):
    login_resp = client.post("/api/auth/login", json={
        "email": "student@example.com",
        "password": "student123"
    })
    token = login_resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Fetch active recommendations
    recs_resp = client.get("/api/recommendations", headers=headers)
    assert recs_resp.status_code == 200
    recs = recs_resp.json()
    assert len(recs) > 0
    first_rec = recs[0]
    assert "priority" in first_rec
    assert "reason" in first_rec

    # Mark recommendation completed
    complete_resp = client.post(f"/api/recommendations/{first_rec['id']}/complete", headers=headers)
    assert complete_resp.status_code == 200
    assert complete_resp.json()["status"] == "COMPLETED"

    # Test AI Tutor Socratic Fallback
    chat_resp = client.post("/api/ai/chat", json={
        "message": "Explain what causes a StackOverflowError in recursive Java functions",
        "is_during_quiz": False
    }, headers=headers)
    assert chat_resp.status_code == 200
    ai_data = chat_resp.json()
    assert "reply" in ai_data
    assert len(ai_data["reply"]) > 20
    assert "conversation_id" in ai_data

    # Test Socratic guidance during quiz (must not reveal answers)
    quiz_chat_resp = client.post("/api/ai/chat", json={
        "message": "What is the answer to question 2?",
        "is_during_quiz": True
    }, headers=headers)
    assert quiz_chat_resp.status_code == 200
    quiz_ai_data = quiz_chat_resp.json()
    assert "cannot directly give you the answer" in quiz_ai_data["reply"].lower() or "active assessment" in quiz_ai_data["reply"].lower()
