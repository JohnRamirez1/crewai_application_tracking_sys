from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from hr_types import MatchingAnalysis, ScoredCandidate

# @st.cache_resource
# def load_llm():
#     llm = LLM(
#         model="ollama/llama3.2:1b",
#         base_url="http://localhost:11434"
#     )
#     return llm

@CrewBase
class HRScoreCrew:
    """HR Score Response Crew"""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"
    
    @agent
    def matching_algorithm(self) -> Agent:
        return Agent(
            config=self.agents_config["matching_algorithm"],
            # llm=load_llm(),
            verbose=False,
            allow_delegation=False,
        )
    
    @agent
    def scoring_system(self) -> Agent:
        return Agent(
            config=self.agents_config["scoring_system"],
            # llm=load_llm(),
            verbose=False,
            allow_delegation=False,
        )
   
    
    @task
    def matching_task(self) -> Task:
        return Task(
            config=self.tasks_config["matching_task"],
            verbose=False,
            output_pydantic=MatchingAnalysis,
        )
    
    @task
    def resume_scoring_task(self) -> Task:
        return Task(
            config=self.tasks_config["resume_scoring_task"],
            verbose=False,
            output_pydantic=ScoredCandidate,
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
