from fastapi import APIRouter, Depends, HTTPException

from app.auth.dependencies import require_role
from app.repositories.machine_repository import (
    create_machine,
    delete_machine,
    get_all_machines,
    get_machine_by_id,
    update_machine,
)

from app.schemas.machine import (
    Machine,
    MachineCreate,
    MachineUpdate,
)


router = APIRouter(
    prefix="/api/machines",
    tags=["Machines"],
)


@router.get(
    "/",
    response_model=list[Machine],
    dependencies=[Depends(require_role("ADMIN", "OPERATOR"))],
)
def list_machines():
    return get_all_machines()


@router.get(
    "/{machine_id}",
    response_model=Machine,
    dependencies=[Depends(require_role("ADMIN", "OPERATOR"))],
)
def get_machine(machine_id: int):
    machine = get_machine_by_id(machine_id)

    if machine is None:
        raise HTTPException(
            status_code=404,
            detail="Machine not found",
        )

    return machine


@router.post(
    "/",
    response_model=Machine,
    status_code=201,
    dependencies=[Depends(require_role("ADMIN"))],
)
def create_new_machine(
    machine: MachineCreate,
):
    return create_machine(
        machine.model_dump()
    )


@router.put(
    "/{machine_id}",
    response_model=Machine,
    dependencies=[Depends(require_role("ADMIN"))],
)
def update_existing_machine(
    machine_id: int,
    machine: MachineUpdate,
):
    updated_machine = update_machine(
        machine_id,
        machine.model_dump(
            exclude_unset=True
        ),
    )

    if updated_machine is None:
        raise HTTPException(
            status_code=404,
            detail="Machine not found",
        )

    return updated_machine


@router.delete(
    "/{machine_id}",
    dependencies=[Depends(require_role("ADMIN"))],
)
def delete_existing_machine(
    machine_id: int,
):
    deleted = delete_machine(machine_id)

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Machine not found",
        )

    return {
        "message": "Machine deleted successfully",
        "machine_id": machine_id,
    }
