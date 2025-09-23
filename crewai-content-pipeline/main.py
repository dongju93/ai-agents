from crewai.flow.flow import Flow, and_, listen, start


class MyFirstFlow(Flow):
    """
    Flow 는 여러개의 method(function) 를 지닌 class
    언제 method 를 실행 할지, method 의 event 를 감지 할지 정할 수 있음
    """

    @start()
    def first(self) -> None:
        print("Hello")

    @listen(first)  # first 이벤트 종료 감지
    def second(self) -> None:
        print("World")

    @listen(first)  # first 이벤트 종료 감지
    def third(self) -> None:
        print("Again")

    @listen(and_(second, third))  # and_ 두 이벤트 모두 종료 감지
    def fourth(self) -> None:
        print("😀")


flow = MyFirstFlow()

flow.plot()
