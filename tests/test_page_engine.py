import importlib
import sys
import types
from pathlib import Path


def _load_page_engine(monkeypatch):
    logger_module = types.ModuleType("src.core.functions.logger")

    class StubLogger:
        def __init__(self, **_kwargs):
            pass

        def fire(self, **_kwargs):
            pass

    logger_module.Logger = StubLogger
    manager_module = types.ModuleType("src.core.engine.manager")
    manager_module.BrowserManager = type("BrowserManager", (), {})
    locators_module = types.ModuleType("src.core.functions.locators")
    locators_module.get_locator = lambda *_args, **_kwargs: None
    locators_module.get_entry = lambda *_args, **_kwargs: None

    monkeypatch.setitem(sys.modules, "src.core.functions.logger", logger_module)
    monkeypatch.setitem(sys.modules, "src.core.engine.manager", manager_module)
    monkeypatch.setitem(sys.modules, "src.core.functions.locators", locators_module)
    sys.modules.pop("src.core.engine.page_engine", None)
    return importlib.import_module("src.core.engine.page_engine")


def test_get_screenshot_creates_directory_and_returns_saved_path(tmp_path, monkeypatch):
    page_engine = _load_page_engine(monkeypatch)
    screenshot_directory = tmp_path / "screenshots"
    monkeypatch.setattr(page_engine, "SCREENSHOTS", screenshot_directory)

    class StubPage:
        saved_path: Path | None = None

        def screenshot(self, *, path: str) -> None:
            self.saved_path = Path(path)
            self.saved_path.write_bytes(b"png")

    page = StubPage()
    engine = object.__new__(page_engine.PageEngine)
    engine.page = page

    screenshot = engine.get_screenshot("home")

    expected = screenshot_directory / "home.png"
    assert screenshot == str(expected)
    assert page.saved_path == expected
    assert expected.read_bytes() == b"png"
