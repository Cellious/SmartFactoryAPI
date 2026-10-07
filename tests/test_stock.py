from app.database.fake_db import products, stock_movements
from app.main import app
from fastapi.testclient import TestClient


client = TestClient(app)


def setup_function():
    products.clear()

    products.extend(
        [
            {
                "id": 1,
                "code": "PRD-001",
                "name": "PVC Profil 60x40",
                "category": "PVC Profil",
                "unit": "metre",
                "stock": 10000,
                "min_stock": 3000,
                "unit_price": 85.50,
                "active": True,
            },
            {
                "id": 2,
                "code": "PRD-002",
                "name": "PVC Profil 80x50",
                "category": "PVC Profil",
                "unit": "metre",
                "stock": 2000,
                "min_stock": 2500,
                "unit_price": 112.75,
                "active": True,
            },
        ]
    )

    stock_movements.clear()

    stock_movements.extend(
        [
            {
                "id": 1,
                "product_id": 1,
                "movement_type": "IN",
                "quantity": 1000,
                "reason": "Production",
                "movement_date": "2026-10-05",
            }
        ]
    )


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
        "Authorization": f"Bearer {token}",
    }


def test_list_stock_movements():
    response = client.get(
        "/api/stock/movements",
        headers=get_admin_headers(),
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1
    assert data[0]["product_id"] == 1
    assert data[0]["movement_type"] == "IN"


def test_stock_increases_with_in_movement():
    response = client.post(
        "/api/stock/movements",
        json={
            "product_id": 1,
            "movement_type": "IN",
            "quantity": 500,
            "reason": "Production",
            "movement_date": "2026-10-05",
        },
        headers=get_admin_headers(),
    )

    assert response.status_code == 201

    data = response.json()

    assert data["product_id"] == 1
    assert data["quantity"] == 500

    product = next(
        product
        for product in products
        if product["id"] == 1
    )

    assert product["stock"] == 10500


def test_stock_decreases_with_out_movement():
    response = client.post(
        "/api/stock/movements",
        json={
            "product_id": 1,
            "movement_type": "OUT",
            "quantity": 500,
            "reason": "Shipment",
            "movement_date": "2026-10-05",
        },
        headers=get_admin_headers(),
    )

    assert response.status_code == 201

    product = next(
        product
        for product in products
        if product["id"] == 1
    )

    assert product["stock"] == 9500


def test_insufficient_stock():
    response = client.post(
        "/api/stock/movements",
        json={
            "product_id": 1,
            "movement_type": "OUT",
            "quantity": 20000,
            "reason": "Shipment",
            "movement_date": "2026-10-05",
        },
        headers=get_admin_headers(),
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Insufficient stock"

    product = next(
        product
        for product in products
        if product["id"] == 1
    )

    assert product["stock"] == 10000


def test_stock_movement_product_not_found():
    response = client.post(
        "/api/stock/movements",
        json={
            "product_id": 999,
            "movement_type": "IN",
            "quantity": 100,
            "reason": "Production",
            "movement_date": "2026-10-05",
        },
        headers=get_admin_headers(),
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Product not found"


def test_stock_balance_report():
    response = client.get(
        "/api/stock/balances",
        headers=get_admin_headers(),
    )

    assert response.status_code == 200

    data = response.json()

    product_1 = next(
        item
        for item in data
        if item["product_id"] == 1
    )

    product_2 = next(
        item
        for item in data
        if item["product_id"] == 2
    )

    assert product_1["stock_status"] == "NORMAL"
    assert product_2["stock_status"] == "LOW"


def test_stock_value_report():
    response = client.get(
        "/api/stock/value",
        headers=get_admin_headers(),
    )

    assert response.status_code == 200

    data = response.json()

    expected_value = (
        10000 * 85.50
        + 2000 * 112.75
    )

    assert data["total_stock_value"] == expected_value
