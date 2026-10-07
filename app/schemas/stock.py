from pydantic import BaseModel, Field


class StockMovementBase(BaseModel):
    product_id: int
    movement_type: str = Field(
        pattern="^(IN|OUT)$"
    )
    quantity: float = Field(
        gt=0
    )
    reason: str
    movement_date: str


class StockMovementCreate(StockMovementBase):
    pass


class StockMovement(StockMovementBase):
    id: int


class StockBalance(BaseModel):
    product_id: int
    product_code: str
    product_name: str
    stock: float
    min_stock: float
    stock_status: str


class StockValueReport(BaseModel):
    total_stock_value: float
