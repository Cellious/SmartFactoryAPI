from app.repositories.stock_repository import (
    calculate_total_stock_value,
    create_stock_movement,
    get_all_stock_movements,
    get_product,
    get_stock_balances,
)


def process_stock_movement(movement_data: dict):
    product = get_product(
        movement_data["product_id"]
    )

    if product is None:
        return None, "Product not found"

    movement_type = movement_data["movement_type"]
    quantity = movement_data["quantity"]

    if movement_type == "IN":
        product["stock"] += quantity

    elif movement_type == "OUT":
        if product["stock"] < quantity:
            return None, "Insufficient stock"

        product["stock"] -= quantity

    movement = create_stock_movement(
        movement_data
    )

    return movement, None


def get_stock_movements():
    return get_all_stock_movements()


def get_stock_balance_report():
    return get_stock_balances()


def get_stock_value_report():
    total_value = calculate_total_stock_value()

    return {
        "total_stock_value": round(
            total_value,
            2,
        )
    }
