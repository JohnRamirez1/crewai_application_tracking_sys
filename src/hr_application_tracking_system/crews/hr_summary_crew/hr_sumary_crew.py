from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from hr_types import  Candidate, CandidateKeywords
from tools.save_csv_file import SaveToCSVTool


@CrewBase
class HRSummaryCrew:
    """HR Resume Summary Crew"""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    @agent
    def resume_parser_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["resume_parser_agent"],
            tools=[SaveToCSVTool()],
            verbose=True,
            allow_delegation=False,
        )
    @agent
    def resume_keyword_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["resume_keyword_agent"],
            tools=[SaveToCSVTool()],
            verbose=True,
            allow_delegation=False,
        )
    
    @task
    def resume_parsing_task(self) -> Task:
        return Task(
            config=self.tasks_config["resume_parsing_task"],
            verbose=True,
            output_pydantic=Candidate,
        )

    @task
    def resume_keyword_extraction_task(self) -> Task:
        return Task(
            config=self.tasks_config["resume_keyword_extraction_task"],
            verbose=True,
            output_pydantic=CandidateKeywords,
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
