from fastapi import APIRouter, Depends, HTTPException

from app.auth.dependencies import require_role

from app.schemas.stock import (
    StockBalance,
    StockMovement,
    StockMovementCreate,
    StockValueReport,
)

from app.services.stock_service import (
    get_stock_balance_report,
    get_stock_movements,
    get_stock_value_report,
    process_stock_movement,
)


router = APIRouter(
    prefix="/api/stock",
    tags=["Stock"],
)


@router.get(
    "/movements",
    response_model=list[StockMovement],
    dependencies=[Depends(require_role("ADMIN", "OPERATOR"))],
)
def list_stock_movements():
    return get_stock_movements()


@router.post(
    "/movements",
    response_model=StockMovement,
    status_code=201,
    dependencies=[Depends(require_role("ADMIN"))],
)
def create_new_stock_movement(
    movement: StockMovementCreate,
):
    created_movement, error = process_stock_movement(
        movement.model_dump()
    )

    if error is not None:
        raise HTTPException(
            status_code=400,
            detail=error,
        )

    return created_movement


@router.get(
    "/balances",
    response_model=list[StockBalance],
    dependencies=[Depends(require_role("ADMIN", "OPERATOR"))],
)
def stock_balances():
    return get_stock_balance_report()


@router.get(
    "/value",
    response_model=StockValueReport,
    dependencies=[Depends(require_role("ADMIN", "OPERATOR"))],
)
def stock_value():
    return get_stock_value_report()
