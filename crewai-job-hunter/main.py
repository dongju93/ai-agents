from crewai import Agent, Crew, Task
from crewai.project import CrewBase, agent, crew, task
from dotenv import load_dotenv

from models import ChosenJob, JobList, RankedJobList
from tools import web_search_tool

load_dotenv()


@CrewBase
class JobHunterCrew:
    @agent
    def job_search_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["job_search_agent"],  # type: ignore
            tools=[web_search_tool],
        )

    @agent
    def job_matching_agent(self) -> Agent:
        return Agent(config=self.agents_config["job_matching_agent"])  # type: ignore

    @agent
    def resume_optimization_agent(self) -> Agent:
        return Agent(config=self.agents_config["resume_optimization_agent"])  # type: ignore

    @agent
    def company_research_agent(self) -> Agent:
        return Agent(config=self.agents_config["company_research_agent"])  # type: ignore

    @agent
    def interview_prep_agent(self) -> Agent:
        return Agent(config=self.agents_config["interview_prep_agent"])  # type: ignore

    @task
    def job_extraction_task(self) -> Task:
        return Task(
            config=self.tasks_config["job_extraction_task"],  # type: ignore
            output_pydantic=JobList,  # structured output
        )

    @task
    def job_matching_task(self) -> Task:
        return Task(
            config=self.tasks_config["job_matching_task"],  # type: ignore
            output_pydantic=RankedJobList,
        )

    @task
    def job_selection_task(self) -> Task:
        return Task(
            config=self.tasks_config["job_selection_task"],  # type: ignore
            output_pydantic=ChosenJob,
        )

    @task
    def resume_rewriting_task(self) -> Task:
        return Task(config=self.tasks_config["resume_rewriting_task"])  # type: ignore

    @task
    def company_research_task(self) -> Task:
        return Task(
            config=self.tasks_config["company_research_task"],  # type: ignore
            context=[self.job_selection_task()],
        )

    @task
    def interview_prep_task(self) -> Task:
        return Task(
            config=self.tasks_config["interview_prep_task"],  # type: ignore
            context=[
                self.job_selection_task(),
                self.resume_rewriting_task(),
                self.company_research_task(),
            ],  # Linear 하지 않은 이전 task 의 output 을 해당 task 의 context 로 사용할 수 있음
        )

    @crew
    def crew(self) -> Crew:
        return Crew(agents=self.agents, tasks=self.tasks, verbose=True)  # type: ignore


JobHunterCrew().crew().kickoff()
