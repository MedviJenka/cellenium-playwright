import importlib
import sys
import types


def test_logfire_token_is_optional(monkeypatch):
    sys.modules.pop("settings", None)
    monkeypatch.delenv("LOGFIRE_TOKEN", raising=False)
    settings = importlib.import_module("settings")

    config = settings.__Config(
        _env_file=None,
        GOOGLE_SHEETS="sheet-id",
        GOOGLE_SHEET_API_KEY="api-key",
        GOOGLE_SHEET_EMAIL="service@example.com",
        GOOGLE_SHEET_ID="sheet-id",
        OPENAI_MODEL="model",
        TEST_HEADLESS=True,
    )

    assert config.LOGFIRE_TOKEN is None


def test_logger_only_sends_when_token_is_present(monkeypatch):
    configure_calls = []
    logfire = types.ModuleType("logfire")
    logfire.configure = lambda **kwargs: configure_calls.append(kwargs) or object()
    settings = types.ModuleType("settings")
    settings.Config = types.SimpleNamespace(LOGFIRE_TOKEN=None)

    monkeypatch.setitem(sys.modules, "logfire", logfire)
    monkeypatch.setitem(sys.modules, "settings", settings)
    sys.modules.pop("src.core.functions.logger", None)
    logger = importlib.import_module("src.core.functions.logger")

    logger.Logger(name="test")

    assert configure_calls == [
        {"token": None, "send_to_logfire": "if-token-present"}
    ]
