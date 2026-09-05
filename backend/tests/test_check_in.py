from datetime import date, time

from flask_jwt_extended import create_access_token

from app import db
from app.models import Reservation


def student_token(app, user_id):
    with app.app_context():
        return create_access_token(
            identity=str(user_id),
            additional_claims={"role": "STUDENT"}
        )


def create_reservation(app, user_id, resource_id, status="CONFIRMED"):
    with app.app_context():
        reservation = Reservation(
            user_id=user_id,
            resource_id=resource_id,
            reservation_date=date(2026, 9, 10),
            start_time=time(9, 0),
            end_time=time(11, 0),
            purpose="Check-in testing",
            status=status
        )
        db.session.add(reservation)
        db.session.commit()
        return reservation.id


def test_generate_check_in_requires_authentication(client, student, resource):
    reservation_id = create_reservation(
        client.application, student, resource
    )

    response = client.post(
        f"/api/reservations/{reservation_id}/check-in"
    )

    assert response.status_code == 401


def test_generate_check_in_success(client, app, student, resource):
    reservation_id = create_reservation(app, student, resource)
    token = student_token(app, student)

    response = client.post(
        f"/api/reservations/{reservation_id}/check-in",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 201
    data = response.get_json()
    assert data["success"] is True
    assert data["message"] == "Check-in token generated successfully"
    assert data["check_in"]["reservation_id"] == reservation_id
    assert data["check_in"]["qr_token"]
    assert data["check_in"]["status"] == "NOT_CHECKED_IN"
    assert data["check_in"]["checked_in_at"] is None


def test_generate_check_in_returns_existing_token(client, app, student, resource):
    reservation_id = create_reservation(app, student, resource)
    token = student_token(app, student)

    first_response = client.post(
        f"/api/reservations/{reservation_id}/check-in",
        headers={"Authorization": f"Bearer {token}"}
    )
    first_data = first_response.get_json()
    first_qr_token = first_data["check_in"]["qr_token"]

    second_response = client.post(
        f"/api/reservations/{reservation_id}/check-in",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert second_response.status_code == 200
    second_data = second_response.get_json()
    assert second_data["success"] is True
    assert second_data["message"] == "Check-in token already exists"
    assert second_data["check_in"]["qr_token"] == first_qr_token
    assert second_data["check_in"]["status"] == "NOT_CHECKED_IN"


def test_generate_check_in_reservation_not_found(client, app, student):
    token = student_token(app, student)

    response = client.post(
        "/api/reservations/9999/check-in",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 404
    data = response.get_json()
    assert data["success"] is False
    assert data["message"] == "Reservation not found"


def test_generate_check_in_other_users_reservation_forbidden(
    client, app, student, resource
):
    with app.app_context():
        from app.models.user import User

        other_student = User(
            name="Other Student",
            student_id="OTHER-STU-001",
            email="other.student@test.com",
            password_hash="test-password-hash",
            role="STUDENT"
        )
        db.session.add(other_student)
        db.session.commit()
        other_student_id = other_student.id

    reservation_id = create_reservation(
        app, other_student_id, resource
    )
    token = student_token(app, student)

    response = client.post(
        f"/api/reservations/{reservation_id}/check-in",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 403
    assert response.get_json()["message"] == "Access denied"


def test_generate_check_in_requires_confirmed_reservation(
    client, app, student, resource
):
    reservation_id = create_reservation(
        app, student, resource, status="CANCELLED"
    )
    token = student_token(app, student)

    response = client.post(
        f"/api/reservations/{reservation_id}/check-in",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 400
    assert response.get_json()["message"] == (
        "Only confirmed reservations can be checked in"
    )


def test_perform_check_in_requires_authentication(client):
    response = client.post("/api/check-in/invalid-token")

    assert response.status_code == 401


def test_perform_check_in_invalid_token(client, app, student):
    token = student_token(app, student)

    response = client.post(
        "/api/check-in/not-a-real-token",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 404
    assert response.get_json()["message"] == "Invalid check-in token"


def test_perform_check_in_success(client, app, student, resource):
    reservation_id = create_reservation(app, student, resource)
    auth_token = student_token(app, student)

    generate_response = client.post(
        f"/api/reservations/{reservation_id}/check-in",
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    qr_token = generate_response.get_json()["check_in"]["qr_token"]

    response = client.post(
        f"/api/check-in/{qr_token}",
        headers={"Authorization": f"Bearer {auth_token}"}
    )

    assert response.status_code == 200
    data = response.get_json()
    assert data["success"] is True
    assert data["message"] == "Check-in successful"
    assert data["check_in"]["reservation_id"] == reservation_id
    assert data["check_in"]["status"] == "CHECKED_IN"
    assert data["check_in"]["checked_in_at"]


def test_perform_check_in_duplicate_is_rejected(
    client, app, student, resource
):
    reservation_id = create_reservation(app, student, resource)
    auth_token = student_token(app, student)

    generate_response = client.post(
        f"/api/reservations/{reservation_id}/check-in",
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    qr_token = generate_response.get_json()["check_in"]["qr_token"]

    first_response = client.post(
        f"/api/check-in/{qr_token}",
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert first_response.status_code == 200

    second_response = client.post(
        f"/api/check-in/{qr_token}",
        headers={"Authorization": f"Bearer {auth_token}"}
    )

    assert second_response.status_code == 400
    assert second_response.get_json()["message"] == "Already checked in"


def test_perform_check_in_other_user_forbidden(
    client, app, student, resource
):
    with app.app_context():
        from app.models.user import User

        other_student = User(
            name="QR Owner",
            student_id="QR-OWNER-001",
            email="qr.owner@test.com",
            password_hash="test-password-hash",
            role="STUDENT"
        )
        db.session.add(other_student)
        db.session.commit()
        other_student_id = other_student.id

    reservation_id = create_reservation(
        app, other_student_id, resource
    )
    owner_token = student_token(app, other_student_id)

    generate_response = client.post(
        f"/api/reservations/{reservation_id}/check-in",
        headers={"Authorization": f"Bearer {owner_token}"}
    )
    qr_token = generate_response.get_json()["check_in"]["qr_token"]

    student_auth_token = student_token(app, student)

    response = client.post(
        f"/api/check-in/{qr_token}",
        headers={"Authorization": f"Bearer {student_auth_token}"}
    )

    assert response.status_code == 403
    assert response.get_json()["message"] == "Access denied"


def test_get_check_in_requires_authentication(client):
    response = client.get("/api/reservations/1/check-in")

    assert response.status_code == 401


def test_get_check_in_not_found_reservation(client, app, student):
    token = student_token(app, student)

    response = client.get(
        "/api/reservations/9999/check-in",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 404
    assert response.get_json()["message"] == "Reservation not found"


def test_get_check_in_record_not_found(client, app, student, resource):
    reservation_id = create_reservation(app, student, resource)
    token = student_token(app, student)

    response = client.get(
        f"/api/reservations/{reservation_id}/check-in",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 404
    assert response.get_json()["message"] == "Check-in record not found"


def test_get_check_in_other_user_forbidden(
    client, app, student, resource
):
    with app.app_context():
        from app.models.user import User

        other_student = User(
            name="GET Other Student",
            student_id="GET-OTHER-001",
            email="get.other@test.com",
            password_hash="test-password-hash",
            role="STUDENT"
        )
        db.session.add(other_student)
        db.session.commit()
        other_student_id = other_student.id

    reservation_id = create_reservation(
        app, other_student_id, resource
    )
    token = student_token(app, student)

    response = client.get(
        f"/api/reservations/{reservation_id}/check-in",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 403
    assert response.get_json()["message"] == "Access denied"


def test_get_check_in_success(client, app, student, resource):
    reservation_id = create_reservation(app, student, resource)
    token = student_token(app, student)

    generate_response = client.post(
        f"/api/reservations/{reservation_id}/check-in",
        headers={"Authorization": f"Bearer {token}"}
    )
    qr_token = generate_response.get_json()["check_in"]["qr_token"]

    response = client.get(
        f"/api/reservations/{reservation_id}/check-in",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    data = response.get_json()
    assert data["success"] is True
    assert data["check_in"]["reservation_id"] == reservation_id
    assert data["check_in"]["qr_token"] == qr_token
    assert data["check_in"]["status"] == "NOT_CHECKED_IN"
    assert data["check_in"]["checked_in_at"] is None


def test_perform_check_in_reservation_not_found(client, app, student, resource):
    from app.models import CheckIn

    token = student_token(app, student)

    with app.app_context():
        reservation_id = create_reservation(app, student, resource)

        check_in = CheckIn(
            reservation_id=reservation_id,
            qr_token="orphaned-qr-token",
            status="NOT_CHECKED_IN"
        )
        db.session.add(check_in)
        db.session.commit()

        db.session.delete(
            db.session.get(Reservation, reservation_id)
        )
        db.session.commit()

    response = client.post(
        "/api/check-in/orphaned-qr-token",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 404
    data = response.get_json()
    assert data["success"] is False
    assert data["message"] == "Reservation not found"


def test_perform_check_in_requires_confirmed_reservation(
    client, app, student, resource
):
    from app.models import CheckIn

    reservation_id = create_reservation(
        app, student, resource, status="CANCELLED"
    )
    token = student_token(app, student)

    with app.app_context():
        check_in = CheckIn(
            reservation_id=reservation_id,
            qr_token="cancelled-reservation-token",
            status="NOT_CHECKED_IN"
        )
        db.session.add(check_in)
        db.session.commit()

    response = client.post(
        "/api/check-in/cancelled-reservation-token",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 400
    data = response.get_json()
    assert data["success"] is False
    assert data["message"] == (
        "Only confirmed reservations can be checked in"
    )