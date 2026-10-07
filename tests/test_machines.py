from app.database.fake_db import machines
from app.main import app
from fastapi.testclient import TestClient


client = TestClient(app)


def get_admin_headers():
    response = client.post(
        "/api/auth/login",
        json={
            "username": "admin",
            "password": "Admin123!",
        },
    )

    assert response.status_code == 200

    token = response.json()["access_token"]

    return {
        "Authorization": f"Bearer {token}"
    }


def setup_function():
    machines.clear()

    machines.extend(
        [
            {
                "id": 1,
                "code": "EXT-01",
                "name": "Ekstruder 01",
                "type": "Extruder",
                "line": "PVC Line 1",
                "status": "running",
                "capacity_per_hour": 1500,
                "active": True,
            },
            {
                "id": 2,
                "code": "EXT-02",
                "name": "Ekstruder 02",
                "type": "Extruder",
                "line": "PVC Line 2",
                "status": "running",
                "capacity_per_hour": 1800,
                "active": True,
            },
            {
                "id": 3,
                "code": "EXT-03",
                "name": "Ekstruder 03",
                "type": "Extruder",
                "line": "PVC Line 3",
                "status": "maintenance",
                "capacity_per_hour": 1400,
                "active": True,
            },
            {
                "id": 4,
                "code": "CUT-01",
                "name": "Kesim Makinesi 01",
                "type": "Cutting",
                "line": "Cutting Line 1",
                "status": "stopped",
                "capacity_per_hour": 2200,
                "active": True,
            },
        ]
    )


def test_list_machines():
    response = client.get(
        "/api/machines/",
        headers=get_admin_headers(),
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 4
    assert data[0]["code"] == "EXT-01"


def test_get_machine_by_id():
    response = client.get(
        "/api/machines/1",
        headers=get_admin_headers(),
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == 1
    assert data["code"] == "EXT-01"
    assert data["status"] == "running"


def test_get_machine_not_found():
    response = client.get(
        "/api/machines/999",
        headers=get_admin_headers(),
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Machine not found"


def test_create_machine():
    new_machine = {
        "code": "EXT-04",
        "name": "Ekstruder 04",
        "type": "Extruder",
        "line": "PVC Line 4",
        "status": "running",
        "capacity_per_hour": 1600,
        "active": True,
    }

    response = client.post(
        "/api/machines/",
        json=new_machine,
        headers=get_admin_headers(),
    )

    assert response.status_code == 201

    data = response.json()

    assert data["id"] == 5
    assert data["code"] == "EXT-04"


def test_update_machine():
    response = client.put(
        "/api/machines/3",
        json={
            "status": "running",
            "capacity_per_hour": 1500,
        },
        headers=get_admin_headers(),
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == 3
    assert data["status"] == "running"
    assert data["capacity_per_hour"] == 1500


def test_update_machine_not_found():
    response = client.put(
        "/api/machines/999",
        json={
            "status": "running",
        },
        headers=get_admin_headers(),
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Machine not found"


def test_delete_machine():
    response = client.delete(
        "/api/machines/4",
        headers=get_admin_headers(),
    )

    assert response.status_code == 200

    data = response.json()

    assert data["message"] == "Machine deleted successfully"
    assert data["machine_id"] == 4

    get_response = client.get(
        "/api/machines/4",
        headers=get_admin_headers(),
    )

    assert get_response.status_code == 404


def test_delete_machine_not_found():
    response = client.delete(
        "/api/machines/999",
        headers=get_admin_headers(),
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Machine not found"
