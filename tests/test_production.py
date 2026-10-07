from fastapi.testclient import TestClient

from app.database.fake_db import production_records
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
    production_records.clear()

    production_records.extend(
        [
            {
                "id": 1,
                "machine_id": 1,
                "product_id": 1,
                "shift": "A",
                "production_date": "2026-10-05",
                "quantity": 12500,
                "scrap_quantity": 240,
                "operator": "Ahmet Yılmaz",
            },
            {
                "id": 2,
                "machine_id": 1,
                "product_id": 2,
                "shift": "B",
                "production_date": "2026-10-05",
                "quantity": 9800,
                "scrap_quantity": 180,
                "operator": "Mehmet Kaya",
            },
            {
                "id": 3,
                "machine_id": 2,
                "product_id": 1,
                "shift": "A",
                "production_date": "2026-10-05",
                "quantity": 14300,
                "scrap_quantity": 310,
                "operator": "Ali Demir",
            },
            {
                "id": 4,
                "machine_id": 2,
                "product_id": 3,
                "shift": "C",
                "production_date": "2026-10-05",
                "quantity": 7600,
                "scrap_quantity": 95,
                "operator": "Mustafa Çelik",
            },
            {
                "id": 5,
                "machine_id": 3,
                "product_id": 4,
                "shift": "A",
                "production_date": "2026-10-04",
                "quantity": 11200,
                "scrap_quantity": 420,
                "operator": "Hasan Şahin",
            },
        ]
    )


def test_get_production_records():
    response = client.get(
        "/api/production/",
        headers=get_admin_headers(),
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 5
    assert data[0]["id"] == 1


def test_get_production_by_id():
    response = client.get(
        "/api/production/1",
        headers=get_admin_headers(),
    )

    assert response.status_code == 200

    data = response.json()

    assert data["machine_id"] == 1
    assert data["product_id"] == 1
    assert data["quantity"] == 12500


def test_get_production_not_found():
    response = client.get(
        "/api/production/999",
        headers=get_admin_headers(),
    )

    assert response.status_code == 404


def test_get_production_statistics():
    response = client.get(
        "/api/production/statistics",
        headers=get_admin_headers(),
    )

    assert response.status_code == 200

    data = response.json()

    assert data["total_production"] == 55400
    assert data["total_scrap"] == 1245
    assert data["scrap_rate"] == 2.25


def test_create_production():
    new_production = {
        "machine_id": 3,
        "product_id": 2,
        "shift": "B",
        "production_date": "2026-10-05",
        "quantity": 8500,
        "scrap_quantity": 120,
        "operator": "Mehmet Demir",
    }

    response = client.post(
        "/api/production/",
        json=new_production,
        headers=get_admin_headers(),
    )

    assert response.status_code == 201

    data = response.json()

    assert data["id"] == 6
    assert data["quantity"] == 8500
    assert data["scrap_quantity"] == 120


def test_update_production():
    response = client.put(
        "/api/production/1",
        json={
            "quantity": 15000,
            "scrap_quantity": 200,
        },
        headers=get_admin_headers(),
    )

    assert response.status_code == 200

    data = response.json()

    assert data["quantity"] == 15000
    assert data["scrap_quantity"] == 200


def test_update_production_not_found():
    response = client.put(
        "/api/production/999",
        json={
            "quantity": 1000,
        },
        headers=get_admin_headers(),
    )

    assert response.status_code == 404


def test_delete_production():
    response = client.delete(
        "/api/production/1",
        headers=get_admin_headers(),
    )

    assert response.status_code == 200

    get_response = client.get(
        "/api/production/1",
        headers=get_admin_headers(),
    )

    assert get_response.status_code == 404


def test_delete_production_not_found():
    response = client.delete(
        "/api/production/999",
        headers=get_admin_headers(),
    )

    assert response.status_code == 404
