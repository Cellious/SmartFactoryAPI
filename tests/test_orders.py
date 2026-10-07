from fastapi.testclient import TestClient

from app.database.fake_db import orders
from app.main import app


client = TestClient(app)


ORIGINAL_ORDERS = [
    {
        "id": 1,
        "order_number": "ORD-2026-001",
        "customer_name": "ABC Yapı Ltd.",
        "product_id": 1,
        "quantity": 5000,
        "order_date": "2026-10-01",
        "delivery_date": "2026-10-10",
        "status": "CONFIRMED",
        "unit_price": 85.50,
    },
    {
        "id": 2,
        "order_number": "ORD-2026-002",
        "customer_name": "XYZ İnşaat A.Ş.",
        "product_id": 2,
        "quantity": 7500,
        "order_date": "2026-10-02",
        "delivery_date": "2026-10-12",
        "status": "PRODUCING",
        "unit_price": 112.75,
    },
    {
        "id": 3,
        "order_number": "ORD-2026-003",
        "customer_name": "Marmara Profil",
        "product_id": 3,
        "quantity": 3200,
        "order_date": "2026-10-03",
        "delivery_date": "2026-10-15",
        "status": "PENDING",
        "unit_price": 145.00,
    },
    {
        "id": 4,
        "order_number": "ORD-2026-004",
        "customer_name": "Delta Yapı",
        "product_id": 4,
        "quantity": 2800,
        "order_date": "2026-10-04",
        "delivery_date": "2026-10-14",
        "status": "READY",
        "unit_price": 67.25,
    },
]


def setup_function():
    orders.clear()

    for order in ORIGINAL_ORDERS:
        orders.append(order.copy())


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


def test_list_orders():
    response = client.get(
        "/api/orders/",
        headers=get_admin_headers(),
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 4


def test_get_order():
    response = client.get(
        "/api/orders/1",
        headers=get_admin_headers(),
    )

    assert response.status_code == 200

    data = response.json()

    assert data["order_number"] == "ORD-2026-001"
    assert data["customer_name"] == "ABC Yapı Ltd."


def test_get_order_not_found():
    response = client.get(
        "/api/orders/999",
        headers=get_admin_headers(),
    )

    assert response.status_code == 404


def test_create_order():
    payload = {
        "order_number": "ORD-2026-005",
        "customer_name": "Yeni Müşteri",
        "product_id": 1,
        "quantity": 2000,
        "order_date": "2026-10-05",
        "delivery_date": "2026-10-15",
        "status": "PENDING",
        "unit_price": 85.50,
    }

    response = client.post(
        "/api/orders/",
        json=payload,
        headers=get_admin_headers(),
    )

    assert response.status_code == 201

    data = response.json()

    assert data["id"] == 5
    assert data["order_number"] == "ORD-2026-005"


def test_create_order_invalid_product():
    payload = {
        "order_number": "ORD-2026-006",
        "customer_name": "Test Müşteri",
        "product_id": 999,
        "quantity": 1000,
        "order_date": "2026-10-05",
        "delivery_date": "2026-10-15",
        "status": "PENDING",
        "unit_price": 85.50,
    }

    response = client.post(
        "/api/orders/",
        json=payload,
        headers=get_admin_headers(),
    )

    assert response.status_code == 400

    assert response.json()["detail"] == "Product not found"


def test_create_duplicate_order_number():
    payload = {
        "order_number": "ORD-2026-001",
        "customer_name": "Test Müşteri",
        "product_id": 1,
        "quantity": 1000,
        "order_date": "2026-10-05",
        "delivery_date": "2026-10-15",
        "status": "PENDING",
        "unit_price": 85.50,
    }

    response = client.post(
        "/api/orders/",
        json=payload,
        headers=get_admin_headers(),
    )

    assert response.status_code == 400

    assert (
        response.json()["detail"]
        == "Order number already exists"
    )


def test_update_order():
    payload = {
        "customer_name": "Güncellenmiş Müşteri",
        "status": "CONFIRMED",
    }

    response = client.put(
        "/api/orders/1",
        json=payload,
        headers=get_admin_headers(),
    )

    assert response.status_code == 200

    data = response.json()

    assert data["customer_name"] == "Güncellenmiş Müşteri"
    assert data["status"] == "CONFIRMED"


def test_filter_orders_by_status():
    response = client.get(
        "/api/orders/status/PRODUCING",
        headers=get_admin_headers(),
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1
    assert data[0]["status"] == "PRODUCING"


def test_order_summary():
    response = client.get(
        "/api/orders/summary",
        headers=get_admin_headers(),
    )

    assert response.status_code == 200

    data = response.json()

    assert data["total_orders"] == 4
    assert data["total_quantity"] == 18500
    assert data["total_value"] == 1925425.0


def test_delete_order():
    response = client.delete(
        "/api/orders/4",
        headers=get_admin_headers(),
    )

    assert response.status_code == 200

    response = client.get(
        "/api/orders/4",
        headers=get_admin_headers(),
    )

    assert response.status_code == 404
