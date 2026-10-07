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


def test_operator_can_read_machine_performance_report():
    response = client.get(
        "/api/reports/machine-performance",
        headers=get_headers("operator", "Admin123!"),
    )

    assert response.status_code == 200


def test_unauthenticated_user_cannot_read_machine_performance_report():
    response = client.get(
        "/api/reports/machine-performance"
    )

    assert response.status_code in (401, 403)
