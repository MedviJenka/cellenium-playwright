"""Bootstrap a Playwright browser/context/page.

Playwright ships and manages its own browser binaries (one-time setup:
`playwright install chromium`) - unlike Selenium, there is no driver-manager
download step to wire up here.
"""
from typing import Optional
from dataclasses import dataclass, field
from playwright.sync_api import sync_playwright, Browser, BrowserContext, Page, Playwright


@dataclass
class BrowserManager:

    """
    Launches a Playwright browser, context, and page for the lifetime of the instance.

    :param headless: run without a visible UI window.
    :param browser_name: one of "chromium", "firefox", "webkit".
    :param http_credentials: optional {"username": ..., "password": ...} for HTTP basic
        auth - Playwright only accepts this at context-creation time, so it is a
        constructor field here rather than a runtime method.
    """

    headless: bool = False
    browser_name: str = "chromium"
    http_credentials: Optional[dict] = None
    playwright: Playwright = field(init=False, repr=False)
    browser: Browser = field(init=False, repr=False)
    context: BrowserContext = field(init=False, repr=False)
    page: Page = field(init=False, repr=False)

    def __post_init__(self) -> None:
        self.playwright = sync_playwright().start()
        launcher = getattr(self.playwright, self.browser_name)
        self.browser = launcher.launch(headless=self.headless)
        self.context = self.browser.new_context(http_credentials=self.http_credentials)
        self.page = self.context.new_page()

    def teardown(self) -> None:
        self.page.close()
        self.context.close()
        self.browser.close()
        self.playwright.stop()
