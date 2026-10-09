import httpx
import pytest

from app.services import ai_service


def test_build_production_analysis_calculates_correct_statistics():
    result = ai_service.build_production_analysis()

    assert result["statistics"]["total_production"] == 55400
    assert result["statistics"]["total_scrap"] == 1245
    assert result["statistics"]["scrap_rate"] == 2.25


def test_build_production_analysis_finds_highest_scrap_machine():
    result = ai_service.build_production_analysis()

    machine = result["highest_scrap_machine"]

    assert machine is not None
    assert machine["machine"] == "EXT-03"
    assert machine["scrap_rate"] == 3.75


def test_build_production_analysis_includes_all_machines():
    result = ai_service.build_production_analysis()

    assert len(result["machines"]) == 4


def test_analyze_production_returns_model_analysis(monkeypatch):
    class FakeResponse:
        def raise_for_status(self):
            pass

        def json(self):
            return {
                "response": "Üretim özeti: Fire oranı %2,25."
            }

    def fake_post(*args, **kwargs):
        assert kwargs["json"]["model"] == ai_service.OLLAMA_MODEL
        assert kwargs["json"]["stream"] is False
        return FakeResponse()

    monkeypatch.setattr(ai_service.httpx, "post", fake_post)

    result = ai_service.analyze_production()

    assert result["model"] == ai_service.OLLAMA_MODEL
    assert result["statistics"]["scrap_rate"] == 2.25
    assert result["highest_scrap_machine"]["machine"] == "EXT-03"
    assert result["analysis"] == "Üretim özeti: Fire oranı %2,25."


def test_analyze_production_handles_ollama_timeout(monkeypatch):
    def fake_post(*args, **kwargs):
        raise httpx.TimeoutException("Test timeout")

    monkeypatch.setattr(ai_service.httpx, "post", fake_post)

    with pytest.raises(
        RuntimeError,
        match="Ollama yanıt vermek için zaman aşımına uğradı",
    ):
        ai_service.analyze_production()


def test_analyze_production_handles_ollama_connection_error(monkeypatch):
    def fake_post(*args, **kwargs):
        raise httpx.ConnectError("Test connection error")

    monkeypatch.setattr(ai_service.httpx, "post", fake_post)

    with pytest.raises(
        RuntimeError,
        match="Ollama servisine erişilemedi",
    ):
        ai_service.analyze_production()


def test_analyze_production_rejects_empty_response(monkeypatch):
    class FakeResponse:
        def raise_for_status(self):
            pass

        def json(self):
            return {"response": "   "}

    monkeypatch.setattr(
        ai_service.httpx,
        "post",
        lambda *args, **kwargs: FakeResponse(),
    )

    with pytest.raises(
        RuntimeError,
        match="Ollama boş bir analiz yanıtı döndürdü",
    ):
        ai_service.analyze_production()
