import dotenv
from crewai import Agent, Crew, Task
from crewai.project import CrewBase, agent, crew, task

from tools import count_letters

dotenv.load_dotenv()


@CrewBase
class TranslationCrew:
    """
    이 클래스는 CrewAI 프레임워크를 기반으로 한 번역 크루를 정의합니다.

    주요 기능:
    - 번역 에이전트: 한국어에서 영어로의 번역을 수행합니다.
    - 카운터 에이전트: 주어진 문장에서 글자 수를 세는 도구를 사용합니다.
    - 태스크: 번역, 재번역, 글자 수 세기 작업을 포함합니다.

    크루는 이러한 에이전트와 태스크를 조합하여 복잡한 번역 워크플로우를 실행합니다.
    """

    @agent
    def translator_agent(self) -> Agent:
        return Agent(config=self.agents_config["translator_agent"])  # type: ignore

    @agent
    def counter_agent(self) -> Agent:
        return Agent(config=self.agents_config["counter_agent"], tools=[count_letters])  # type: ignore

    @task
    def translate_task(self) -> Task:
        return Task(config=self.tasks_config["translate_task"])  # type: ignore

    @task
    def retranslate_task(self) -> Task:
        return Task(config=self.tasks_config["retranslate_task"])  # type: ignore

    @task
    def counter_task(self) -> Task:
        return Task(config=self.tasks_config["counter_task"])  # type: ignore

    @crew
    def assemble_crew(self) -> Crew:
        return Crew(
            agents=[self.translator_agent(), self.counter_agent()],
            tasks=[self.translate_task(), self.retranslate_task(), self.counter_task()],
            verbose=True,
        )


# Crew 실행
TranslationCrew().assemble_crew().kickoff(
    inputs={"sentence": "AI 에이전트를 활용 할 수 있는 개발자만이 살아남을 것이다."}
)

"""
Output:

╭──────────────────────────────────────────── Crew Execution Started ────────────────────────────────────────────╮
│                                                                                                                │
│  Crew Execution Started                                                                                        │
│  Name: crew                                                                                                    │
│  ID: 37dd77c4-925e-4893-bc92-50bef3e6aafe                                                                      │
│  Tool Args:                                                                                                    │
│                                                                                                                │
│                                                                                                                │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯

🚀 Crew: crew
└── 📋 Task: translate_task (ID: a3abc9eb-e113-49c6-b0cc-076a93d9df87)
    Status: Executing Task...
╭─────────────────────────────────────────────── 🤖 Agent Started ───────────────────────────────────────────────╮
│                                                                                                                │
│  Agent: translator                                                                                             │
│                                                                                                                │
│  Task: Translate AI 에이전트를 활용 할 수 있는 개발자만이 살아남을 것이다. from Korean to English while        │
│  preserving the original meaning and context.                                                                  │
│                                                                                                                │
│                                                                                                                │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯

🚀 Crew: crew
└── 📋 Task: translate_task (ID: a3abc9eb-e113-49c6-b0cc-076a93d9df87)
    Status: Executing Task...
╭──────────────────────────────────────────── ✅ Agent Final Answer ─────────────────────────────────────────────╮
│                                                                                                                │
│  Agent: translator                                                                                             │
│                                                                                                                │
│  Final Answer:                                                                                                 │
│  Only developers who can utilize AI agents will survive.                                                       │
│                                                                                                                │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯

🚀 Crew: crew
└── 📋 Task: translate_task (ID: a3abc9eb-e113-49c6-b0cc-076a93d9df87)
    Assigned to: translator
    
    Status: ✅ Completed
╭─────────────────────────────────────────────── Task Completion ────────────────────────────────────────────────╮
│                                                                                                                │
│  Task Completed                                                                                                │
│  Name: translate_task                                                                                          │
│  Agent: translator                                                                                             │
│                                                                                                                │
│  Tool Args:                                                                                                    │
│                                                                                                                │
│                                                                                                                │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯

🚀 Crew: crew
├── 📋 Task: translate_task (ID: a3abc9eb-e113-49c6-b0cc-076a93d9df87)
│   Assigned to: translator
│   
│   Status: ✅ Completed
└── 📋 Task: retranslate_task (ID: 99085797-5963-4a23-80aa-8d2edd52008c)
    Status: Executing Task...
╭─────────────────────────────────────────────── 🤖 Agent Started ───────────────────────────────────────────────╮
│                                                                                                                │
│  Agent: translator                                                                                             │
│                                                                                                                │
│  Task: Translate AI 에이전트를 활용 할 수 있는 개발자만이 살아남을 것이다. from English to Swedish while       │
│  preserving the original meaning and context.                                                                  │
│                                                                                                                │
│                                                                                                                │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯

🚀 Crew: crew
├── 📋 Task: translate_task (ID: a3abc9eb-e113-49c6-b0cc-076a93d9df87)
│   Assigned to: translator
│   
│   Status: ✅ Completed
└── 📋 Task: retranslate_task (ID: 99085797-5963-4a23-80aa-8d2edd52008c)
    Status: Executing Task...
╭──────────────────────────────────────────── ✅ Agent Final Answer ─────────────────────────────────────────────╮
│                                                                                                                │
│  Agent: translator                                                                                             │
│                                                                                                                │
│  Final Answer:                                                                                                 │
│  Endast utvecklare som kan använda AI-agenter kommer att överleva.                                             │
│                                                                                                                │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯

🚀 Crew: crew
├── 📋 Task: translate_task (ID: a3abc9eb-e113-49c6-b0cc-076a93d9df87)
│   Assigned to: translator
│   
│   Status: ✅ Completed
└── 📋 Task: retranslate_task (ID: 99085797-5963-4a23-80aa-8d2edd52008c)
    Assigned to: translator
    
    Status: ✅ Completed
╭─────────────────────────────────────────────── Task Completion ────────────────────────────────────────────────╮
│                                                                                                                │
│  Task Completed                                                                                                │
│  Name: retranslate_task                                                                                        │
│  Agent: translator                                                                                             │
│                                                                                                                │
│  Tool Args:                                                                                                    │
│                                                                                                                │
│                                                                                                                │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯

🚀 Crew: crew
├── 📋 Task: translate_task (ID: a3abc9eb-e113-49c6-b0cc-076a93d9df87)
│   Assigned to: translator
│   
│   Status: ✅ Completed
├── 📋 Task: retranslate_task (ID: 99085797-5963-4a23-80aa-8d2edd52008c)
│   Assigned to: translator
│   
│   Status: ✅ Completed
└── 📋 Task: counter_task (ID: a6ecf607-749b-4b1e-b5c4-93fe029cd37a)
    Status: Executing Task...
╭─────────────────────────────────────────────── 🤖 Agent Started ───────────────────────────────────────────────╮
│                                                                                                                │
│  Agent: letter counter                                                                                         │
│                                                                                                                │
│  Task: Count the number of letters in the given sentence.                                                      │
│                                                                                                                │
│                                                                                                                │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯

🚀 Crew: crew
├── 📋 Task: translate_task (ID: a3abc9eb-e113-49c6-b0cc-076a93d9df87)
│   Assigned to: translator
│   
│   Status: ✅ Completed
├── 📋 Task: retranslate_task (ID: 99085797-5963-4a23-80aa-8d2edd52008c)
│   Assigned to: translator
│   
│   Status: ✅ Completed
└── 📋 Task: counter_task (ID: a6ecf607-749b-4b1e-b5c4-93fe029cd37a)
    Status: Executing Task...
    └── 🔧 Used count_letters (1)
╭─────────────────────────────────────────── 🔧 Agent Tool Execution ────────────────────────────────────────────╮
│                                                                                                                │
│  Agent: letter counter                                                                                         │
│                                                                                                                │
│  Thought: I need to count the number of letters in the given sentence.                                         │
│                                                                                                                │
│  Using Tool: count_letters                                                                                     │
│                                                                                                                │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭────────────────────────────────────────────────── Tool Input ──────────────────────────────────────────────────╮
│                                                                                                                │
│  "{\"sentence\": \"Only developers who can utilize AI agents will survive.\"}"                                 │
│                                                                                                                │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭───────────────────────────────────────────────── Tool Output ──────────────────────────────────────────────────╮
│                                                                                                                │
│  55                                                                                                            │
│                                                                                                                │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯

🚀 Crew: crew
├── 📋 Task: translate_task (ID: a3abc9eb-e113-49c6-b0cc-076a93d9df87)
│   Assigned to: translator
│   
│   Status: ✅ Completed
├── 📋 Task: retranslate_task (ID: 99085797-5963-4a23-80aa-8d2edd52008c)
│   Assigned to: translator
│   
│   Status: ✅ Completed
└── 📋 Task: counter_task (ID: a6ecf607-749b-4b1e-b5c4-93fe029cd37a)
    Status: Executing Task...
    ├── 🔧 Used count_letters (1)
    └── 🔧 Used count_letters (2)
╭─────────────────────────────────────────── 🔧 Agent Tool Execution ────────────────────────────────────────────╮
│                                                                                                                │
│  Agent: letter counter                                                                                         │
│                                                                                                                │
│  Thought: Thought: I have counted the letters in the first sentence. Now, I need to count the letters in the   │
│  second sentence.                                                                                              │
│                                                                                                                │
│  Using Tool: count_letters                                                                                     │
│                                                                                                                │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭────────────────────────────────────────────────── Tool Input ──────────────────────────────────────────────────╮
│                                                                                                                │
│  "{\"sentence\": \"Endast utvecklare som kan anv\\u00e4nda AI-agenter kommer att \\u00f6verleva.\"}"           │
│                                                                                                                │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭───────────────────────────────────────────────── Tool Output ──────────────────────────────────────────────────╮
│                                                                                                                │
│  65                                                                                                            │
│                                                                                                                │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯

🚀 Crew: crew
├── 📋 Task: translate_task (ID: a3abc9eb-e113-49c6-b0cc-076a93d9df87)
│   Assigned to: translator
│   
│   Status: ✅ Completed
├── 📋 Task: retranslate_task (ID: 99085797-5963-4a23-80aa-8d2edd52008c)
│   Assigned to: translator
│   
│   Status: ✅ Completed
└── 📋 Task: counter_task (ID: a6ecf607-749b-4b1e-b5c4-93fe029cd37a)
    Status: Executing Task...
    ├── 🔧 Used count_letters (1)
    └── 🔧 Used count_letters (2)
╭──────────────────────────────────────────── ✅ Agent Final Answer ─────────────────────────────────────────────╮
│                                                                                                                │
│  Agent: letter counter                                                                                         │
│                                                                                                                │
│  Final Answer:                                                                                                 │
│  55 letters in the first sentence and 65 letters in the second sentence.                                       │
│                                                                                                                │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯

🚀 Crew: crew
├── 📋 Task: translate_task (ID: a3abc9eb-e113-49c6-b0cc-076a93d9df87)
│   Assigned to: translator
│   
│   Status: ✅ Completed
├── 📋 Task: retranslate_task (ID: 99085797-5963-4a23-80aa-8d2edd52008c)
│   Assigned to: translator
│   
│   Status: ✅ Completed
└── 📋 Task: counter_task (ID: a6ecf607-749b-4b1e-b5c4-93fe029cd37a)
    Assigned to: letter counter
    
    Status: ✅ Completed
    ├── 🔧 Used count_letters (1)
    └── 🔧 Used count_letters (2)
╭─────────────────────────────────────────────── Task Completion ────────────────────────────────────────────────╮
│                                                                                                                │
│  Task Completed                                                                                                │
│  Name: counter_task                                                                                            │
│  Agent: letter counter                                                                                         │
│                                                                                                                │
│  Tool Args:                                                                                                    │
│                                                                                                                │
│                                                                                                                │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯

╭─────────────────────────────────────────────── Crew Completion ────────────────────────────────────────────────╮
│                                                                                                                │
│  Crew Execution Completed                                                                                      │
│  Name: crew                                                                                                    │
│  ID: 37dd77c4-925e-4893-bc92-50bef3e6aafe                                                                      │
│  Tool Args:                                                                                                    │
│  Final Output: 55 letters in the first sentence and 65 letters in the second sentence.                         │
│                                                                                                                │
│                                                                                                                │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
"""
