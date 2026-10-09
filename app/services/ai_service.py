import os

import httpx

from app.services.production_service import (
    calculate_production_statistics,
)
from app.services.report_service import (
    calculate_machine_performance,
)


OLLAMA_URL = os.getenv(
    "OLLAMA_URL",
    "http://localhost:11434",
).rstrip("/")

OLLAMA_MODEL = os.getenv(
    "OLLAMA_MODEL",
    "qwen2.5:3b",
)


def build_production_analysis():
    """Calculate trusted metrics before asking the model to interpret them."""
    statistics = calculate_production_statistics()
    machine_reports = calculate_machine_performance()

    highest_scrap_machine = max(
        machine_reports,
        key=lambda machine: machine["scrap_rate"],
        default=None,
    )

    return {
        "statistics": statistics,
        "machines": machine_reports,
        "highest_scrap_machine": highest_scrap_machine,
    }


def analyze_production():
    analysis_data = build_production_analysis()

    prompt = f"""
Sen bir üretim analisti asistanısın.
Yalnızca Türkçe cevap ver.
Sadece aşağıdaki verileri kullan; veri uydurma.
Sayısal hesaplamaları yeniden yapmaya çalışma.
En fazla üç somut ve uygulanabilir öneri sun.
Fire oranı yüksek bir makine varsa bunu belirt.
Veri yetersizse açıkça ifade et.

Üretim istatistikleri:
{analysis_data["statistics"]}

Makine performansları:
{analysis_data["machines"]}

Fire oranı en yüksek makine:
{analysis_data["highest_scrap_machine"]}

Türkçe bir yönetici özeti ve iyileştirme önerileri oluştur.
"""

    try:
        response = httpx.post(
        f"{OLLAMA_URL}/api/generate",
        json={
            "model": OLLAMA_MODEL,
            "prompt": prompt,
            "stream": False,
            "keep_alive": "10m",
            "options": {
                "temperature": 0,
                "num_predict": 120,
                "num_ctx": 2048,
            },
        },
        timeout=180.0,
        )
        response.raise_for_status()
        result = response.json()

    except httpx.TimeoutException as exc:
        raise RuntimeError(
            "Ollama yanıt vermek için zaman aşımına uğradı."
        ) from exc

    except httpx.HTTPError as exc:
        raise RuntimeError(
            "Ollama servisine erişilemedi veya istek başarısız oldu."
        ) from exc

    except ValueError as exc:
        raise RuntimeError(
            "Ollama geçersiz bir yanıt döndürdü."
        ) from exc

    answer = result.get("response", "").strip()

    if not answer:
        raise RuntimeError(
            "Ollama boş bir analiz yanıtı döndürdü."
        )

    return {
        "model": OLLAMA_MODEL,
        "statistics": analysis_data["statistics"],
        "machines": analysis_data["machines"],
        "highest_scrap_machine": analysis_data[
            "highest_scrap_machine"
        ],
        "analysis": answer,
    }

