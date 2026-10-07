import pytest
from src.core.engine.page_engine import PageEngine
from src.core.functions.logger import Logger


log = Logger(name='google sanity')


class TestGoogleSearch:

    @pytest.mark.parametrize('engine', ['Google'], indirect=True)
    def test_cats(self, engine: PageEngine) -> None:
        engine.get_web("https://www.google.com")
        engine.get_element("search").fill("cats")
        engine.get_element("button").click()
        engine.get_screenshot()
        log.fire('test complete')
