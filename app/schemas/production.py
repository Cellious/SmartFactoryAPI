from pydantic import BaseModel


class ProductionBase(BaseModel):
    machine_id: int
    product_id: int
    shift: str
    production_date: str
    quantity: float
    scrap_quantity: float
    operator: str


class ProductionCreate(ProductionBase):
    pass


class ProductionUpdate(BaseModel):
    machine_id: int | None = None
    product_id: int | None = None
    shift: str | None = None
    production_date: str | None = None
    quantity: float | None = None
    scrap_quantity: float | None = None
    operator: str | None = None


class Production(ProductionBase):
    id: int


class ProductionStatistics(BaseModel):
    total_production: float
    total_scrap: float
    scrap_rate: float