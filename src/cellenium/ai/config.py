from asyncio import Task
from crewai import LLM
from cellenium.settings import get_config
from functools import cached_property
from crewai.agents.agent_builder.base_agent import BaseAgent


class AgentConfig:

    agents: list[BaseAgent]
    tasks: list[Task]
    agents_config: dict = 'config/agents.yaml'
    tasks_config: dict = 'config/tasks.yaml'

    @cached_property
    def llm(self) -> LLM:
        return LLM(model=get_config().OPENAI_MODEL)
