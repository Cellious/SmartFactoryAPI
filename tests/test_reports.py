from app.database.fake_db import machines, production_records
from app.main import app
from fastapi.testclient import TestClient


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
        "Authorization": f"Bearer {token}"
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
            },
            {
                "id": 2,
                "code": "EXT-02",
                "name": "Ekstruder 02",
                "type": "Extruder",
                "line": "PVC Line 2",
                "status": "running",
                "capacity_per_hour": 1800,
                "active": True,
            },
            {
                "id": 3,
                "code": "EXT-03",
                "name": "Ekstruder 03",
                "type": "Extruder",
                "line": "PVC Line 3",
                "status": "maintenance",
                "capacity_per_hour": 1400,
                "active": True,
            },
            {
                "id": 4,
                "code": "CUT-01",
                "name": "Kesim Makinesi 01",
                "type": "Cutting",
                "line": "Cutting Line 1",
                "status": "stopped",
                "capacity_per_hour": 2200,
                "active": True,
            },
        ]
    )

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


def test_machine_performance_report_status():
    response = client.get(
        "/api/reports/machine-performance",
        headers=get_admin_headers(),
    )

    assert response.status_code == 200


def test_machine_performance_report_count():
    response = client.get(
        "/api/reports/machine-performance",
        headers=get_admin_headers(),
    )

    data = response.json()

    assert len(data) == 4


def test_ext01_performance():
    response = client.get(
        "/api/reports/machine-performance",
        headers=get_admin_headers(),
    )

    data = response.json()

    ext01 = next(
        item
        for item in data
        if item["machine"] == "EXT-01"
    )

    assert ext01["machine_name"] == "Ekstruder 01"
    assert ext01["total_production"] == 22300
    assert ext01["total_scrap"] == 420
    assert ext01["scrap_rate"] == 1.88


def test_ext02_performance():
    response = client.get(
        "/api/reports/machine-performance",
        headers=get_admin_headers(),
    )

    data = response.json()

    ext02 = next(
        item
        for item in data
        if item["machine"] == "EXT-02"
    )

    assert ext02["total_production"] == 21900
    assert ext02["total_scrap"] == 405
    assert ext02["scrap_rate"] == 1.85


def test_ext03_performance():
    response = client.get(
        "/api/reports/machine-performance",
        headers=get_admin_headers(),
    )

    data = response.json()

    ext03 = next(
        item
        for item in data
        if item["machine"] == "EXT-03"
    )

    assert ext03["total_production"] == 11200
    assert ext03["total_scrap"] == 420
    assert ext03["scrap_rate"] == 3.75


def test_machine_without_production():
    response = client.get(
        "/api/reports/machine-performance",
        headers=get_admin_headers(),
    )

    data = response.json()

    cut01 = next(
        item
        for item in data
        if item["machine"] == "CUT-01"
    )

    assert cut01["total_production"] == 0
    assert cut01["total_scrap"] == 0
    assert cut01["scrap_rate"] == 0
