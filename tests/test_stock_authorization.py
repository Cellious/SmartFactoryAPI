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
        "Authorization": f"Bearer {token}",
    }


def test_operator_can_read_stock_movements():
    response = client.get(
        "/api/stock/movements",
        headers=get_headers("operator", "Admin123!"),
    )

    assert response.status_code == 200


def test_operator_can_read_stock_balances():
    response = client.get(
        "/api/stock/balances",
        headers=get_headers("operator", "Admin123!"),
    )

    assert response.status_code == 200


def test_operator_can_read_stock_value():
    response = client.get(
        "/api/stock/value",
        headers=get_headers("operator", "Admin123!"),
    )

    assert response.status_code == 200


def test_operator_cannot_create_stock_movement():
    response = client.post(
        "/api/stock/movements",
        json={
            "product_id": 1,
            "movement_type": "IN",
            "quantity": 500,
            "reason": "Authorization Test",
            "movement_date": "2026-10-05",
        },
        headers=get_headers("operator", "Admin123!"),
    )

    assert response.status_code == 403
