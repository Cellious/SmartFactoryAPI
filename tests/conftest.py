import pytest

from app.database.fake_db import production_records


@pytest.fixture(autouse=True)
def reset_production_records():
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
