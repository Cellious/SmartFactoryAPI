import logging
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException

from app.auth.dependencies import require_role
from app.schemas.ai import ProductionAnalysisResponse
from app.services.ai_service import analyze_production
from app.services.log_service import add_log


logger = logging.getLogger(__name__)

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
    operation_id = str(uuid4())
    add_log(
        "AI üretim analizi başlatıldı.",
        level="INFO",
        source="ai",
        operation_id=operation_id,
    )

    try:
        result = analyze_production()

        add_log(
            "AI üretim analizi başarıyla tamamlandı.",
            level="SUCCESS",
            source="ai",
            operation_id=operation_id,
        )
        return result

    except RuntimeError as exc:
        logger.exception("AI üretim analizi başarısız oldu.")
        add_log(
            f"AI üretim analizi başarısız oldu: {exc}",
            level="ERROR",
            source="ai",
            operation_id=operation_id,
        )
        raise HTTPException(
            status_code=503,
            detail=str(exc),
        ) from exc

    except Exception:
        logger.exception("AI üretim analizinde beklenmeyen hata.")
        add_log(
            "AI üretim analizinde beklenmeyen bir hata oluştu.",
            level="ERROR",
            source="ai",
            operation_id=operation_id,
        )
        raise
