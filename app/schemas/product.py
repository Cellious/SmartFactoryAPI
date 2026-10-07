from pydantic import BaseModel


class ProductBase(BaseModel):
    code: str
    name: str
    category: str
    unit: str
    stock: float
    min_stock: float
    unit_price: float
    active: bool = True


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    code: str | None = None
    name: str | None = None
    category: str | None = None
    unit: str | None = None
    stock: float | None = None
    min_stock: float | None = None
    unit_price: float | None = None
    active: bool | None = None


class Product(ProductBase):
    id: int