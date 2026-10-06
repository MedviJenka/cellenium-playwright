"""Sync Page Object Model locators from a Google Sheet via a service account.

Uses gspread with a service-account credentials.json (no "anyone with the
link" sharing required) - the sheet just needs to be shared with the service
account's client_email (see credentials.json) as a Viewer.

Sheet columns (per the QA team's POM sheet):
    name    - identifier used to look up the locator in code
    locator - the strategy, e.g. NAME / XPATH / ID / CSS
    type    - the actual locator value (confusingly named, but matches the sheet)
    actions - optional
    comments - optional
"""
import json
import re
import gspread
from dataclasses import dataclass
from pathlib import Path
from typing import Optional
from settings import Config

CREDENTIALS_PATH = Path(__file__).resolve().parent.parent.parent.parent / "credentials.json"
OUTPUT_PATH = Path(__file__).resolve().parent.parent / "data" / "locators.json"

_ID_RE = re.compile(r"/spreadsheets/d/([a-zA-Z0-9-_]+)")
_GID_RE = re.compile(r"[?#&]gid=(\d+)")


def _parse_sheet_ref(raw: str) -> tuple[str, Optional[int]]:
    """Accept either a bare spreadsheet ID or a full edit URL (with gid)."""
    id_match = _ID_RE.search(raw)
    spreadsheet_id = id_match.group(1) if id_match else raw
    gid_match = _GID_RE.search(raw)
    gid = int(gid_match.group(1)) if gid_match else None
    return spreadsheet_id, gid


def fetch_locators(credentials_path: Path = CREDENTIALS_PATH) -> dict[str, dict[str, str]]:
    """Pull the POM sheet. Returns {name: {type, value, actions, comments}}."""
    spreadsheet_id, gid = _parse_sheet_ref(Config.GOOGLE_SHEETS)

    gc = gspread.service_account(filename=str(credentials_path))
    spreadsheet = gc.open_by_key(spreadsheet_id)
    worksheet = spreadsheet.get_worksheet_by_id(gid) if gid is not None else spreadsheet.sheet1

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


def sync_locators(output_path: Path = OUTPUT_PATH) -> Path:
    """Fetch the sheet and cache it as JSON so tests don't hit the API at runtime."""
    locators = fetch_locators()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(locators, indent=2), encoding="utf-8")
    return output_path


@dataclass
class GoogleSheets:

    



if __name__ == "__main__":
    path = sync_locators()
    print(f"Synced locators -> {path}")
