from collections.abc import Callable

from playwright.sync_api import Locator, Page

from src.core.functions.sheets import fetch_locators

# Selenium's find_element silently returns the first match; Playwright locators are
# strict-mode by default and raise on multiple matches, so each strategy here resolves
# to the first match (via .first) to keep that same "resolve to one element" semantics.
LOCATOR_MAP: dict[str, Callable[[Page, str], Locator]] = {
    "NAME": lambda page, v: page.locator(f'[name="{v}"]').first,
    "XPATH": lambda page, v: page.locator(f"xpath={v}").first,
    "ID": lambda page, v: page.locator(f"#{v}").first,
    "CSS": lambda page, v: page.locator(v).first,
    "CLASS_NAME": lambda page, v: page.locator(f".{v}").first,
    "LINK_TEXT": lambda page, v: page.get_by_text(v, exact=True).first,
    "TAG_NAME": lambda page, v: page.locator(v).first,
}


def get_entry(screen: str | None, name: str) -> dict[str, str]:
    """Look up a raw POM entry from the worksheet selected by screen."""
    entries = fetch_locators(screen)
    if name not in entries:
        raise KeyError(f"No locator named {name!r} on screen {screen!r}")

    return entries[name]


def get_locator(page: Page, screen: str | None, name: str) -> Locator:
    """Resolve a Google Sheets POM entry to a Playwright Locator."""
    entry = get_entry(screen, name)
    strategy = entry["type"]
    try:
        builder = LOCATOR_MAP[strategy]
    except KeyError:
        raise ValueError(f"Unsupported locator strategy {strategy!r} for {name!r} on screen {screen!r}")
    return builder(page, entry["value"])
