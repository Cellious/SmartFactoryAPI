from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def get_token(username: str, password: str):
    response = client.post(
        "/api/auth/login",
        json={
            "username": username,
            "password": password,
        },
    )

    assert response.status_code == 200

    return response.json()["access_token"]


def get_headers(username: str, password: str):
    token = get_token(username, password)

    return {
        "Authorization": f"Bearer {token}",
    }


def test_operator_can_read_products():
    response = client.get(
        "/api/products/",
        headers=get_headers("operator", "Admin123!"),
    )

    assert response.status_code == 200


def test_operator_cannot_create_product():
    response = client.post(
        "/api/products/",
        json={
            "code": "PRD-TEST",
            "name": "Test Product",
            "category": "Test",
            "unit": "metre",
            "stock": 1000,
            "min_stock": 100,
            "unit_price": 50,
            "active": True,
        },
        headers=get_headers("operator", "Admin123!"),
    )

    assert response.status_code == 403


def test_operator_cannot_update_product():
    response = client.put(
        "/api/products/1",
        json={
            "name": "Updated Product",
        },
        headers=get_headers("operator", "Admin123!"),
    )

    assert response.status_code == 403


def test_operator_cannot_delete_product():
    response = client.delete(
        "/api/products/1",
        headers=get_headers("operator", "Admin123!"),
    )

    assert response.status_code == 403


def test_operator_can_create_production():
    response = client.post(
        "/api/production/",
        json={
            "machine_id": 1,
            "product_id": 1,
            "shift": "A",
            "production_date": "2026-10-05",
            "quantity": 1000,
            "scrap_quantity": 20,
            "operator": "Test Operator",
        },
        headers=get_headers("operator", "Admin123!"),
    )

    assert response.status_code == 201


def test_operator_can_update_production():
    response = client.put(
        "/api/production/1",
        json={
            "quantity": 1500,
        },
        headers=get_headers("operator", "Admin123!"),
    )

    assert response.status_code == 200


def test_operator_cannot_delete_production():
    response = client.delete(
        "/api/production/1",
        headers=get_headers("operator", "Admin123!"),
    )

    assert response.status_code == 403


def test_admin_can_delete_production():
    response = client.delete(
        "/api/production/1",
        headers=get_headers("admin", "Admin123!"),
    )

    assert response.status_code == 200
