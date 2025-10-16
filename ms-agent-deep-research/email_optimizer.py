"""
Email Optimizer with MS Agent Framework

This script demonstrates a multi-agent workflow for optimizing emails using Microsoft Agent Framework.
It features five specialized agents that collaborate sequentially to improve email quality:
- ClarityAgent: Focuses on clarity and simplicity
- ToneAgent: Adjusts emotional tone and professionalism
- PersuasionAgent: Enhances persuasive power
- SynthesizerAgent: Integrates all improvements into a unified draft
- CriticAgent: Performs final quality review and approval

**Explanation:**
This migration from AutoGen to MS Agent Framework demonstrates several key concepts:

1. **SequentialBuilder** replaces `RoundRobinGroupChat` for sequential agent orchestration
2. **ChatAgent** replaces `AssistantAgent` with `chat_client` instead of `model_client`
3. **OpenAIChatClient** replaces `OpenAIChatCompletionClient`
4. **AgentMiddleware** implements termination conditions (TERMINATE keyword and max messages)
5. **WorkflowOutputEvent** handles streaming workflow results
6. Agent `instructions` parameter replaces `system_message`
"""

import asyncio
import os

from agent_framework import (
    AgentMiddleware,
    AgentRunContext,
    ChatAgent,
    ChatMessage,
    Role,
    SequentialBuilder,
    WorkflowOutputEvent,
)
from agent_framework.openai import OpenAIChatClient
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class TerminationMiddleware(AgentMiddleware):
    """
    Middleware that checks for termination conditions.

    **Explanation:**
    This middleware replaces AutoGen's `TextMentionTermination` and `MaxMessageTermination`.
    It monitors both message count limits and the presence of "TERMINATE" keyword in responses.
    MS Agent Framework uses middleware pattern for cross-cutting concerns like termination.
    """

    def __init__(self, max_messages: int = 30):
        self.max_messages = max_messages
        self.message_count = 0

    async def process(self, context: AgentRunContext, next) -> None:
        """Process middleware logic before and after agent execution."""
        # Increment message counter
        self.message_count += 1

        # Check max messages limit
        if self.message_count >= self.max_messages:
            print(
                f"\n[Termination] Maximum message limit ({self.max_messages}) reached."
            )
            context.terminate = True
            return

        # Continue processing
        await next(context)

        # Check for TERMINATE keyword in response
        if context.result:
            response_text = str(context.result)
            if "TERMINATE" in response_text:
                print("\n[Termination] TERMINATE keyword detected.")
                context.terminate = True
                return


async def run_email_optimizer(email_draft: str) -> list[ChatMessage]:
    """
    Run the email optimization workflow.

    **Explanation:**
    This function orchestrates the multi-agent workflow using MS Agent Framework's SequentialBuilder.
    Unlike AutoGen's RoundRobinGroupChat which runs agents in a loop, SequentialBuilder passes
    conversation context through agents in a single pass, with agents appending their responses
    to the shared conversation history.

    Args:
        email_draft: The initial email text to optimize

    Returns:
        list[ChatMessage]: Complete conversation history including all agent interactions
    """
    # Initialize OpenAI chat client
    # Explanation: OpenAIChatClient replaces AutoGen's OpenAIChatCompletionClient
    # Note: Use model_id parameter instead of model
    chat_client = OpenAIChatClient(
        model_id="gpt-4o-mini",
        api_key=os.getenv("OPENAI_API_KEY"),
    )

    # Create shared termination middleware instance
    # Explanation: All agents share the same middleware instance to track total message count
    termination_middleware = TerminationMiddleware(max_messages=30)

    # Define specialized agents with MS Agent Framework
    # Explanation: ChatAgent is the primary agent class in MS Agent Framework.
    # Key differences from AutoGen's AssistantAgent:
    # - Uses `chat_client` parameter instead of `model_client`
    # - Uses `instructions` instead of `system_message`
    # - Middleware is passed as a list for composability

    clarity_agent = ChatAgent(
        name="ClarityAgent",
        chat_client=chat_client,
        instructions="""
        You are an expert editor focused on clarity and simplicity.
        Your job is to eliminate ambiguity, redundancy, and make every sentence crisp and clear.
        Don't worry about persuasion or tone — just make the message easy to read and understand.
        Provide your improved version of the email.
        """,
        middleware=[termination_middleware],
    )

    tone_agent = ChatAgent(
        name="ToneAgent",
        chat_client=chat_client,
        instructions="""
        You are a communication coach focused on emotional tone and professionalism.
        Your job is to make the email sound warm, confident, and human — while staying professional
        and appropriate for the audience. Improve the emotional resonance, polish the phrasing,
        and adjust any words that may come off as stiff, cold, or overly casual.
        Provide your improved version of the email.
        """,
        middleware=[termination_middleware],
    )

    persuasion_agent = ChatAgent(
        name="PersuasionAgent",
        chat_client=chat_client,
        instructions="""
        You are a persuasion expert trained in marketing, behavioral psychology,
        and copywriting. Your job is to enhance the email's persuasive power: improve call to action,
        structure arguments, and emphasize benefits. Remove weak or passive language.
        Provide your improved version of the email.
        """,
        middleware=[termination_middleware],
    )

    synthesizer_agent = ChatAgent(
        name="SynthesizerAgent",
        chat_client=chat_client,
        instructions="""
        You are an advanced email-writing specialist. Your role is to read all
        prior agent responses and revisions, and then synthesize the best ideas into a unified,
        polished draft of the email. Focus on: Integrating clarity, tone, and persuasion improvements;
        Ensuring coherence, fluency, and a natural voice; Creating a version that feels professional,
        effective, and readable.
        Provide the final synthesized email draft.
        """,
        middleware=[termination_middleware],
    )

    critic_agent = ChatAgent(
        name="CriticAgent",
        chat_client=chat_client,
        instructions="""
        You are an email quality evaluator. Your job is to perform a final review
        of the synthesized email and determine if it meets professional standards. Review the email for:
        Clarity and flow, appropriate professional tone, effective call-to-action, and overall coherence.
        Be constructive but decisive. If the email has major flaws (unclear message, unprofessional tone,
        or missing key elements), provide ONE specific improvement suggestion. If the email meets professional
        standards and communicates effectively, respond with 'The email meets professional standards.' followed
        by `TERMINATE` on a new line. You should only approve emails that are perfect enough for professional use,
        don't settle.
        """,
        middleware=[termination_middleware],
    )

    # Build the sequential workflow
    # Explanation: SequentialBuilder creates a workflow where agents process messages sequentially,
    # each appending their response to a shared conversation context (list[ChatMessage]).
    # This replaces AutoGen's RoundRobinGroupChat pattern.
    workflow = (
        SequentialBuilder()
        .participants(
            [
                clarity_agent,
                tone_agent,
                persuasion_agent,
                synthesizer_agent,
                critic_agent,
            ]
        )
        .build()
    )

    print("=" * 80)
    print("EMAIL OPTIMIZATION WORKFLOW")
    print("=" * 80)
    print(f"\nOriginal Email:\n{email_draft}\n")
    print("=" * 80)
    print("Starting agent collaboration...\n")

    conversation_history: list[ChatMessage] = []

    # Run workflow with streaming
    # Explanation: workflow.run_stream() returns an async generator of workflow events.
    # WorkflowOutputEvent contains the final conversation history when workflow completes.
    # This replaces AutoGen's Console(team.run_stream()) pattern.
    async for event in workflow.run_stream(email_draft):
        if isinstance(event, WorkflowOutputEvent):
            # Workflow completed - get final conversation
            conversation_history = event.data if event.data else []
            print("\n" + "=" * 80)
            print("WORKFLOW COMPLETED")
            print("=" * 80)

            # Display full conversation
            print("\nFull Conversation History:")
            print("-" * 80)
            if conversation_history:
                for msg in conversation_history:
                    role = msg.role if hasattr(msg, "role") else "unknown"
                    author = msg.author_name if hasattr(msg, "author_name") else role
                    content = ""
                    if hasattr(msg, "text"):
                        content = msg.text
                    elif hasattr(msg, "contents") and msg.contents:
                        content = " ".join(
                            str(c) for c in msg.contents if hasattr(c, "text")
                        )

                    print(f"\n[{author}]:")
                    print(content)
                    print("-" * 80)

            # Extract final optimized email (from SynthesizerAgent, second-to-last assistant)
            # The last assistant message is from CriticAgent with approval/feedback
            final_email = None
            assistant_messages = []
            if conversation_history:
                for msg in conversation_history:
                    if hasattr(msg, "role") and msg.role == Role.ASSISTANT:
                        if (
                            hasattr(msg, "author_name")
                            and msg.author_name == "SynthesizerAgent"
                        ):
                            if hasattr(msg, "text"):
                                final_email = msg.text
                            break
                        assistant_messages.append(msg)

                # Fallback: if SynthesizerAgent not found by name, get second-to-last assistant
                if not final_email and len(assistant_messages) >= 2:
                    if hasattr(assistant_messages[-2], "text"):
                        final_email = assistant_messages[-2].text

            if final_email:
                print("\n" + "=" * 80)
                print("FINAL OPTIMIZED EMAIL")
                print("=" * 80)
                print(final_email)
                print("=" * 80)

    return conversation_history


async def main():
    """Main entry point for the email optimizer."""
    # Example email to optimize
    test_email = "Thank you for your help! without your help our business collapse, I'll buy lunch later"

    # Run the workflow
    await run_email_optimizer(test_email)


if __name__ == "__main__":
    asyncio.run(main())
