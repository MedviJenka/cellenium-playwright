import pytest
from cellenium.ai.agents.vision.crew import run_vision_agent
from cellenium.engine.page_engine import PageEngine
from cellenium.functions.logger import Logger


log = Logger(name='google sanity')


class TestGoogleSearch:

    @pytest.mark.parametrize('engine', ['Google'], indirect=True)
    def test_cats(self, engine: PageEngine) -> None:
        engine.get_web("https://www.google.com")
        engine.get_element("search").fill("cats")
        engine.get_element("button").click()
        sc = engine.get_screenshot()
        response = run_vision_agent(prompt='what is displayed?', image=[sc])
        log.fire(f'ai response:\n{response}')
        assert response['confidence_level'] > 80, log.fire(message=f'test failed, confidence level is {response['confidence_level']}', level='error')
