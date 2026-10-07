from pydantic import BaseModel, Field


class OrderBase(BaseModel):
    order_number: str
    customer_name: str
    product_id: int
    quantity: float = Field(gt=0)
    order_date: str
    delivery_date: str
    status: str = Field(
        pattern="^(PENDING|CONFIRMED|PRODUCING|READY|SHIPPED|COMPLETED|CANCELLED)$"
    )
    unit_price: float = Field(gt=0)


class OrderCreate(OrderBase):
    pass


class OrderUpdate(BaseModel):
    customer_name: str | None = None
    product_id: int | None = None
    quantity: float | None = Field(
        default=None,
        gt=0,
    )
    order_date: str | None = None
    delivery_date: str | None = None
    status: str | None = Field(
        default=None,
        pattern="^(PENDING|CONFIRMED|PRODUCING|READY|SHIPPED|COMPLETED|CANCELLED)$",
    )
    unit_price: float | None = Field(
        default=None,
        gt=0,
    )


class Order(OrderBase):
    id: int


class OrderSummary(BaseModel):
    total_orders: int
    total_quantity: float
    total_value: float
