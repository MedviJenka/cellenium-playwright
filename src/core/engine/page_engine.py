import uuid
from dataclasses import dataclass
from pathlib import Path
from typing import Literal, Optional
from playwright.sync_api import Locator
from src.core.engine.manager import BrowserManager
from src.core.functions.locators import get_entry, get_locator
from src.core.functions.logger import Logger


SCREENSHOTS = Path(__file__).resolve().parent.parent / "data" / "screenshots"

log = Logger(name='browser-manager')


@dataclass
class PageEngine(BrowserManager):

    screen: Optional[str] = None

    def get_web(self, url: str) -> None:
        self.page.goto(url)
        log.fire(message=f'web opened: {url} using: {self.screen} screen')

    def get_element(self, name: str, timeout: int = 10_000) -> Locator:
        locator = get_locator(self.page, self.screen, name)
        locator.wait_for(state="attached", timeout=timeout)
        log.fire(message=f'element used: {name}')
        return locator

    def get_dynamic_element(self, attribute: str, name: str) -> Locator:
        # explanation ............ //*[contains(@<attribute>, <name>)]
        # example ................ //*[contains(@name, "btnK")]
        entry = get_entry(self.screen, name)
        path = f"//*[contains(@{attribute}, '{entry['value']}')]"
        return self.page.locator(f"xpath={path}")

    def wait_for_element(self, name: str, timeout: int = 5_000) -> Locator:
        locator = get_locator(self.page, self.screen, name)
        locator.wait_for(state="visible", timeout=timeout)
        log.fire(message=f'waiting for element: {name}')
        return locator

    def get_screenshot(self, name: Optional[str] = None) -> str:
        SCREENSHOTS.mkdir(parents=True, exist_ok=True)
        file_name = f"{name or uuid.uuid4()}.png"
        path = SCREENSHOTS / file_name
        self.page.screenshot(path=str(path))
        return str(path)

    def dropdown(self, name: str, label: str) -> None:
        self.get_element(name).select_option(label=label)

    def count_elements(self, name: str, tag: str) -> int:
        count = self.get_element(name).locator(tag).count()
        print(f"number of rows in this page is: {count}")
        return count

    def count_rows(self, name: str, structure: str) -> int:
        return self.get_element(name).locator(structure).count()

    def press_keyboard_key(self, key: str) -> None:
        self.page.keyboard.press(f"Control+{key}")

    def scroll_page(self, direction: Literal['up', 'down'], px: int) -> None:
        match direction:
            case "up":
                self.page.mouse.wheel(0, -px)
            case "down":
                self.page.mouse.wheel(0, px)

    def switch_to_new_tab(self, url: str) -> None:
        new_page = self.context.new_page()
        new_page.goto(url)
        log.fire(message=f'url switched to {url}')

    def switch_to_main_tab(self) -> None:
        self.page = self.context.pages[0]
        self.page.bring_to_front()
