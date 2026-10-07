from app.database.fake_db import orders


def get_all_orders():
    return orders


def get_order_by_id(order_id: int):
    for order in orders:
        if order["id"] == order_id:
            return order

    return None


def get_order_by_number(order_number: str):
    for order in orders:
        if order["order_number"] == order_number:
            return order

    return None


def create_order(order_data: dict):
    new_id = max(
        order["id"]
        for order in orders
    ) + 1

    order = {
        "id": new_id,
        **order_data,
    }

    orders.append(order)

    return order


def update_order(
    order_id: int,
    order_data: dict,
):
    order = get_order_by_id(order_id)

    if order is None:
        return None

    for key, value in order_data.items():
        if value is not None:
            order[key] = value

    return order


def delete_order(order_id: int):
    order = get_order_by_id(order_id)

    if order is None:
        return False

    orders.remove(order)

    return True
