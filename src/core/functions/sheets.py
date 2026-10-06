"""Read Page Object Model locators directly from Google Sheets.
Uses gspread with a service-account credentials.json (no "anyone with the
link" sharing required) - the sheet just needs to be shared with the service
account's client_email (see credentials.json) as a Viewer.

Each worksheet (tab) in the spreadsheet is one screen. Callers select the
worksheet by passing the same screen name used by ``PageEngine``.

Sheet columns (per the QA team's POM sheet):
    name    - identifier used to look up the locator in code
    locator - the strategy, e.g. NAME / XPATH / ID / CSS
    type    - the actual locator value (confusingly named, but matches the sheet)
    actions - optional
    comments - optional
"""
import re
from pathlib import Path

import gspread

from settings import Config

CREDENTIALS_PATH = Path(__file__).resolve().parent.parent.parent.parent / "credentials.json"

_ID_RE = re.compile(r"/spreadsheets/d/([a-zA-Z0-9-_]+)")


def _parse_sheet_id(raw: str) -> str:
    """Accept either a bare spreadsheet ID or a full edit URL."""
    id_match = _ID_RE.search(raw)
    return id_match.group(1) if id_match else raw


def _parse_worksheet(worksheet: gspread.Worksheet) -> dict[str, dict[str, str]]:
    rows = worksheet.get_all_values()
    if not rows:
        return {}

    header = [h.strip().lower() for h in rows[0]]
    locators: dict[str, dict[str, str]] = {}
    for row in rows[1:]:
        record = dict(zip(header, row))
        name = record.get("name", "").strip()
        if not name:
            continue
        locators[name] = {
            "type": record.get("locator", "").strip().upper(),
            "value": record.get("type", "").strip(),
            "actions": record.get("actions", "").strip(),
            "comments": record.get("comments", "").strip(),
        }
    return locators


def fetch_locators(
    screen: str | None,
    credentials_path: Path = CREDENTIALS_PATH,
) -> dict[str, dict[str, str]]:
    """Read all locator rows from one worksheet selected by screen name."""
    if not screen:
        raise ValueError("screen is required to select a Google Sheets worksheet")

    spreadsheet_id = _parse_sheet_id(Config.GOOGLE_SHEETS)
    gc = gspread.service_account(filename=str(credentials_path))
    spreadsheet = gc.open_by_key(spreadsheet_id)

    try:
        worksheet = spreadsheet.worksheet(screen)
    except gspread.WorksheetNotFound as exc:
        raise KeyError(f"No worksheet named {screen!r} in the configured Google Sheet") from exc

    return _parse_worksheet(worksheet)
