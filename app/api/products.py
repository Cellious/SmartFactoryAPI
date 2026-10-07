from fastapi import APIRouter, Depends, HTTPException

from app.auth.dependencies import require_role
from app.repositories.product_repository import (
    create_product,
    delete_product,
    get_all_products,
    get_low_stock_products,
    get_product_by_id,
    update_product,
)
from app.schemas.product import (
    Product,
    ProductCreate,
    ProductUpdate,
)


router = APIRouter(
    prefix="/api/products",
    tags=["Products"],
)


@router.get(
    "/",
    response_model=list[Product],
    dependencies=[Depends(require_role("ADMIN", "OPERATOR"))],
)
def list_products():
    return get_all_products()


@router.get(
    "/low-stock",
    response_model=list[Product],
    dependencies=[Depends(require_role("ADMIN", "OPERATOR"))],
)
def list_low_stock_products():
    return get_low_stock_products()


@router.get(
    "/{product_id}",
    response_model=Product,
    dependencies=[Depends(require_role("ADMIN", "OPERATOR"))],
)
def get_product(product_id: int):
    product = get_product_by_id(product_id)

    if product is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found",
        )

    return product


@router.post(
    "/",
    response_model=Product,
    status_code=201,
    dependencies=[Depends(require_role("ADMIN"))],
)
def create_new_product(product: ProductCreate):
    return create_product(product.model_dump())


@router.put(
    "/{product_id}",
    response_model=Product,
    dependencies=[Depends(require_role("ADMIN"))],
)
def update_existing_product(
    product_id: int,
    product: ProductUpdate,
):
    updated_product = update_product(
        product_id,
        product.model_dump(exclude_unset=True),
    )

    if updated_product is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found",
        )

    return updated_product


@router.delete(
    "/{product_id}",
    dependencies=[Depends(require_role("ADMIN"))],
)
def delete_existing_product(product_id: int):
    deleted = delete_product(product_id)

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Product not found",
        )

    return {
        "message": "Product deleted successfully",
        "product_id": product_id,
    }
