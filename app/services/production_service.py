from app.database.fake_db import machines, products
from app.repositories.production_repository import (
    create_production,
    get_all_production,
)


def validate_production_references(
    machine_id: int,
    product_id: int,
):
    machine_exists = any(
        machine["id"] == machine_id
        for machine in machines
    )

    if not machine_exists:
        return False, "Machine not found"

    product_exists = any(
        product["id"] == product_id
        for product in products
    )

    if not product_exists:
        return False, "Product not found"

    return True, None


def create_valid_production(production_data: dict):
    is_valid, error = validate_production_references(
        production_data["machine_id"],
        production_data["product_id"],
    )

    if not is_valid:
        return None, error

    return create_production(production_data), None


def calculate_production_statistics():
    records = get_all_production()

    total_production = sum(
        record["quantity"]
        for record in records
    )

    total_scrap = sum(
        record["scrap_quantity"]
        for record in records
    )

    if total_production == 0:
        scrap_rate = 0
    else:
        scrap_rate = (
            total_scrap / total_production
        ) * 100

    return {
        "total_production": total_production,
        "total_scrap": total_scrap,
        "scrap_rate": round(scrap_rate, 2),
    }
