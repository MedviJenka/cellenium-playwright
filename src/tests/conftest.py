import pytest
from src.core.engine.page_engine import PageEngine


@pytest.fixture
def engine():
    page_engine = PageEngine(screen="Google", headless=False)
    yield page_engine
    page_engine.teardown()
