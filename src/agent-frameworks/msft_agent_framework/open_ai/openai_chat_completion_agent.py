import asyncio
from typing import Annotated
from agent_framework import ChatAgent
from pydantic import Field
from dotenv import load_dotenv

from agent_framework.openai import OpenAIChatClient


async def basic_example():
    # Create an agent using OpenAI ChatCompletion
    agent = OpenAIChatClient().create_agent(
        name="HelpfulAssistant",
        instructions="You are a helpful assistant.",
    )

    result = await agent.run("Hello, how can you help me?")
    print(result.text)


def get_weather(
    location: Annotated[str, Field(description="The location to get weather for")],
) -> str:
    """Get the weather for a given location."""
    # Your weather API implementation here
    return f"The weather in {location} is sunny with 25°C."


async def tools_example():
    agent = ChatAgent(
        chat_client=OpenAIChatClient(),
        instructions="You are a helpful weather assistant.",
        tools=get_weather,  # Add tools to the agent
    )

    result = await agent.run("What's the weather like in Tokyo?")
    print(result.text)


async def streaming_example():
    agent = OpenAIChatClient().create_agent(
        name="StoryTeller",
        instructions="You are a creative storyteller.",
    )

    print("Assistant: ", end="", flush=True)
    async for chunk in agent.run_stream("Tell me a short story about AI."):
        if chunk.text:
            print(chunk.text, end="", flush=True)
    print()  # New line after streaming


async def main():
    load_dotenv(override=True)

    await basic_example()
    await streaming_example()
    await tools_example()


if __name__ == "__main__":
    asyncio.run(main())
