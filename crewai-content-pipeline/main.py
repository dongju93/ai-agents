from typing import Literal

from crewai.flow.flow import Flow, and_, listen, router, start
from pydantic import BaseModel


class FlowState(BaseModel):  # 상태 모델 (struct)
    flow_id: int = 0
    flow_state: Literal["initial", "running", "completed"] = "initial"


class MyFirstFlow(Flow[FlowState]):
    """
    Flow 는 여러개의 method(function) 를 지닌 class
    언제 method 를 실행 할지, method 의 event 를 감지 할지 정할 수 있음
    """

    @start()
    def first(self) -> None:
        self.state.flow_id = 1  # 메서드 간에 데이터를 공유하고, 실행 상태를 추적
        self.state.flow_state = "initial"
        print(self.state.flow_id)
        print(self.state.flow_state)
        print("Hello")

    @listen(first)  # first 이벤트 종료 감지
    def second(self) -> None:
        self.state.flow_id = 2
        self.state.flow_state = "running"
        print(self.state.flow_id)
        print(self.state.flow_state)
        print("World")

    @listen(first)
    def third(self) -> None:
        self.state.flow_id = 3
        self.state.flow_state = "running"
        print(self.state.flow_id)
        print(self.state.flow_state)
        print("Again")

    @listen(and_(second, third))  # and_ 두 이벤트 모두 종료 감지
    def fourth(self) -> None:
        self.state.flow_id = 4
        self.state.flow_state = "running"
        print(self.state.flow_id)
        print(self.state.flow_state)
        print("😀")

    @router(fourth)
    def fifth(self) -> str:
        self.state.flow_id = 5
        self.state.flow_state = "running"
        print(self.state.flow_id)
        print(self.state.flow_state)
        a = 2
        if a == 2:
            return "even"  # 이벤트를 발생(emit) 시킴
        else:
            return "odd"

    @listen("even")  # 함수가 발생한 이벤트를 감지
    def even_listener(self) -> None:
        self.state.flow_id = 6
        self.state.flow_state = "completed"
        print(self.state.flow_id)
        print(self.state.flow_state)
        print("짝수입니다.")

    @listen("odd")
    def odd_listener(self) -> None:
        self.state.flow_id = 7
        self.state.flow_state = "completed"
        print(self.state.flow_id)
        print(self.state.flow_state)
        print("홀수입니다.")


flow = MyFirstFlow()

flow.plot()
flow.kickoff()
