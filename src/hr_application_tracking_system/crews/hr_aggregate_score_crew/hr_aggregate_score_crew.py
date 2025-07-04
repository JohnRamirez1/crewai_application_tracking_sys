from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from hr_types import  ScoredCandidate
# @st.cache_resource
# def load_llm():
#     llm = LLM(
#         model="ollama/llama3.2:1b",
#         base_url="http://localhost:11434"
#     )
#     return llm


@CrewBase
class HRAggregatorCrew:
    """HR Score Aggregator Crew"""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    @agent
    def final_score_aggregator_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["final_score_aggregator_agent"],
            # llm=load_llm(),
            verbose=False,
            allow_delegation=False,
        )
    

    @task
    def final_score_aggregating_task(self) -> Task:
        return Task(
            config=self.tasks_config["final_score_aggregating_task"],
            verbose=False,
            output_pydantic=ScoredCandidate
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Lead Response Crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
