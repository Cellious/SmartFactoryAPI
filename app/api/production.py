from fastapi import APIRouter, Depends, HTTPException

from app.auth.dependencies import require_role
from app.repositories.production_repository import (
    delete_production,
    get_all_production,
    get_production_by_id,
    update_production,
)
from app.schemas.production import (
    Production,
    ProductionCreate,
    ProductionStatistics,
    ProductionUpdate,
)
from app.services.production_service import (
    calculate_production_statistics,
    create_valid_production,
)


router = APIRouter(
    prefix="/api/production",
    tags=["Production"],
)


@router.get(
    "/",
    response_model=list[Production],
    dependencies=[Depends(require_role("ADMIN", "OPERATOR"))],
)
def list_production():
    return get_all_production()


@router.get(
    "/statistics",
    response_model=ProductionStatistics,
    dependencies=[Depends(require_role("ADMIN", "OPERATOR"))],
)
def production_statistics():
    return calculate_production_statistics()


@router.get(
    "/{production_id}",
    response_model=Production,
    dependencies=[Depends(require_role("ADMIN", "OPERATOR"))],
)
def get_production(production_id: int):
    record = get_production_by_id(production_id)

    if record is None:
        raise HTTPException(
            status_code=404,
            detail="Production record not found",
        )

    return record


@router.post(
    "/",
    response_model=Production,
    status_code=201,
    dependencies=[Depends(require_role("ADMIN", "OPERATOR"))],
)
def create_new_production(
    production: ProductionCreate,
):
    record, error = create_valid_production(
        production.model_dump()
    )

    if error is not None:
        raise HTTPException(
            status_code=404,
            detail=error,
        )

    return record


@router.put(
    "/{production_id}",
    response_model=Production,
    dependencies=[Depends(require_role("ADMIN", "OPERATOR"))],
)
def update_existing_production(
    production_id: int,
    production: ProductionUpdate,
):
    updated_record = update_production(
        production_id,
        production.model_dump(
            exclude_unset=True
        ),
    )

    if updated_record is None:
        raise HTTPException(
            status_code=404,
            detail="Production record not found",
        )

    return updated_record


@router.delete(
    "/{production_id}",
    dependencies=[Depends(require_role("ADMIN"))],
)
def delete_existing_production(
    production_id: int,
):
    deleted = delete_production(production_id)

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Production record not found",
        )

    return {
        "message": "Production record deleted successfully",
        "production_id": production_id,
    }
