import pytest
from flask_jwt_extended import create_access_token


def admin_token(app, admin):
    with app.app_context():
        return create_access_token(
            identity=str(admin),
            additional_claims={"role": "ADMIN"}
        )


def student_token(app, student):
    with app.app_context():
        return create_access_token(
            identity=str(student),
            additional_claims={"role": "STUDENT"}
        )


def test_get_resources(client, resource):
    response = client.get("/api/resources")

    assert response.status_code == 200
    data = response.get_json()
    assert data["success"] is True
    assert len(data["resources"]) == 1
    assert data["resources"][0]["name"] == "Pytest Study Room"


def test_get_resource_success(client, resource):
    response = client.get(f"/api/resources/{resource}")

    assert response.status_code == 200
    data = response.get_json()
    assert data["success"] is True
    assert data["resource"]["id"] == resource


def test_get_resource_not_found(client):
    response = client.get("/api/resources/9999")

    assert response.status_code == 404
    assert response.get_json()["success"] is False


def test_create_resource_success(client):
    response = client.post("/api/resources", json={
        "name": "Pytest Computer Lab",
        "type": "LABORATORY",
        "description": "Testing laboratory",
        "location": "Engineering Block",
        "capacity": 30
    })

    assert response.status_code == 201
    data = response.get_json()
    assert data["success"] is True
    assert data["resource"]["type"] == "LABORATORY"
    assert data["resource"]["status"] == "AVAILABLE"


@pytest.mark.parametrize("payload", [
    {},
    {"name": "Missing Type", "location": "Block", "capacity": 5},
    {"name": "Missing Location", "type": "STUDY_ROOM", "capacity": 5},
    {"name": "Missing Capacity", "type": "STUDY_ROOM", "location": "Block"}
])
def test_create_resource_missing_required_fields(client, payload):
    response = client.post("/api/resources", json=payload)
    assert response.status_code == 400


def test_create_resource_invalid_type(client):
    response = client.post("/api/resources", json={
        "name": "Invalid Resource",
        "type": "INVALID",
        "location": "Block",
        "capacity": 5
    })

    assert response.status_code == 400
    assert response.get_json()["message"] == "Invalid resource type"


@pytest.mark.parametrize("capacity", [0, -1, 1.5, "10"])
def test_create_resource_invalid_capacity(client, capacity):
    response = client.post("/api/resources", json={
        "name": "Invalid Capacity",
        "type": "STUDY_ROOM",
        "location": "Block",
        "capacity": capacity
    })

    assert response.status_code == 400


def test_update_resource_requires_authentication(client, resource):
    response = client.put(
        f"/api/admin/resources/{resource}",
        json={"name": "Updated Room"}
    )

    assert response.status_code == 401


def test_update_resource_student_forbidden(client, app, student, resource):
    token = student_token(app, student)

    response = client.put(
        f"/api/admin/resources/{resource}",
        headers={"Authorization": f"Bearer {token}"},
        json={"name": "Updated Room"}
    )

    assert response.status_code == 403


def test_update_resource_success(client, app, admin, resource):
    token = admin_token(app, admin)

    response = client.put(
        f"/api/admin/resources/{resource}",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "name": "Updated Study Room",
            "capacity": 20,
            "status": "UNAVAILABLE"
        }
    )

    assert response.status_code == 200
    data = response.get_json()
    assert data["success"] is True
    assert data["resource"]["name"] == "Updated Study Room"
    assert data["resource"]["capacity"] == 20
    assert data["resource"]["status"] == "UNAVAILABLE"


def test_delete_resource_requires_admin(client, app, student, resource):
    token = student_token(app, student)

    response = client.delete(
        f"/api/admin/resources/{resource}",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 403


def test_delete_resource_success(client, app, admin, resource):
    token = admin_token(app, admin)

    response = client.delete(
        f"/api/admin/resources/{resource}",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    assert response.get_json()["success"] is True
    assert client.get(f"/api/resources/{resource}").status_code == 404

def test_update_resource_not_found(client, app, admin):
    token = admin_token(app, admin)
    response = client.put('/api/admin/resources/9999', headers={'Authorization': f'Bearer {token}'}, json={'name': 'Missing Resource'})
    assert response.status_code == 404
    assert response.get_json()['success'] is False


def test_update_resource_missing_body(client, app, admin, resource):
    token = admin_token(app, admin)
    response = client.put(f'/api/admin/resources/{resource}', headers={'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}, data='null')
    assert response.status_code == 400
    assert response.get_json()['message'] == 'Request body is required'


@pytest.mark.parametrize('resource_type', ['INVALID', '', 'LAB'])
def test_update_resource_invalid_type(client, app, admin, resource, resource_type):
    token = admin_token(app, admin)
    response = client.put(f'/api/admin/resources/{resource}', headers={'Authorization': f'Bearer {token}'}, json={'type': resource_type})
    assert response.status_code == 400
    assert response.get_json()['message'] == 'Invalid resource type'


def test_update_resource_valid_type(client, app, admin, resource):
    token = admin_token(app, admin)

    response = client.put(
        f"/api/admin/resources/{resource}",
        headers={"Authorization": f"Bearer {token}"},
        json={"type": "EQUIPMENT"}
    )

    assert response.status_code == 200
    assert response.get_json()["resource"]["type"] == "EQUIPMENT"


def test_update_resource_description_and_location(client, app, admin, resource):
    token = admin_token(app, admin)
    response = client.put(f'/api/admin/resources/{resource}', headers={'Authorization': f'Bearer {token}'}, json={'description': 'Updated description', 'location': 'Updated location'})
    assert response.status_code == 200
    data = response.get_json()
    assert data['resource']['description'] == 'Updated description'
    assert data['resource']['location'] == 'Updated location'


@pytest.mark.parametrize('capacity', [0, -1, 1.5, '20'])
def test_update_resource_invalid_capacity(client, app, admin, resource, capacity):
    token = admin_token(app, admin)
    response = client.put(f'/api/admin/resources/{resource}', headers={'Authorization': f'Bearer {token}'}, json={'capacity': capacity})
    assert response.status_code == 400
    assert response.get_json()['message'] == 'Capacity must be a positive integer'


def test_update_resource_invalid_status(client, app, admin, resource):
    token = admin_token(app, admin)
    response = client.put(f'/api/admin/resources/{resource}', headers={'Authorization': f'Bearer {token}'}, json={'status': 'INVALID'})
    assert response.status_code == 400
    assert response.get_json()['message'] == 'Invalid resource status'


def test_delete_resource_not_found(client, app, admin):
    token = admin_token(app, admin)
    response = client.delete('/api/admin/resources/9999', headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 404
    assert response.get_json()['success'] is False
