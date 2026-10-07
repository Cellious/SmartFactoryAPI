from fastapi.testclient import TestClient

from app.database.fake_db import machines, production_records, products
from app.main import app


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
        "Authorization": f"Bearer {token}",
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
            }
        ]
    )

    products.clear()

    products.extend(
        [
            {
                "id": 1,
                "code": "PRD-001",
                "name": "PVC Profil 60x40",
                "category": "PVC Profil",
                "unit": "metre",
                "stock": 12500,
                "min_stock": 3000,
                "unit_price": 85.50,
                "active": True,
            }
        ]
    )

    production_records.clear()


def test_create_production_with_invalid_machine():
    response = client.post(
        "/api/production/",
        json={
            "machine_id": 999,
            "product_id": 1,
            "shift": "A",
            "production_date": "2026-10-05",
            "quantity": 1000,
            "scrap_quantity": 20,
            "operator": "Test Operator",
        },
        headers=get_admin_headers(),
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Machine not found"


def test_create_production_with_invalid_product():
    response = client.post(
        "/api/production/",
        json={
            "machine_id": 1,
            "product_id": 999,
            "shift": "A",
            "production_date": "2026-10-05",
            "quantity": 1000,
            "scrap_quantity": 20,
            "operator": "Test Operator",
        },
        headers=get_admin_headers(),
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Product not found"
