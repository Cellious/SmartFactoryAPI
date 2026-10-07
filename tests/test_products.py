from fastapi.testclient import TestClient

from app.main import app
from app.database.fake_db import products


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
    """
    Her testten önce fake database'i başlangıç durumuna getirir.
    """
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
            },
            {
                "id": 2,
                "code": "PRD-002",
                "name": "PVC Profil 80x50",
                "category": "PVC Profil",
                "unit": "metre",
                "stock": 8600,
                "min_stock": 2500,
                "unit_price": 112.75,
                "active": True,
            },
            {
                "id": 3,
                "code": "PRD-003",
                "name": "Alüminyum Profil 40x20",
                "category": "Alüminyum",
                "unit": "metre",
                "stock": 4200,
                "min_stock": 1500,
                "unit_price": 145.00,
                "active": True,
            },
            {
                "id": 4,
                "code": "PRD-004",
                "name": "PVC Kapak Profil",
                "category": "PVC Profil",
                "unit": "metre",
                "stock": 1800,
                "min_stock": 2000,
                "unit_price": 67.25,
                "active": True,
            },
            {
                "id": 5,
                "code": "PRD-005",
                "name": "Köşe Profil",
                "category": "PVC Profil",
                "unit": "metre",
                "stock": 6500,
                "min_stock": 2000,
                "unit_price": 54.90,
                "active": True,
            },
        ]
    )


def test_get_products():
    response = client.get(
        "/api/products/",
        headers=get_admin_headers(),
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 5
    assert data[0]["code"] == "PRD-001"


def test_get_product_by_id():
    response = client.get(
        "/api/products/1",
        headers=get_admin_headers(),
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == 1
    assert data["name"] == "PVC Profil 60x40"


def test_get_product_not_found():
    response = client.get(
        "/api/products/999",
        headers=get_admin_headers(),
    )

    assert response.status_code == 404

    assert response.json()["detail"] == "Product not found"


def test_get_low_stock_products():
    response = client.get(
        "/api/products/low-stock",
        headers=get_admin_headers(),
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1
    assert data[0]["code"] == "PRD-004"


def test_create_product():
    new_product = {
        "code": "PRD-006",
        "name": "Dekoratif Profil",
        "category": "PVC Profil",
        "unit": "metre",
        "stock": 3200,
        "min_stock": 1000,
        "unit_price": 72.50,
        "active": True,
    }

    response = client.post(
        "/api/products/",
        json=new_product,
        headers=get_admin_headers(),
    )

    assert response.status_code == 201

    data = response.json()

    assert data["id"] == 6
    assert data["code"] == "PRD-006"
    assert data["name"] == "Dekoratif Profil"


def test_update_product():
    response = client.put(
        "/api/products/1",
        json={
            "stock": 5000,
        },
        headers=get_admin_headers(),
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == 1
    assert data["stock"] == 5000


def test_update_product_not_found():
    response = client.put(
        "/api/products/999",
        json={
            "stock": 5000,
        },
        headers=get_admin_headers(),
    )

    assert response.status_code == 404


def test_delete_product():
    response = client.delete(
        "/api/products/1",
        headers=get_admin_headers(),
    )

    assert response.status_code == 200

    data = response.json()

    assert data["product_id"] == 1

    get_response = client.get(
        "/api/products/1",
        headers=get_admin_headers(),
    )

    assert get_response.status_code == 404


def test_delete_product_not_found():
    response = client.delete(
        "/api/products/999",
        headers=get_admin_headers(),
    )

    assert response.status_code == 404
