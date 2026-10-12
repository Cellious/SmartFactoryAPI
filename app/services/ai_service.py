import logging
import os

import httpx

from app.services.production_service import (
    calculate_production_statistics,
)
from app.services.report_service import (
    calculate_machine_performance,
)


logger = logging.getLogger(__name__)

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
Türkçe konuşan bir fabrika üretim analistisin.
Aşağıdaki hazır hesaplanmış verileri yorumla.
Sayıları tekrar hesaplama, değiştirme veya tahmin etme.
Verilmeyen nedenleri gerçekmiş gibi sunma.
Yalnızca Türkçe yaz. En fazla 120 kelime kullan.

VERİLER:
Genel istatistikler: {analysis_data["statistics"]}
Makine performansları: {analysis_data["machines"]}
En yüksek fireli makine: {analysis_data["highest_scrap_machine"]}

Şu üç başlığı sırayla ve kısa şekilde tamamla:

### Genel Değerlendirme
Toplam üretimi, toplam fire miktarını ve verilen fire oranını belirt.

### Makine Performansı
En yüksek fire oranlı makineyi, üretimini ve fire oranını belirt.
Diğer makinelerle kısa karşılaştırma yap.

### İyileştirme Önerileri
En fazla iki kısa öneri ver.
Makine ayarları, hammadde koşulları veya üretim kayıtlarının
kontrol edilmesini önerebilirsin.

Raporu eksiksiz tamamla. Verilerdeki sayıları aynen koru.
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
                    "num_predict": 100,
                    "num_ctx": 2048,
                },
            },
            timeout=180.0,
        )
        logger.info(
            "Ollama yanıtı alındı: model=%s, status=%s",
            OLLAMA_MODEL,
            response.status_code,
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

    if result.get("done_reason") == "length":
        logger.warning(
            "Ollama analizi token sınırına ulaştı: model=%s",
            OLLAMA_MODEL,
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
