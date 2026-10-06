import importlib
import sys
import types

import pytest


def _load_sheets(monkeypatch):
    settings = types.ModuleType("settings")
    settings.Config = types.SimpleNamespace(
        GOOGLE_SHEETS="https://docs.google.com/spreadsheets/d/sheet-id/edit"
    )
    monkeypatch.setitem(sys.modules, "settings", settings)
    sys.modules.pop("src.core.functions.sheets", None)
    return importlib.import_module("src.core.functions.sheets")


def test_fetch_locators_reads_only_the_selected_screen(monkeypatch, tmp_path):
    sheets = _load_sheets(monkeypatch)
    selected_screens = []

    class Worksheet:
        def get_all_values(self):
            return [
                ["name", "locator", "type", "actions", "comments"],
                ["search", "NAME", "q", "fill", "Google search input"],
            ]

    class Spreadsheet:
        def worksheet(self, screen):
            selected_screens.append(screen)
            return Worksheet()

    class Client:
        def open_by_key(self, spreadsheet_id):
            assert spreadsheet_id == "sheet-id"
            return Spreadsheet()

    credentials = tmp_path / "credentials.json"
    monkeypatch.setattr(sheets.gspread, "service_account", lambda *, filename: Client())

    locators = sheets.fetch_locators("Google", credentials_path=credentials)

    assert selected_screens == ["Google"]
    assert locators == {
        "search": {
            "type": "NAME",
            "value": "q",
            "actions": "fill",
            "comments": "Google search input",
        }
    }


def test_fetch_locators_requires_a_screen(monkeypatch, tmp_path):
    sheets = _load_sheets(monkeypatch)

    with pytest.raises(ValueError, match="screen"):
        sheets.fetch_locators(None, credentials_path=tmp_path / "credentials.json")


def test_get_entry_reads_the_requested_screen_directly(monkeypatch):
    sheets = types.ModuleType("src.core.functions.sheets")
    requested_screens = []

    def fetch_locators(screen):
        requested_screens.append(screen)
        return {"search": {"type": "NAME", "value": "q", "actions": "", "comments": ""}}

    sheets.fetch_locators = fetch_locators
    monkeypatch.setitem(sys.modules, "src.core.functions.sheets", sheets)
    sys.modules.pop("src.core.functions.locators", None)
    locators = importlib.import_module("src.core.functions.locators")

    entry = locators.get_entry("Google", "search")

    assert requested_screens == ["Google"]
    assert entry["value"] == "q"
