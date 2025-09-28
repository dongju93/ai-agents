from enum import Enum, StrEnum
from typing import Annotated, ClassVar

from crewai import LLM, Agent
from crewai.flow.flow import Flow, listen, or_, router, start
from pydantic import BaseModel, Field

from tools import web_search_tool


class BlogPost(BaseModel):
    title: str
    subtitle: str
    sections: list[str]


class Tweet(BaseModel):
    content: str
    hashtags: str


class LinkedInPost(BaseModel):
    hook: str
    content: str
    call_to_action: str


class Score(BaseModel):
    score: int = 0
    reason: str = ""


class ContentType(StrEnum):
    TWEET = "tweet"
    BLOG = "blog"
    LINKEDIN = "linkedin"


class ContentLength(int, Enum):
    SHORT = 150
    MEDIUM = 500
    LONG = 800


class ContentCreateEvent(StrEnum):
    CREATE_TWEET = "create_tweet"
    CREATE_BLOG = "create_blog"
    CREATE_LINKEDIN = "create_linkedin"


class ContentPipelineState(BaseModel):
    # user input
    content_type: Annotated[
        ContentType, Field(description="Type of content to generate")
    ] = ContentType.TWEET
    topic: Annotated[str, Field(description="Topic of the content to generate")] = ""

    # content maximum size
    max_length: Annotated[
        int, Field(description="Maximum length of the content to generate")
    ] = 0
    # content quality
    score: Annotated[
        Score | None, Field(description="Quality score of the generated content")
    ] = None
    # content
    tweet: Annotated[Tweet | None, Field(description="Generated tweet content")] = None
    blog_post: Annotated[
        BlogPost | None, Field(description="Generated blog content")
    ] = None
    linkedin_post: Annotated[
        LinkedInPost | None, Field(description="Generated linkedin content")
    ] = None

    # tools
    research: str = ""


class ContentPipelineFlow(Flow[ContentPipelineState]):
    INVALID_CONTENT_TYPE_MESSAGE: ClassVar[str] = "Invalid content type"

    @start()
    def init_content_pipeline(self) -> None:
        # strict content type
        if self.state.content_type not in [
            ContentType.TWEET,
            ContentType.BLOG,
            ContentType.LINKEDIN,
        ]:
            raise ValueError(self.INVALID_CONTENT_TYPE_MESSAGE)

        if self.state.topic == "":
            raise ValueError("Topic is required")

        if self.state.content_type == ContentType.TWEET:
            self.state.max_length = ContentLength.SHORT
        elif self.state.content_type == ContentType.BLOG:
            self.state.max_length = ContentLength.LONG
        elif self.state.content_type == ContentType.LINKEDIN:
            self.state.max_length = ContentLength.MEDIUM
        else:
            raise ValueError(self.INVALID_CONTENT_TYPE_MESSAGE)

    @listen(init_content_pipeline)
    def conduct_research(self):
        researcher: Agent = Agent(
            role="Head Researcher",
            backstory="You're like a digital detective who loves digging up fascinating facts and insights. You have a knack for finding the good stuff that others miss.",
            goal=f"Find the most interesting and useful info about {self.state.topic}",
            tools=[web_search_tool],  # type: ignore
        )

        self.state.research = researcher.kickoff(  # type: ignore
            f"Find the most interesting and useful info about {self.state.topic}"
        )

    @router(conduct_research)
    def route_content_creation(self) -> str:
        if self.state.content_type == ContentType.TWEET:
            return "create_tweet"  # Enum not working in here
        elif self.state.content_type == ContentType.BLOG:
            return "create_blog"
        elif self.state.content_type == ContentType.LINKEDIN:
            return "create_linkedin"
        else:
            raise ValueError(self.INVALID_CONTENT_TYPE_MESSAGE)

    @listen(or_(ContentCreateEvent.CREATE_TWEET, "reproduce_tweet"))
    def handle_create_tweet(self):
        llm = LLM(model="openai/o4-mini", response_format=Tweet)

        # if listen "reproduce_tweet" event, improve existing content otherwise create new content
        if self.state.tweet is None:
            # create content
            self.state.tweet = llm.call(  # type: ignore
                f"""
                Make a tweet on the topic {self.state.topic} using the following research:

                <research>
                {self.state.research}
                </research>
                """
            )
        else:
            # improve content
            self.state.tweet = llm.call(  # type: ignore
                f"""
                You wrote this tweet on {self.state.topic}, but it does not viral score because of {self.state.score.reason} 
                
                Improve it.

                <tweet>
                {self.state.tweet.model_dump_json()}
                </tweet>

                Use the following research.

                <research>
                {self.state.research}
                </research>
                """
            )

    @listen(or_(ContentCreateEvent.CREATE_BLOG, "reproduce_blog"))
    def handle_create_blog(self):
        print("Handling event: create_blog")

    @listen(or_(ContentCreateEvent.CREATE_LINKEDIN, "reproduce_linkedin"))
    def handle_create_linkedin(self):
        print("Handling event: create_linkedin")

    @listen(or_(handle_create_linkedin, handle_create_blog))
    def check_seo(self):
        print("Performing SEO check for blog content")

    @listen(handle_create_tweet)
    def check_viral(self):
        print(self.state.tweet)
        print("==========")
        print(self.state.research)
        print("Performing virality check for tweet content")

    @router(or_(check_seo, check_viral))
    def content_quality_check(self):
        content_type = self.state.content_type
        if self.state.score.score >= 8.0:
            print("Content quality is good, proceed finalization")
        else:
            match content_type:
                case ContentType.TWEET:
                    return "reproduce_tweet"
                case ContentType.BLOG:
                    return "reproduce_blog"
                case ContentType.LINKEDIN:
                    return "reproduce_linkedin"

    @listen(content_quality_check)
    def finalize_content_creation(self):
        print("Finalizing content creation process")


flow = ContentPipelineFlow().kickoff(
    inputs={
        "content_type": ContentType.TWEET,
        "topic": "The future of AI in healthcare",
    }
)

# flow.plot()
