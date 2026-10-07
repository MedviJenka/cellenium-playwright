"""
Read Page Object Model locators directly from Google Sheets.
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

import gspread
from pathlib import Path
from typing import Optional
from functions.logger import Logger
from settings import Config


log = Logger('sheets-logic')


def _parse_worksheet(worksheet: gspread.Worksheet) -> dict[str, dict[str, str]]:

    rows = worksheet.get_all_values()

    if not rows:
        log.fire(message='no rows were found', level='debug')
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


def fetch_locators(screen: Optional[str] = None, credentials_path: Path = Config.CREDENTIALS_JSON) -> dict[str, dict]:
    """Read all locator rows from one worksheet selected by screen name."""
    if not screen:
        log.fire(message='screen is required to select a Google Sheets worksheet', level='error')
        raise ValueError

    gc = gspread.service_account(filename=str(credentials_path))
    spreadsheet = gc.open_by_url(Config.GOOGLE_SHEETS)

    try:
        worksheet = spreadsheet.worksheet(screen)

    except gspread.WorksheetNotFound as e:
        log.fire(f"No worksheet named {screen!r} in the configured Google Sheet", level='error')
        raise ValueError from e

    return _parse_worksheet(worksheet)
