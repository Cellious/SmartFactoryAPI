from app.database.fake_db import (
    products,
    stock_movements,
)


def get_all_stock_movements():
    return stock_movements


def get_stock_movement_by_id(movement_id: int):
    for movement in stock_movements:
        if movement["id"] == movement_id:
            return movement

    return None


def create_stock_movement(movement_data: dict):
    new_id = max(
        movement["id"]
        for movement in stock_movements
    ) + 1

    movement = {
        "id": new_id,
        **movement_data,
    }

    stock_movements.append(movement)

    return movement


def get_product(product_id: int):
    for product in products:
        if product["id"] == product_id:
            return product

    return None


def get_stock_balances():
    balances = []

    for product in products:
        if product["stock"] <= product["min_stock"]:
            status = "LOW"
        else:
            status = "NORMAL"

        balances.append(
            {
                "product_id": product["id"],
                "product_code": product["code"],
                "product_name": product["name"],
                "stock": product["stock"],
                "min_stock": product["min_stock"],
                "stock_status": status,
            }
        )

    return balances


def calculate_total_stock_value():
    return sum(
        product["stock"] * product["unit_price"]
        for product in products
    )
