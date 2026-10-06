import pytest
from src.core.engine.page_engine import PageEngine


class TestGoogleSearch:

    @pytest.mark.parametrize('engine', ['Google'], indirect=True)
    def test_cats(self, engine: PageEngine) -> None:
        engine.get_web("https://www.google.com")
        engine.get_element("search").fill("cats")
        engine.get_element("button").click()
        engine.get_screenshot()
