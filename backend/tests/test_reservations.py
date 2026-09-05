import pytest
from datetime import date, time

from flask_jwt_extended import create_access_token

from app import db
from app.models.reservation import Reservation


def student_token(app, student):
    with app.app_context():
        return create_access_token(
            identity=str(student),
            additional_claims={"role": "STUDENT"}
        )


def admin_token(app, admin):
    with app.app_context():
        return create_access_token(
            identity=str(admin),
            additional_claims={"role": "ADMIN"}
        )


def create_test_reservation(app, student, resource, status="CONFIRMED"):
    with app.app_context():
        reservation = Reservation(
            user_id=student,
            resource_id=resource,
            reservation_date=date(2026, 9, 10),
            start_time=time(9, 0),
            end_time=time(11, 0),
            purpose="Pytest reservation",
            status=status
        )
        db.session.add(reservation)
        db.session.commit()
        return reservation.id


def test_create_reservation_requires_authentication(client, resource):
    response = client.post("/api/reservations", json={
        "resource_id": resource,
        "reservation_date": "2026-09-10",
        "start_time": "09:00",
        "end_time": "11:00"
    })

    assert response.status_code == 401


def test_create_reservation_success(client, app, student, resource):
    token = student_token(app, student)

    response = client.post(
        "/api/reservations",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "resource_id": resource,
            "reservation_date": "2026-09-10",
            "start_time": "09:00",
            "end_time": "11:00",
            "purpose": "Software engineering project"
        }
    )

    assert response.status_code == 201
    data = response.get_json()

    assert data["success"] is True
    assert data["reservation"]["user_id"] == student
    assert data["reservation"]["resource_id"] == resource
    assert data["reservation"]["reservation_date"] == "2026-09-10"
    assert data["reservation"]["start_time"] == "09:00"
    assert data["reservation"]["end_time"] == "11:00"
    assert data["reservation"]["purpose"] == "Software engineering project"
    assert data["reservation"]["status"] == "CONFIRMED"


@pytest.mark.parametrize("payload", [
    {},
    {
        "resource_id": 1,
        "start_time": "09:00",
        "end_time": "11:00"
    },
    {
        "resource_id": 1,
        "reservation_date": "2026-09-10",
        "end_time": "11:00"
    },
    {
        "resource_id": 1,
        "reservation_date": "2026-09-10",
        "start_time": "09:00"
    },
])
def test_create_reservation_missing_required_fields(
    client, app, student, payload
):
    token = student_token(app, student)

    response = client.post(
        "/api/reservations",
        headers={"Authorization": f"Bearer {token}"},
        json=payload
    )

    assert response.status_code == 400
    assert response.get_json()["success"] is False


def test_create_reservation_requires_integer_resource_id(
    client, app, student
):
    token = student_token(app, student)

    response = client.post(
        "/api/reservations",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "resource_id": "1",
            "reservation_date": "2026-09-10",
            "start_time": "09:00",
            "end_time": "11:00"
        }
    )

    assert response.status_code == 400
    assert response.get_json()["message"] == "Resource ID must be an integer"


def test_create_reservation_resource_not_found(client, app, student):
    token = student_token(app, student)

    response = client.post(
        "/api/reservations",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "resource_id": 9999,
            "reservation_date": "2026-09-10",
            "start_time": "09:00",
            "end_time": "11:00"
        }
    )

    assert response.status_code == 404
    assert response.get_json()["message"] == "Resource not found"


def test_create_reservation_unavailable_resource(
    client, app, student, resource
):
    token = student_token(app, student)

    with app.app_context():
        from app.models.resource import Resource

        item = db.session.get(Resource, resource)
        item.status = "UNAVAILABLE"
        db.session.commit()

    response = client.post(
        "/api/reservations",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "resource_id": resource,
            "reservation_date": "2026-09-10",
            "start_time": "09:00",
            "end_time": "11:00"
        }
    )

    assert response.status_code == 400
    assert response.get_json()["message"] == "Resource is unavailable"


@pytest.mark.parametrize("reservation_date,start_time,end_time", [
    ("10-09-2026", "09:00", "11:00"),
    ("2026-09-10", "09:00", "11:00:00"),
])
def test_create_reservation_invalid_date_or_time_format(
    client, app, student, resource,
    reservation_date, start_time, end_time
):
    token = student_token(app, student)

    response = client.post(
        "/api/reservations",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "resource_id": resource,
            "reservation_date": reservation_date,
            "start_time": start_time,
            "end_time": end_time
        }
    )

    assert response.status_code == 400
    assert response.get_json()["message"] == (
        "Invalid date or time format. Use YYYY-MM-DD and HH:MM"
    )


def test_create_reservation_start_time_must_be_before_end_time(
    client, app, student, resource
):
    token = student_token(app, student)

    response = client.post(
        "/api/reservations",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "resource_id": resource,
            "reservation_date": "2026-09-10",
            "start_time": "11:00",
            "end_time": "09:00"
        }
    )

    assert response.status_code == 400
    assert response.get_json()["message"] == (
        "Start time must be before end time"
    )


def test_get_reservations_requires_authentication(client):
    response = client.get("/api/reservations")

    assert response.status_code == 401


def test_get_reservations_returns_current_users_reservations(
    client, app, student, resource
):
    token = student_token(app, student)

    reservation_id = create_test_reservation(
        app, student, resource
    )

    response = client.get(
        "/api/reservations",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    data = response.get_json()

    assert data["success"] is True
    assert len(data["reservations"]) == 1
    assert data["reservations"][0]["id"] == reservation_id
    assert data["reservations"][0]["user_id"] == student


def test_get_reservation_requires_authentication(client, resource):
    response = client.get(f"/api/reservations/{resource}")

    assert response.status_code == 401


def test_get_reservation_success(client, app, student, resource):
    token = student_token(app, student)

    reservation_id = create_test_reservation(
        app, student, resource
    )

    response = client.get(
        f"/api/reservations/{reservation_id}",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    data = response.get_json()

    assert data["success"] is True
    assert data["reservation"]["id"] == reservation_id
    assert data["reservation"]["user_id"] == student
    assert data["reservation"]["resource_id"] == resource


def test_get_reservation_not_found(client, app, student):
    token = student_token(app, student)

    response = client.get(
        "/api/reservations/9999",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 404
    assert response.get_json()["message"] == "Reservation not found"


def test_get_reservation_denies_other_user(
    client, app, student, resource
):
    token = student_token(app, student)

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

    reservation_id = create_test_reservation(
        app, other_student_id, resource
    )

    response = client.get(
        f"/api/reservations/{reservation_id}",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 403
    assert response.get_json()["message"] == "Access denied"


def test_cancel_reservation_requires_authentication(client, resource):
    response = client.delete(f"/api/reservations/{resource}")

    assert response.status_code == 401


def test_cancel_reservation_success(client, app, student, resource):
    token = student_token(app, student)

    reservation_id = create_test_reservation(
        app, student, resource
    )

    response = client.delete(
        f"/api/reservations/{reservation_id}",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    data = response.get_json()

    assert data["success"] is True
    assert data["reservation"]["id"] == reservation_id
    assert data["reservation"]["status"] == "CANCELLED"


def test_cancel_reservation_not_found(client, app, student):
    token = student_token(app, student)

    response = client.delete(
        "/api/reservations/9999",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 404
    assert response.get_json()["message"] == "Reservation not found"


def test_cancel_reservation_denies_other_user(
    client, app, student, resource
):
    token = student_token(app, student)

    with app.app_context():
        from app.models.user import User

        other_student = User(
            name="Other Student",
            student_id="OTHER-STU-002",
            email="other.student2@test.com",
            password_hash="test-password-hash",
            role="STUDENT"
        )
        db.session.add(other_student)
        db.session.commit()
        other_student_id = other_student.id

    reservation_id = create_test_reservation(
        app, other_student_id, resource
    )

    response = client.delete(
        f"/api/reservations/{reservation_id}",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 403
    assert response.get_json()["message"] == "Access denied"


def test_cancel_reservation_already_cancelled(
    client, app, student, resource
):
    token = student_token(app, student)

    reservation_id = create_test_reservation(
        app, student, resource, status="CANCELLED"
    )

    response = client.delete(
        f"/api/reservations/{reservation_id}",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 400
    assert response.get_json()["message"] == "Reservation is already cancelled"


def test_admin_update_status_requires_authentication(client, resource):
    response = client.put(
        f"/api/admin/reservations/{resource}/status",
        json={"status": "COMPLETED"}
    )

    assert response.status_code == 401


def test_admin_update_status_student_forbidden(
    client, app, student, resource
):
    token = student_token(app, student)

    reservation_id = create_test_reservation(
        app, student, resource
    )

    response = client.put(
        f"/api/admin/reservations/{reservation_id}/status",
        headers={"Authorization": f"Bearer {token}"},
        json={"status": "COMPLETED"}
    )

    assert response.status_code == 403
    assert response.get_json()["message"] == "Admin access required"


def test_admin_update_status_success(
    client, app, student, admin, resource
):
    token = admin_token(app, admin)

    reservation_id = create_test_reservation(
        app, student, resource
    )

    response = client.put(
        f"/api/admin/reservations/{reservation_id}/status",
        headers={"Authorization": f"Bearer {token}"},
        json={"status": "COMPLETED"}
    )

    assert response.status_code == 200
    data = response.get_json()

    assert data["success"] is True
    assert data["reservation"]["id"] == reservation_id
    assert data["reservation"]["status"] == "COMPLETED"


def test_admin_update_status_not_found(client, app, admin):
    token = admin_token(app, admin)

    response = client.put(
        "/api/admin/reservations/9999/status",
        headers={"Authorization": f"Bearer {token}"},
        json={"status": "COMPLETED"}
    )

    assert response.status_code == 404
    assert response.get_json()["message"] == "Reservation not found"


def test_admin_update_status_requires_body(
    client, app, admin, student, resource
):
    token = admin_token(app, admin)

    reservation_id = create_test_reservation(
        app, student, resource
    )

    response = client.put(
        f"/api/admin/reservations/{reservation_id}/status",
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
    )

    assert response.status_code == 400
    assert response.get_json() is None

@pytest.mark.parametrize("status", [
    "INVALID",
    "",
    "approved",
    None
])
def test_admin_update_status_invalid(
    client, app, admin, student, resource, status
):
    token = admin_token(app, admin)

    reservation_id = create_test_reservation(
        app, student, resource
    )

    response = client.put(
        f"/api/admin/reservations/{reservation_id}/status",
        headers={"Authorization": f"Bearer {token}"},
        json={"status": status}
    )

    assert response.status_code == 400
    assert response.get_json()["message"] == "Invalid reservation status" 
