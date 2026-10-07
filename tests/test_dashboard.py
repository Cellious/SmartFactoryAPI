from fastapi.testclient import TestClient

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
        "Authorization": f"Bearer {token}"
    }


def test_dashboard_summary_status():
    response = client.get(
        "/api/dashboard/summary",
        headers=get_admin_headers(),
    )

    assert response.status_code == 200


def test_dashboard_product_metrics():
    response = client.get(
        "/api/dashboard/summary",
        headers=get_admin_headers(),
    )

    data = response.json()

    assert data["total_products"] == 5
    assert data["low_stock_products"] == 1


def test_dashboard_stock_value():
    response = client.get(
        "/api/dashboard/summary",
        headers=get_admin_headers(),
    )

    data = response.json()

    assert data["total_stock_value"] == 3125300.0


def test_dashboard_production_metrics():
    response = client.get(
        "/api/dashboard/summary",
        headers=get_admin_headers(),
    )

    data = response.json()

    assert data["total_production"] == 55400
    assert data["total_scrap"] == 1245
    assert data["overall_scrap_rate"] == 2.25


def test_dashboard_machine_metrics():
    response = client.get(
        "/api/dashboard/summary",
        headers=get_admin_headers(),
    )

    data = response.json()

    assert data["total_machines"] == 4
    assert data["active_machines"] == 4
    assert data["running_machines"] == 2
    assert data["maintenance_machines"] == 1


def test_dashboard_order_metrics():
    response = client.get(
        "/api/dashboard/summary",
        headers=get_admin_headers(),
    )

    data = response.json()

    assert data["total_orders"] == 4
    assert data["pending_orders"] == 1
    assert data["producing_orders"] == 1
    assert data["ready_orders"] == 1
    assert data["shipped_orders"] == 0
    assert data["completed_orders"] == 0
