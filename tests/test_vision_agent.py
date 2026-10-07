import asyncio
from types import SimpleNamespace

from cellenium.ai.agents.vision import crew as vision_crew


def test_run_vision_agent_moves_sync_kickoff_outside_active_event_loop(monkeypatch):
    inputs = {"image": ["screenshot.png"], "prompt": "what is displayed?"}
    expected = {"description": "search results"}
    calls = []

    class FakeCrew:
        def kickoff(self, received_inputs: dict):
            try:
                asyncio.get_running_loop()
            except RuntimeError:
                calls.append(received_inputs)
                return SimpleNamespace(
                    pydantic=SimpleNamespace(model_dump=lambda: expected)
                )
            raise RuntimeError(
                "Agent execution was invoked synchronously from within a running event loop."
            )

    class FakeVision:
        def crew(self):
            return FakeCrew()

    monkeypatch.setattr(vision_crew, "Vision", FakeVision)

    async def invoke_from_running_loop():
        return vision_crew.run_vision_agent(**inputs)

    response = asyncio.run(invoke_from_running_loop())

    assert response == expected
    assert calls == [inputs]
