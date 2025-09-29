from datetime import datetime
from enum import Enum, StrEnum
from pathlib import Path
from typing import Annotated, ClassVar

from crewai import LLM, Agent
from crewai.flow.flow import Flow, listen, or_, router, start
from pydantic import BaseModel, Field

from seo_crew import Score, SeoCrew
from tools import web_search_tool
from virality_crew import ViralityCrew


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
        Score, Field(description="Quality score of the generated content")
    ] = Score()
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
            llm_response = llm.call(
                f"""
                Make a tweet on the topic {self.state.topic} using the following research:

                <research>
                {self.state.research}
                </research>
                """
            )

        else:
            # improve content
            llm_response = llm.call(  # type: ignore
                f"""
                You wrote this tweet on {self.state.topic}, but it does not have a good viral score because of {self.state.score.reason} 
                
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

        self.state.tweet = Tweet.model_validate_json(llm_response)

    @listen(or_(ContentCreateEvent.CREATE_BLOG, "reproduce_blog"))
    def handle_create_blog(self):
        llm = LLM(model="openai/o4-mini", response_format=BlogPost)

        if self.state.blog_post is None:
            # create content
            llm_response = llm.call(  # type: ignore
                f"""
                Make a blog post on the topic {self.state.topic} using the following research:

                <research>
                {self.state.research}
                </research>
                """
            )
        else:
            # improve content
            llm_response = llm.call(  # type: ignore
                f"""
                You wrote this blog post on {self.state.topic}, but it does not good SEO score because of {self.state.score.reason} 
                
                Improve it.

                <blog_post>
                {self.state.blog_post.model_dump_json()}
                </blog_post>

                Use the following research.

                <research>
                {self.state.research}
                </research>
                """
            )

        self.state.blog_post = BlogPost.model_validate_json(llm_response)

    @listen(or_(ContentCreateEvent.CREATE_LINKEDIN, "reproduce_linkedin"))
    def handle_create_linkedin(self):
        llm = LLM(model="openai/o4-mini", response_format=LinkedInPost)

        if self.state.linkedin_post is None:
            # create content
            llm_response = llm.call(  # type: ignore
                f"""
                Make a linkedin post on the topic {self.state.topic} using the following research:

                <research>
                {self.state.research}
                </research>
                """
            )

        else:
            # improve content
            llm_response = llm.call(  # type: ignore
                f"""
                You wrote this linkedin post on {self.state.topic}, but it does not have a good viral score because of {self.state.score.reason} 
                
                Improve it.

                <linkedin_post>
                {self.state.linkedin_post.model_dump_json()}
                </linkedin_post>

                Use the following research.

                <research>
                {self.state.research}
                </research>
                """
            )

        self.state.linkedin_post = LinkedInPost.model_validate_json(llm_response)

    @listen(handle_create_blog)
    def check_seo(self):
        eval_seo = (
            SeoCrew()
            .crew()
            .kickoff(
                inputs={
                    "topic": self.state.topic,
                    "blog_post": self.state.blog_post.model_dump_json(),  # type: ignore
                }
            )
        )

        self.state.score = eval_seo.pydantic  # type: ignore

    @listen(or_(handle_create_linkedin, handle_create_tweet))
    def check_viral(self):
        eval_viral = (
            ViralityCrew()
            .crew()
            .kickoff(
                inputs={
                    "topic": self.state.topic,
                    "content_type": self.state.content_type,
                    "content": self.state.tweet.model_dump_json()  # type: ignore
                    if self.state.content_type == ContentType.TWEET
                    else self.state.linkedin_post.model_dump_json(),  # type: ignore
                }
            )
        )

        self.state.score = eval_viral.pydantic  # type: ignore

    # refinement loop
    @router(or_(check_seo, check_viral))
    def content_quality_check(self):
        content_type = self.state.content_type
        score = self.state.score

        if score.score >= 6:
            print("Content quality is good, proceed finalization")
            return "finalize"
        else:
            print("Content quality is low, need to improve")
            if content_type == ContentType.TWEET:
                return "reproduce_tweet"
            elif content_type == ContentType.BLOG:
                return "reproduce_blog"
            elif content_type == ContentType.LINKEDIN:
                return "reproduce_linkedin"

    @listen("finalize")
    def finalize_content_creation(self):
        print("Finalizing content creation process")

        # Create timestamp for filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{self.state.content_type}_{timestamp}.txt"

        # Get the content based on content type
        content = ""
        if self.state.content_type == ContentType.TWEET and self.state.tweet:
            content = f"Content: {self.state.tweet.content}\nHashtags: {self.state.tweet.hashtags}"
        elif self.state.content_type == ContentType.BLOG and self.state.blog_post:
            content = (
                f"Title: {self.state.blog_post.title}\nSubtitle: {self.state.blog_post.subtitle}\nSections:\n"
                + "\n".join(f"- {section}" for section in self.state.blog_post.sections)
            )
        elif (
            self.state.content_type == ContentType.LINKEDIN and self.state.linkedin_post
        ):
            content = f"Hook: {self.state.linkedin_post.hook}\nContent: {self.state.linkedin_post.content}\nCall to Action: {self.state.linkedin_post.call_to_action}"

        # Add metadata
        file_content = f"""
            Topic: {self.state.topic}
            Content Type: {self.state.content_type}
            Quality Score: {self.state.score.score}/10
            Score Reason: {self.state.score.reason}
            Generated At: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

            {content}
            """

        # Save to file
        output_path = Path("output") / filename
        output_path.parent.mkdir(exist_ok=True)

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(file_content)

        print(f"Content saved to: {output_path}")


flow = ContentPipelineFlow().kickoff(
    inputs={
        "content_type": ContentType.TWEET,
        "topic": "Chainsaw Man: Reze Arc is fire",
    }
)

# flow.plot()
