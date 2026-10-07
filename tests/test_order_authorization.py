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


def test_operator_can_read_orders():
    response = client.get(
        "/api/orders/",
        headers=get_headers("operator", "Admin123!"),
    )

    assert response.status_code == 200


def test_operator_can_read_order_summary():
    response = client.get(
        "/api/orders/summary",
        headers=get_headers("operator", "Admin123!"),
    )

    assert response.status_code == 200


def test_operator_can_read_order_by_status():
    response = client.get(
        "/api/orders/status/PRODUCING",
        headers=get_headers("operator", "Admin123!"),
    )

    assert response.status_code == 200


def test_operator_cannot_create_order():
    response = client.post(
        "/api/orders/",
        json={
            "order_number": "ORD-AUTH-001",
            "customer_name": "Authorization Test",
            "product_id": 1,
            "quantity": 1000,
            "order_date": "2026-10-05",
            "delivery_date": "2026-10-15",
            "status": "PENDING",
            "unit_price": 85.50,
        },
        headers=get_headers("operator", "Admin123!"),
    )

    assert response.status_code == 403


def test_operator_cannot_update_order():
    response = client.put(
        "/api/orders/1",
        json={
            "customer_name": "Unauthorized Update",
        },
        headers=get_headers("operator", "Admin123!"),
    )

    assert response.status_code == 403


def test_operator_cannot_delete_order():
    response = client.delete(
        "/api/orders/1",
        headers=get_headers("operator", "Admin123!"),
    )

    assert response.status_code == 403
