from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def get_headers(username: str, password: str):
    response = client.post(
        "/api/auth/login",
        json={
            "username": username,
            "password": password,
        },
    )

    assert response.status_code == 200

    token = response.json()["access_token"]

    return {
        "Authorization": f"Bearer {token}"
    }


def test_operator_can_read_machines():
    response = client.get(
        "/api/machines/",
        headers=get_headers("operator", "Admin123!"),
    )

    assert response.status_code == 200


def test_operator_can_read_machine_detail():
    response = client.get(
        "/api/machines/1",
        headers=get_headers("operator", "Admin123!"),
    )

    assert response.status_code == 200


def test_operator_cannot_create_machine():
    response = client.post(
        "/api/machines/",
        json={
            "code": "EXT-AUTH-01",
            "name": "Authorization Test Machine",
            "type": "Extruder",
            "line": "Test Line",
            "status": "stopped",
            "capacity_per_hour": 1000,
            "active": True,
        },
        headers=get_headers("operator", "Admin123!"),
    )

    assert response.status_code == 403


def test_operator_cannot_update_machine():
    response = client.put(
        "/api/machines/1",
        json={
            "status": "maintenance",
        },
        headers=get_headers("operator", "Admin123!"),
    )

    assert response.status_code == 403


def test_operator_cannot_delete_machine():
    response = client.delete(
        "/api/machines/1",
        headers=get_headers("operator", "Admin123!"),
    )

    assert response.status_code == 403
