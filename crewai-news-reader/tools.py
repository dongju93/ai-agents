import time

from bs4 import BeautifulSoup
from crewai.tools import tool
from crewai_tools import SerperDevTool
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright
from playwright.sync_api._generated import Browser, Page

load_dotenv()

search_tool = SerperDevTool(n_results=10)


# Crew.AI 는 docstring 을 Schema 로 보고 Tool 로 사용함
@tool
def count_letters(sentence: str) -> int:
    """
    This function is to count the number of letters in a given sentence.
    The input is a `sentence` string
    The output is a number.
    """
    return len(sentence)


UNWANTED_HTML_TAGS: list[str] = [
    "header",
    "footer",
    "nav",
    "aside",
    "script",
    "style",
    "noscript",
    "iframe",
    "form",
    "button",
    "input",
    "select",
    "textarea",
    "img",
    "svg",
    "canvas",
    "audio",
    "video",
    "embed",
    "object",
]


@tool
def scrape_tool(url: str) -> str:
    """
    This tool scrapes the text content from a given URL.
    Input: url (str) - The URL of the web page to scrape.
    Output: str - The cleaned text content of the page, or "No content" if empty.
    Example: scrape_tool("https://example.com") -> "This is the content of the page."
    """
    with sync_playwright() as p:
        # playwright 를 통해 브라우저 직접 제어
        browser: Browser = p.chromium.launch(headless=True)
        page: Page = browser.new_page()
        page.goto(url)
        time.sleep(5)
        raw_html: str = page.content()
        browser.close()

    # BeautifulSoup 를 통해 HTML 파싱
    soup = BeautifulSoup(raw_html, "html.parser")
    for tag in soup.find_all(UNWANTED_HTML_TAGS):
        tag.decompose()  # HTML 요소에서 불필요한 TAG 항목을 제거하여 Agent 에게 전달할 News Scrape 컨텐츠를 필터링함

    html: str = soup.get_text(separator=" ")

    return html if html != "" else "No content"
