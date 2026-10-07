from pathlib import Path
import importlib
import sys

import logfire
from fastapi.testclient import TestClient


def _load_vision_api(monkeypatch):
    monkeypatch.setenv("GOOGLE_SHEETS", "sheet-id")
    monkeypatch.setenv("OPENAI_MODEL", "model")
    monkeypatch.setenv("LOGFIRE_TOKEN", "")
    configure = logfire.configure
    monkeypatch.setattr(
        logfire,
        "configure",
        lambda **_: configure(send_to_logfire=False),
    )

    for module_name in (
        "cellenium.api.vision",
        "cellenium.functions.logger",
        "src.cellenium.api.vision",
        "src.cellenium.settings",
    ):
        sys.modules.pop(module_name, None)

    return importlib.import_module("cellenium.api.vision")


def test_health_endpoint_works_after_service_startup(monkeypatch):
    vision_api = _load_vision_api(monkeypatch)

    with TestClient(vision_api.app) as client:
        response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_ai_endpoint_passes_temporary_image_path(monkeypatch):
    vision_api = _load_vision_api(monkeypatch)
    image_bytes = b"fake-image-data"
    received = {}

    def fake_run_vision_agent(*, prompt, image):
        image_path = Path(image[0])
        received.update(
            prompt=prompt,
            image_path=image_path,
            image_bytes=image_path.read_bytes(),
        )
        return {"result": "ok"}

    monkeypatch.setattr(vision_api, "run_vision_agent", fake_run_vision_agent)

    with TestClient(vision_api.app) as client:
        response = client.post(
            "/api/v1/vision/ai",
            params={"prompt": "what is displayed?"},
            files={"image": ("sample.png", image_bytes, "image/png")},
        )

    assert response.status_code == 200
    assert received["prompt"] == "what is displayed?"
    assert received["image_path"].suffix == ".png"
    assert received["image_bytes"] == image_bytes
    assert not received["image_path"].exists()
