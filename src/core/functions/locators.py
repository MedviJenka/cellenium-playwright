"""Resolve POM entries (synced from the QA Google Sheet) into Playwright locators."""
import json
from pathlib import Path
from typing import Callable, Dict
from playwright.sync_api import Locator, Page

DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "locators.json"

LOCATOR_MAP: Dict[str, Callable[[Page, str], Locator]] = {
    "NAME": lambda page, v: page.locator(f'[name="{v}"]'),
    "XPATH": lambda page, v: page.locator(f"xpath={v}"),
    "ID": lambda page, v: page.locator(f"#{v}"),
    "CSS": lambda page, v: page.locator(v),
    "CLASS_NAME": lambda page, v: page.locator(f".{v}"),
    "LINK_TEXT": lambda page, v: page.get_by_text(v, exact=True),
    "TAG_NAME": lambda page, v: page.locator(v),
}


def _load(data_path: Path) -> Dict[str, Dict[str, str]]:
    if not data_path.exists():
        raise FileNotFoundError(
            f"{data_path} not found - run `python -m src.core.functions.sheets` to sync it first"
        )
    return json.loads(data_path.read_text(encoding="utf-8"))


def get_locator(page: Page, name: str, data_path: Path = DATA_PATH) -> Locator:
    """Resolve a POM entry (by its sheet `name`) to a Playwright Locator."""
    entries = _load(data_path)
    if name not in entries:
        raise KeyError(f"No locator named {name!r} in {data_path}")

    entry = entries[name]
    strategy = entry["type"]
    try:
        builder = LOCATOR_MAP[strategy]
    except KeyError:
        raise ValueError(f"Unsupported locator strategy {strategy!r} for {name!r}")
    return builder(page, entry["value"])
