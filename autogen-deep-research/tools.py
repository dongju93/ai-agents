import re
from os import environ
from typing import TypedDict

from firecrawl import Firecrawl
from firecrawl.v2.types import Document, ScrapeOptions, SearchData, SearchResultWeb

FIRECRAWL_API_KEY: str = environ["FIRECRAWL_API_KEY"]

CONTENT_CLEANER: re.Pattern[str] = re.compile(
    r"\\+|\n|\[[^\]]+\]\([^\)]+\)|https?://[^\s]+"
)


class WebSearchResults(TypedDict):
    title: str
    url: str
    markdown: str


def web_search_tool(query: str) -> list[WebSearchResults] | str:
    """
    Searches the web for general information.

    Use this tool to find information from various web sources.
    Be specific with your search queries to get better results.

    Args:
        query (str): Search query string.

    Returns:
        list[WebSearchResults] | str: List of search results with title, url, and content.
        Returns error string if search fails.

    Examples:
        web_search_tool("latest news on AI")
        web_search_tool("Python tutorials")
        web_search_tool("weather in Seoul")
    """
    firecrawl = Firecrawl(api_key=FIRECRAWL_API_KEY)
    results: SearchData = firecrawl.search(
        query=query,
        limit=1,
        sources=["web"],
        scrape_options=ScrapeOptions(formats=["markdown"]),
    )

    searched_chunks: list[WebSearchResults] = []
    title: str | None = None
    url: str | None = None
    content: str | None = None

    if not results.web:
        return "Error in web search tool use."

    for item in results.web:
        if isinstance(item, Document):
            title = item.metadata.title if item.metadata else None
            url = item.metadata.url if item.metadata else None
            content = item.markdown
        elif isinstance(item, SearchResultWeb):
            title = item.title
            url = item.url
            content = item.description

        assert title is not None
        assert url is not None
        assert content is not None

        cleaned_content: str = CONTENT_CLEANER.sub("", content).strip()

        searched_chunks.append(
            WebSearchResults(title=title, url=url, markdown=cleaned_content)
        )

    return searched_chunks
