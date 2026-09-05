from datetime import date, time

from flask_jwt_extended import create_access_token

from app import db
from app.models import CheckIn, Reservation
from app.models.user import User


def admin_token(app, user_id):
    with app.app_context():
        return create_access_token(
            identity=str(user_id),
            additional_claims={"role": "ADMIN"}
        )


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
            purpose="Admin testing",
            status=status
        )
        db.session.add(reservation)
        db.session.commit()
        return reservation.id


def test_get_all_reservations_requires_authentication(client):
    response = client.get("/api/admin/reservations")

    assert response.status_code == 401


def test_get_all_reservations_student_forbidden(
    client, app, student
):
    token = student_token(app, student)

    response = client.get(
        "/api/admin/reservations",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 403
    assert response.get_json()["message"] == "Admin access required"


def test_get_all_reservations_success(
    client, app, admin, student, resource
):
    reservation_id = create_reservation(
        app, student, resource
    )
    token = admin_token(app, admin)

    response = client.get(
        "/api/admin/reservations",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    data = response.get_json()
    assert data["success"] is True
    assert len(data["reservations"]) == 1
    assert data["reservations"][0]["id"] == reservation_id
    assert data["reservations"][0]["user_id"] == student
    assert data["reservations"][0]["resource_id"] == resource
    assert data["reservations"][0]["status"] == "CONFIRMED"


def test_get_all_check_ins_requires_authentication(client):
    response = client.get("/api/admin/check-ins")

    assert response.status_code == 401


def test_get_all_check_ins_student_forbidden(
    client, app, student
):
    token = student_token(app, student)

    response = client.get(
        "/api/admin/check-ins",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 403
    assert response.get_json()["message"] == "Admin access required"


def test_get_all_check_ins_success(
    client, app, admin, student, resource
):
    reservation_id = create_reservation(
        app, student, resource
    )

    with app.app_context():
        check_in = CheckIn(
            reservation_id=reservation_id,
            qr_token="pytest-admin-check-in-token",
            status="NOT_CHECKED_IN"
        )
        db.session.add(check_in)
        db.session.commit()
        check_in_id = check_in.id

    token = admin_token(app, admin)

    response = client.get(
        "/api/admin/check-ins",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    data = response.get_json()
    assert data["success"] is True
    assert len(data["check_ins"]) == 1
    assert data["check_ins"][0]["id"] == check_in_id
    assert data["check_ins"][0]["reservation_id"] == reservation_id
    assert data["check_ins"][0]["qr_token"] == "pytest-admin-check-in-token"
    assert data["check_ins"][0]["status"] == "NOT_CHECKED_IN"
    assert data["check_ins"][0]["checked_in_at"] is None


def test_get_all_users_requires_authentication(client):
    response = client.get("/api/admin/users")

    assert response.status_code == 401


def test_get_all_users_student_forbidden(
    client, app, student
):
    token = student_token(app, student)

    response = client.get(
        "/api/admin/users",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 403
    assert response.get_json()["message"] == "Admin access required"


def test_get_all_users_success(client, app, admin, student):
    token = admin_token(app, admin)

    response = client.get(
        "/api/admin/users",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    data = response.get_json()
    assert data["success"] is True
    assert len(data["users"]) == 2

    user_ids = [user["id"] for user in data["users"]]
    assert user_ids == sorted(user_ids)

    student_data = next(
        user for user in data["users"] if user["id"] == student
    )
    assert student_data["name"] == "Test Student"
    assert student_data["student_id"] == "TEST-STU-001"
    assert student_data["email"] == "pytest.student@test.com"
    assert student_data["role"] == "STUDENT"


def test_update_resource_status_requires_authentication(
    client, resource
):
    response = client.put(
        f"/api/admin/resources/{resource}/status",
        json={"status": "UNAVAILABLE"}
    )

    assert response.status_code == 401


def test_update_resource_status_student_forbidden(
    client, app, student, resource
):
    token = student_token(app, student)

    response = client.put(
        f"/api/admin/resources/{resource}/status",
        headers={"Authorization": f"Bearer {token}"},
        json={"status": "UNAVAILABLE"}
    )

    assert response.status_code == 403
    assert response.get_json()["message"] == "Admin access required"


def test_update_resource_status_not_found(
    client, app, admin
):
    token = admin_token(app, admin)

    response = client.put(
        "/api/admin/resources/9999/status",
        headers={"Authorization": f"Bearer {token}"},
        json={"status": "UNAVAILABLE"}
    )

    assert response.status_code == 404
    assert response.get_json()["message"] == "Resource not found"


def test_update_resource_status_requires_status(
    client, app, admin, resource
):
    token = admin_token(app, admin)

    response = client.put(
        f"/api/admin/resources/{resource}/status",
        headers={"Authorization": f"Bearer {token}"},
        json={}
    )

    assert response.status_code == 400
    assert response.get_json()["message"] == "Status is required"


def test_update_resource_status_invalid_status(
    client, app, admin, resource
):
    token = admin_token(app, admin)

    response = client.put(
        f"/api/admin/resources/{resource}/status",
        headers={"Authorization": f"Bearer {token}"},
        json={"status": "INVALID"}
    )

    assert response.status_code == 400
    assert response.get_json()["message"] == "Invalid resource status"


def test_update_resource_status_success(
    client, app, admin, resource
):
    token = admin_token(app, admin)

    response = client.put(
        f"/api/admin/resources/{resource}/status",
        headers={"Authorization": f"Bearer {token}"},
        json={"status": "UNAVAILABLE"}
    )

    assert response.status_code == 200
    data = response.get_json()
    assert data["success"] is True
    assert data["message"] == "Resource status updated successfully"
    assert data["resource"]["id"] == resource
    assert data["resource"]["status"] == "UNAVAILABLE"

    with app.app_context():
        updated_resource = db.session.get(
            __import__("app.models.resource", fromlist=["Resource"]).Resource,
            resource
        )
        assert updated_resource.status == "UNAVAILABLE"