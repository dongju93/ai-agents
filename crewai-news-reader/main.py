import dotenv
from crewai import Agent, Crew, Task
from crewai.project import CrewBase, agent, crew, task

dotenv.load_dotenv()


@CrewBase
class TranslationCrew:
    @agent
    def translator_agent(self) -> Agent:
        return Agent(config=self.agents_config["translator_agent"])  # type: ignore

    @task
    def translate_task(self) -> Task:
        return Task(config=self.tasks_config["translate_task"])  # type: ignore

    @task
    def retranslate_task(self) -> Task:
        return Task(config=self.tasks_config["retranslate_task"])  # type: ignore

    @crew
    def assemble_crew(self) -> Crew:
        return Crew(
            agents=[self.translator_agent()],
            tasks=[self.translate_task(), self.retranslate_task()],
            verbose=True,
        )


TranslationCrew().assemble_crew().kickoff(
    inputs={"sentence": "AI 에이전트를 활용 할 수 있는 개발자만이 살아남을 것이다."}
)

"""
Output:

╭──────────────────────────────────────────── Crew Execution Started ────────────────────────────────────────────╮
│                                                                                                                │
│  Crew Execution Started                                                                                        │
│  Name: crew                                                                                                    │
│  ID: d1c53323-9d0c-4bda-84cd-c0a4e0d412df                                                                      │
│  Tool Args:                                                                                                    │
│                                                                                                                │
│                                                                                                                │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯

🚀 Crew: crew
└── 📋 Task: translate_task (ID: 251c1288-efa0-4604-b18c-efbbfc9b76bb)
    Status: Executing Task...
╭─────────────────────────────────────────────── 🤖 Agent Started ───────────────────────────────────────────────╮
│                                                                                                                │
│  Agent: "translator"                                                                                           │
│                                                                                                                │
│  Task: "Translate AI 에이전트를 활용 할 수 있는 개발자만이 살아남을 것이다. from Korean to English while       │
│  preserving the original meaning and context."                                                                 │
│                                                                                                                │
│                                                                                                                │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯

🚀 Crew: crew
└── 📋 Task: translate_task (ID: 251c1288-efa0-4604-b18c-efbbfc9b76bb)
    Status: Executing Task...
╭──────────────────────────────────────────── ✅ Agent Final Answer ─────────────────────────────────────────────╮
│                                                                                                                │
│  Agent: "translator"                                                                                           │
│                                                                                                                │
│  Final Answer:                                                                                                 │
│  Only developers who can utilize AI agents will survive.                                                       │
│                                                                                                                │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯

🚀 Crew: crew
└── 📋 Task: translate_task (ID: 251c1288-efa0-4604-b18c-efbbfc9b76bb)
    Assigned to: "translator"
    
    Status: ✅ Completed
╭─────────────────────────────────────────────── Task Completion ────────────────────────────────────────────────╮
│                                                                                                                │
│  Task Completed                                                                                                │
│  Name: translate_task                                                                                          │
│  Agent: "translator"                                                                                           │
│                                                                                                                │
│  Tool Args:                                                                                                    │
│                                                                                                                │
│                                                                                                                │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯

╭─────────────────────────────────────────────── Crew Completion ────────────────────────────────────────────────╮
│                                                                                                                │
│  Crew Execution Completed                                                                                      │
│  Name: crew                                                                                                    │
│  ID: d1c53323-9d0c-4bda-84cd-c0a4e0d412df                                                                      │
│  Tool Args:                                                                                                    │
│  Final Output: Only developers who can utilize AI agents will survive.                                         │
│                                                                                                                │
│                                                                                                                │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
"""
