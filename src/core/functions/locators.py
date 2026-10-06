"""Resolve POM entries (synced from the QA Google Sheet) into Playwright locators."""
import json
from pathlib import Path
from typing import Callable, Dict, Optional
from playwright.sync_api import Locator, Page

DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "locators.json"

# Selenium's find_element silently returns the first match; Playwright locators are
# strict-mode by default and raise on multiple matches, so each strategy here resolves
# to the first match (via .first) to keep that same "resolve to one element" semantics.
LOCATOR_MAP: Dict[str, Callable[[Page, str], Locator]] = {
    "NAME": lambda page, v: page.locator(f'[name="{v}"]').first,
    "XPATH": lambda page, v: page.locator(f"xpath={v}").first,
    "ID": lambda page, v: page.locator(f"#{v}").first,
    "CSS": lambda page, v: page.locator(v).first,
    "CLASS_NAME": lambda page, v: page.locator(f".{v}").first,
    "LINK_TEXT": lambda page, v: page.get_by_text(v, exact=True).first,
    "TAG_NAME": lambda page, v: page.locator(v).first,
}


def _load(data_path: Path) -> Dict[str, Dict[str, Dict[str, str]]]:
    if not data_path.exists():
        raise FileNotFoundError(
            f"{data_path} not found - run `python -m src.core.functions.sheets` to sync it first"
        )
    return json.loads(data_path.read_text(encoding="utf-8"))


def get_entry(screen: Optional[str], name: str, data_path: Path = DATA_PATH) -> Dict[str, str]:
    """Look up the raw POM entry (type/value/actions/comments) for a screen + name."""
    screens = _load(data_path)

    if screen not in screens:
        raise KeyError(f"No screen named {screen!r} in {data_path}")

    entries = screens[screen]
    if name not in entries:
        raise KeyError(f"No locator named {name!r} on screen {screen!r} in {data_path}")

    return entries[name]


def get_locator(page: Page, screen: Optional[str], name: str, data_path: Path = DATA_PATH) -> Locator:
    """Resolve a POM entry (by its sheet `screen` tab + `name` row) to a Playwright Locator."""
    entry = get_entry(screen, name, data_path)
    strategy = entry["type"]
    try:
        builder = LOCATOR_MAP[strategy]
    except KeyError:
        raise ValueError(f"Unsupported locator strategy {strategy!r} for {name!r} on screen {screen!r}")
    return builder(page, entry["value"])
