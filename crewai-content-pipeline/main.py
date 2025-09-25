from enum import Enum, StrEnum
from typing import Annotated, ClassVar

from crewai.flow.flow import Flow, listen, or_, router, start
from pydantic import BaseModel, Field


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
        print(f"Conducting research on topic: {self.state.topic}")
        return True

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

    @listen(ContentCreateEvent.CREATE_TWEET)
    def handle_create_tweet(self):
        print("Handling event: create_tweet")

    @listen(ContentCreateEvent.CREATE_BLOG)
    def handle_create_blog(self):
        print("Handling event: create_blog")

    @listen(ContentCreateEvent.CREATE_LINKEDIN)
    def handle_create_linkedin(self):
        print("Handling event: create_linkedin")

    @listen(handle_create_blog)
    def check_seo(self):
        print("Performing SEO check for blog content")

    @listen(or_(handle_create_linkedin, handle_create_tweet))
    def check_viral(self):
        print("Performing viral content check for tweet or linkedin content")

    @listen(or_(check_seo, check_viral))
    def finalize_content_creation(self):
        print("Finalizing content creation process")


flow = ContentPipelineFlow()

flow.plot()
