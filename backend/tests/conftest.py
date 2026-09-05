import pytest

from app import create_app, db
from app.models.user import User
from app.models.resource import Resource


@pytest.fixture
def app():
    app = create_app({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "JWT_SECRET_KEY": "test-jwt-secret-key-must-be-at-least-32-bytes"
    })

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def student(app):
    with app.app_context():
        user = User(
            name="Test Student",
            student_id="TEST-STU-001",
            email="pytest.student@test.com",
            password_hash="test-password-hash",
            role="STUDENT"
        )
        db.session.add(user)
        db.session.commit()
        return user.id


@pytest.fixture
def admin(app):
    with app.app_context():
        user = User(
            name="Test Admin",
            student_id="TEST-ADM-001",
            email="pytest.admin@test.com",
            password_hash="test-password-hash",
            role="ADMIN"
        )
        db.session.add(user)
        db.session.commit()
        return user.id


@pytest.fixture
def resource(app):
    with app.app_context():
        item = Resource(
            name="Pytest Study Room",
            type="STUDY_ROOM",
            description="Test resource",
            location="Test Building",
            capacity=10,
            status="AVAILABLE"
        )
        db.session.add(item)
        db.session.commit()
        return item.id