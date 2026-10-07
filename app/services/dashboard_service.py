from app.database.fake_db import (
    machines,
    orders,
    products,
    production_records,
)


def get_dashboard_summary():
    total_products = len(products)

    low_stock_products = sum(
        1
        for product in products
        if product["stock"] <= product["min_stock"]
    )

    total_stock_value = sum(
        product["stock"] * product["unit_price"]
        for product in products
    )

    total_production = sum(
        record["quantity"]
        for record in production_records
    )

    total_scrap = sum(
        record["scrap_quantity"]
        for record in production_records
    )

    if total_production == 0:
        overall_scrap_rate = 0
    else:
        overall_scrap_rate = (
            total_scrap / total_production
        ) * 100

    total_machines = len(machines)

    active_machines = sum(
        1
        for machine in machines
        if machine["active"]
    )

    running_machines = sum(
        1
        for machine in machines
        if machine["status"] == "running"
    )

    maintenance_machines = sum(
        1
        for machine in machines
        if machine["status"] == "maintenance"
    )

    total_orders = len(orders)

    pending_orders = sum(
        1
        for order in orders
        if order["status"] == "PENDING"
    )

    producing_orders = sum(
        1
        for order in orders
        if order["status"] == "PRODUCING"
    )

    ready_orders = sum(
        1
        for order in orders
        if order["status"] == "READY"
    )

    shipped_orders = sum(
        1
        for order in orders
        if order["status"] == "SHIPPED"
    )

    completed_orders = sum(
        1
        for order in orders
        if order["status"] == "COMPLETED"
    )

    return {
        "total_products": total_products,
        "low_stock_products": low_stock_products,
        "total_stock_value": round(
            total_stock_value,
            2,
        ),
        "total_production": total_production,
        "total_scrap": total_scrap,
        "overall_scrap_rate": round(
            overall_scrap_rate,
            2,
        ),
        "total_machines": total_machines,
        "active_machines": active_machines,
        "running_machines": running_machines,
        "maintenance_machines": maintenance_machines,
        "total_orders": total_orders,
        "pending_orders": pending_orders,
        "producing_orders": producing_orders,
        "ready_orders": ready_orders,
        "shipped_orders": shipped_orders,
        "completed_orders": completed_orders,
    }
