from fastapi import APIRouter, Depends

from app.auth.dependencies import require_role
from app.schemas.dashboard import DashboardSummary
from app.services.dashboard_service import get_dashboard_summary


router = APIRouter(
    prefix="/api/dashboard",
    tags=["Dashboard"],
)


@router.get(
    "/summary",
    response_model=DashboardSummary,
    dependencies=[Depends(require_role("ADMIN", "OPERATOR"))],
)
def dashboard_summary():
    return get_dashboard_summary()
