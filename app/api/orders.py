from fastapi import APIRouter, Depends, HTTPException

from app.auth.dependencies import require_role

from app.repositories.order_repository import (
    get_all_orders,
    get_order_by_id,
)

from app.schemas.order import (
    Order,
    OrderCreate,
    OrderSummary,
    OrderUpdate,
)

from app.services.order_service import (
    create_valid_order,
    delete_existing_order,
    get_order_summary,
    get_orders_filtered_by_status,
    update_existing_order,
)


router = APIRouter(
    prefix="/api/orders",
    tags=["Orders"],
)


@router.get(
    "/",
    response_model=list[Order],
    dependencies=[Depends(require_role("ADMIN", "OPERATOR"))],
)
def list_orders():
    return get_all_orders()


@router.get(
    "/summary",
    response_model=OrderSummary,
    dependencies=[Depends(require_role("ADMIN", "OPERATOR"))],
)
def order_summary():
    return get_order_summary()


@router.get(
    "/status/{status}",
    response_model=list[Order],
    dependencies=[Depends(require_role("ADMIN", "OPERATOR"))],
)
def list_orders_by_status(status: str):
    orders = get_orders_filtered_by_status(status)

    return orders


@router.get(
    "/{order_id}",
    response_model=Order,
    dependencies=[Depends(require_role("ADMIN", "OPERATOR"))],
)
def get_order(order_id: int):
    order = get_order_by_id(order_id)

    if order is None:
        raise HTTPException(
            status_code=404,
            detail="Order not found",
        )

    return order


@router.post(
    "/",
    response_model=Order,
    status_code=201,
    dependencies=[Depends(require_role("ADMIN"))],
)
def create_new_order(order: OrderCreate):
    created_order, error = create_valid_order(
        order.model_dump()
    )

    if error is not None:
        raise HTTPException(
            status_code=400,
            detail=error,
        )

    return created_order


@router.put(
    "/{order_id}",
    response_model=Order,
    dependencies=[Depends(require_role("ADMIN"))],
)
def update_order(
    order_id: int,
    order: OrderUpdate,
):
    updated_order, error = update_existing_order(
        order_id,
        order.model_dump(exclude_unset=True),
    )

    if error is not None:
        status_code = 404 if error == "Order not found" else 400

        raise HTTPException(
            status_code=status_code,
            detail=error,
        )

    return updated_order


@router.delete(
    "/{order_id}",
    dependencies=[Depends(require_role("ADMIN"))],
)
def delete_order(order_id: int):
    deleted = delete_existing_order(order_id)

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Order not found",
        )

    return {
        "message": "Order deleted successfully",
        "order_id": order_id,
    }
