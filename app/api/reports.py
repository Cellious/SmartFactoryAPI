from fastapi import APIRouter, Depends

from app.auth.dependencies import require_role
from app.schemas.report import MachinePerformanceReport
from app.services.report_service import calculate_machine_performance


router = APIRouter(
    prefix="/api/reports",
    tags=["Reports"],
)


@router.get(
    "/machine-performance",
    response_model=list[MachinePerformanceReport],
    dependencies=[Depends(require_role("ADMIN", "OPERATOR"))],
)
def machine_performance_report():
    return calculate_machine_performance()
