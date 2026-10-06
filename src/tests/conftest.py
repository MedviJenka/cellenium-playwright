from collections.abc import Generator

import pytest

from src.core.engine.page_engine import PageEngine


@pytest.fixture
def engine(request: pytest.FixtureRequest) -> Generator[PageEngine]:
    page_engine = PageEngine(screen=request.param)
    try:
        yield page_engine
    finally:
        page_engine.teardown()
