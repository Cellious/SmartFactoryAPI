from app.database.fake_db import products
from app.repositories.order_repository import (
    create_order,
    delete_order,
    get_all_orders,
    get_order_by_id,
    get_order_by_number,
    update_order,
)


def product_exists(product_id: int):
    return any(
        product["id"] == product_id
        for product in products
    )


def create_valid_order(order_data: dict):
    product_id = order_data["product_id"]
    order_number = order_data["order_number"]

    if not product_exists(product_id):
        return None, "Product not found"

    existing_order = get_order_by_number(order_number)

    if existing_order is not None:
        return None, "Order number already exists"

    return create_order(order_data), None


def update_existing_order(
    order_id: int,
    order_data: dict,
):
    order = get_order_by_id(order_id)

    if order is None:
        return None, "Order not found"

    if "product_id" in order_data:
        if not product_exists(order_data["product_id"]):
            return None, "Product not found"

    if "order_number" in order_data:
        existing_order = get_order_by_number(
            order_data["order_number"]
        )

        if (
            existing_order is not None
            and existing_order["id"] != order_id
        ):
            return None, "Order number already exists"

    updated_order = update_order(
        order_id,
        order_data,
    )

    return updated_order, None


def get_order_summary():
    orders = get_all_orders()

    total_orders = len(orders)

    total_quantity = sum(
        order["quantity"]
        for order in orders
    )

    total_value = sum(
        order["quantity"] * order["unit_price"]
        for order in orders
    )

    return {
        "total_orders": total_orders,
        "total_quantity": total_quantity,
        "total_value": round(total_value, 2),
    }


def get_orders_filtered_by_status(status: str):
    orders = get_all_orders()

    return [
        order
        for order in orders
        if order["status"] == status
    ]


def delete_existing_order(order_id: int):
    return delete_order(order_id)
