from pathlib import Path
from cellenium.ai.config import AgentConfig
from crewai import Agent, Crew, Task
from cellenium.ai.agents.vision.schemas import VisionSchema
from cellenium.ai.agents.vision.tools.vision import VisionTool
from crewai.project import CrewBase, agent, crew, task


SKILLS = Path(__file__).resolve().parent / "skills"


@CrewBase
class Vision(AgentConfig):

    @agent
    def vision(self) -> Agent:
        return Agent(config=self.agents_config["vision"], llm=self.llm, skills=[SKILLS])

    @task
    def vision_task(self) -> Task:
        return Task(config=self.tasks_config["vision_task"], output_pydantic=VisionSchema, tools=[VisionTool(llm=self.llm)])

    @crew
    def crew(self) -> Crew:
        return Crew(agents=self.agents, tasks=self.tasks, verbose=True)


def run_vision_agent(image: list[str], prompt: str) -> VisionSchema:
    return Vision().crew().kickoff({'image': image, 'prompt': prompt}).pydantic.model_dump()


if __name__ == '__main__':
    print(run_vision_agent(prompt='what is displayed?', image=[r'C:\Users\medvi\OneDrive\Desktop\checklist\data\screenshots\img.png']))
