from crewai.tools import tool


# Crew.AI 는 docstring 을 Schema 로 보고 Tool 로 사용함
@tool
def count_letters(sentence: str) -> int:
    """
    This function is to count the number of letters in a given sentence.
    The input is a `sentence` string
    The output is a number.
    """
    return len(sentence)
