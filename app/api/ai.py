from fastapi import APIRouter, Depends, HTTPException

from app.auth.dependencies import require_role
from app.schemas.ai import ProductionAnalysisResponse
from app.services.ai_service import analyze_production


router = APIRouter(
    prefix="/api/ai",
    tags=["AI Analysis"],
)


@router.post(
    "/production-analysis",
    response_model=ProductionAnalysisResponse,
    dependencies=[Depends(require_role("ADMIN", "OPERATOR"))],
)
def production_analysis():
    try:
        return analyze_production()
    except RuntimeError as exc:
        raise HTTPException(
            status_code=503,
            detail=str(exc),
        ) from exc
