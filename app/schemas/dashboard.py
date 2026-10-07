from pydantic import BaseModel


class DashboardSummary(BaseModel):
    total_products: int
    low_stock_products: int

    total_stock_value: float

    total_production: float
    total_scrap: float
    overall_scrap_rate: float

    total_machines: int
    active_machines: int
    running_machines: int
    maintenance_machines: int

    total_orders: int
    pending_orders: int
    producing_orders: int
    ready_orders: int
    shipped_orders: int
    completed_orders: int
