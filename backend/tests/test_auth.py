from werkzeug.security import generate_password_hash

from app import db
from app.models.user import User


def test_register_success(client):
    response = client.post("/api/auth/register", json={
        "name": "New Student",
        "student_id": "STU-TEST-100",
        "email": "new.student@test.com",
        "password": "TestPassword123!"
    })

    assert response.status_code == 201
    data = response.get_json()
    assert data["success"] is True
    assert data["user"]["email"] == "new.student@test.com"
    assert data["user"]["role"] == "STUDENT"


def test_register_duplicate_email(client, student):
    response = client.post("/api/auth/register", json={
        "name": "Another Student",
        "student_id": "STU-TEST-101",
        "email": "pytest.student@test.com",
        "password": "TestPassword123!"
    })

    assert response.status_code == 409
    data = response.get_json()
    assert data["success"] is False
    assert data["message"] == "Email already registered"


def test_login_success(client, app):
    with app.app_context():
        user = User(
            name="Login Student",
            student_id="STU-LOGIN-001",
            email="login.student@test.com",
            password_hash=generate_password_hash("CorrectPassword123!"),
            role="STUDENT"
        )
        db.session.add(user)
        db.session.commit()

    response = client.post("/api/auth/login", json={
        "email": "login.student@test.com",
        "password": "CorrectPassword123!"
    })

    assert response.status_code == 200
    data = response.get_json()
    assert data["success"] is True
    assert data["access_token"]
    assert data["user"]["email"] == "login.student@test.com"


def test_login_invalid_password(client, app):
    with app.app_context():
        user = User(
            name="Invalid Login Student",
            student_id="STU-LOGIN-002",
            email="invalid.login@test.com",
            password_hash=generate_password_hash("CorrectPassword123!"),
            role="STUDENT"
        )
        db.session.add(user)
        db.session.commit()

    response = client.post("/api/auth/login", json={
        "email": "invalid.login@test.com",
        "password": "WrongPassword123!"
    })

    assert response.status_code == 401
    data = response.get_json()
    assert data["success"] is False
    assert data["message"] == "Invalid email or password"


def test_protected_endpoint_requires_authentication(client):
    response = client.get("/api/protected")

    assert response.status_code == 401


def test_register_missing_body(client):
    response = client.post(
        "/api/auth/register",
        data="",
        content_type="application/json"
    )

    assert response.status_code == 400


def test_register_missing_required_fields(client):
    response = client.post("/api/auth/register", json={
        "name": "Incomplete Student",
        "email": "incomplete@test.com"
    })

    assert response.status_code == 400
    data = response.get_json()
    assert data["success"] is False
    assert data["message"] == "Name, email and password are required"


def test_register_duplicate_student_id(client, student):
    response = client.post("/api/auth/register", json={
        "name": "Another Student",
        "student_id": "TEST-STU-001",
        "email": "another.student@test.com",
        "password": "TestPassword123!"
    })

    assert response.status_code == 409
    data = response.get_json()
    assert data["success"] is False
    assert data["message"] == "Student ID already registered"


def test_login_missing_body(client):
    response = client.post(
        "/api/auth/login",
        data="",
        content_type="application/json"
    )

    assert response.status_code == 400


def test_login_missing_required_fields(client):
    response = client.post("/api/auth/login", json={
        "email": "missing.password@test.com"
    })

    assert response.status_code == 400
    data = response.get_json()
    assert data["success"] is False
    assert data["message"] == "Email and password are required"


def test_protected_endpoint_with_authentication(client, app, student):
    from flask_jwt_extended import create_access_token

    with app.app_context():
        token = create_access_token(identity=str(student))

    response = client.get(
        "/api/protected",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    data = response.get_json()
    assert data["success"] is True
    assert data["message"] == "Access granted"
    assert data["user_id"] == str(student)