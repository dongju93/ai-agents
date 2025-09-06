from crewai import Agent, Crew, CrewOutput, Task
from crewai.project import CrewBase, agent, crew, task
from dotenv import load_dotenv

from tools import scrape_tool, search_tool

load_dotenv()
# Set code way to set model
# llm = LLM(
#     model="openai/gpt-5-nano",
#     reasoning_effort="low",
#     temperature=0.1,
# )


@CrewBase
class NewsReaderCrew:
    @agent
    def news_hunter_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["news_hunter_agent"],  # type: ignore
            tools=[search_tool, scrape_tool],
        )

    @agent
    def news_summarizer_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["news_summarizer_agent"],  # type: ignore
            tools=[scrape_tool],
        )

    @agent
    def news_curator_agent(self) -> Agent:
        return Agent(config=self.agents_config["news_curator_agent"])  # type: ignore

    # 각 Task 는 순차적으로 수행되며, 이전 Task 의 Output 를 다음 Task 의 Input 으로 사용함, 순서 중요
    @task
    def news_content_harvest_task(self) -> Task:
        return Task(config=self.tasks_config["news_content_harvest_task"])  # type: ignore

    @task
    def news_summarize_task(self) -> Task:
        return Task(config=self.tasks_config["news_summarize_task"])  # type: ignore

    @task
    def news_report_task(self) -> Task:
        return Task(config=self.tasks_config["news_report_task"])  # type: ignore

    @crew
    def news_union(self) -> Crew:
        return Crew(agents=self.agents, tasks=self.tasks, verbose=True)  # type: ignore


result: CrewOutput = (
    NewsReaderCrew()
    .news_union()
    .kickoff(inputs={"topic": "Latest advancements in AI technology"})
)

for task_output in result.tasks_output:
    print(task_output)
