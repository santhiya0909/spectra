def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] in ["healthy", "degraded"]
    assert data["service"] == "SPECTRA Educational API"

def test_login_success(client):
    response = client.post("/api/auth/login", json={
        "email": "student@example.com",
        "password": "student123"
    })
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["role"] == "STUDENT"
    assert data["email"] == "student@example.com"

def test_login_invalid_password(client):
    response = client.post("/api/auth/login", json={
        "email": "student@example.com",
        "password": "wrongpassword"
    })
    assert response.status_code == 401

def test_rbac_teacher_access_denied_for_student(client):
    # Log in as student
    login_resp = client.post("/api/auth/login", json={
        "email": "student@example.com",
        "password": "student123"
    })
    token = login_resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Attempt to access teacher dashboard
    response = client.get("/api/teacher/dashboard", headers=headers)
    assert response.status_code == 403

def test_rbac_teacher_access_allowed_for_teacher(client):
    # Log in as teacher
    login_resp = client.post("/api/auth/login", json={
        "email": "teacher@example.com",
        "password": "teacher123"
    })
    token = login_resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    response = client.get("/api/teacher/dashboard", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert "total_students" in data
    assert "average_class_performance" in data
