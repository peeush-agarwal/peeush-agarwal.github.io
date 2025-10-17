import asyncio
from pydantic import BaseModel
from typing import Annotated
from pydantic import Field
from agent_framework import (
    AgentRunResponse,
    HostedCodeInterpreterTool,
    TextContent,
    TextReasoningContent,
    DataContent,
    UriContent,
)
from agent_framework.openai import OpenAIResponsesClient
from dotenv import load_dotenv


async def basic_example():
    # Create an agent using OpenAI Responses
    agent = OpenAIResponsesClient().create_agent(
        name="WeatherBot",
        instructions="You are a helpful weather assistant.",
    )

    result = await agent.run("What's a good way to check the weather?")
    print(result.text)


async def streaming_example():
    agent = OpenAIResponsesClient().create_agent(
        instructions="You are a creative storyteller.",
    )

    print("Assistant: ", end="", flush=True)
    async for chunk in agent.run_stream("Tell me a short story about AI."):
        if chunk.text:
            print(chunk.text, end="", flush=True)
    print()  # New line after streaming


async def reasoning_example():
    agent = OpenAIResponsesClient(ai_model_id="gpt-5").create_agent(
        name="MathTutor",
        instructions="You are a personal math tutor. When asked a math question, "
        "write and run code to answer the question.",
        tools=HostedCodeInterpreterTool(),
        reasoning={"effort": "high", "summary": "detailed"},
    )

    print("Assistant: ", end="", flush=True)
    async for chunk in agent.run_stream("Solve: 3x + 11 = 14"):
        if chunk.contents:
            for content in chunk.contents:
                if isinstance(content, TextReasoningContent):
                    # Reasoning content in gray text
                    print(f"\033[97m{content.text}\033[0m", end="", flush=True)
                elif isinstance(content, TextContent):
                    print(content.text, end="", flush=True)
    print()


class CityInfo(BaseModel):
    """A structured output for city information."""

    city: str
    description: str


async def structured_output_example():
    agent = OpenAIResponsesClient().create_agent(
        name="CityExpert",
        instructions="You describe cities in a structured format.",
    )

    # Non-streaming structured output
    result = await agent.run("Tell me about Paris, France", response_format=CityInfo)

    if result.value:
        city_data = result.value
        print(f"City: {city_data.city}")
        print(f"Description: {city_data.description}")

    # Streaming structured output
    structured_result = await AgentRunResponse.from_agent_response_generator(
        agent.run_stream("Tell me about Tokyo, Japan", response_format=CityInfo),
        output_format_type=CityInfo,
    )

    if structured_result.value:
        tokyo_data = structured_result.value
        print(f"City: {tokyo_data.city}")
        print(f"Description: {tokyo_data.description}")


def get_weather(
    location: Annotated[str, Field(description="The location to get weather for")],
) -> str:
    """Get the weather for a given location."""
    # Your weather API implementation here
    return f"The weather in {location} is sunny with 25°C."


async def tools_example():
    agent = OpenAIResponsesClient().create_agent(
        instructions="You are a helpful weather assistant.",
        tools=get_weather,
    )

    result = await agent.run("What's the weather like in Tokyo?")
    print(result.text)


async def image_generation_example():
    agent = OpenAIResponsesClient().create_agent(
        instructions="You are a helpful AI that can generate images.",
        tools=[
            {
                "type": "image_generation",
                "size": "1024x1024",
                "quality": "low",
            }
        ],
    )

    result = await agent.run("Generate an image of a sunset over the ocean.")

    # Check for generated images in the response
    for content in result.contents:
        if isinstance(content, (DataContent, UriContent)):
            print(f"Image generated: {content.uri}")


async def code_interpreter_example():
    agent = OpenAIResponsesClient().create_agent(
        instructions="You are a helpful assistant that can write and execute Python code.",
        tools=HostedCodeInterpreterTool(),
    )

    result = await agent.run("Calculate the factorial of 100 using Python code.")
    print(result.text)


async def main():
    load_dotenv(override=True)

    await basic_example()
    await streaming_example()
    await reasoning_example()
    await structured_output_example()
    await tools_example()
    await code_interpreter_example()
    # await image_generation_example()


if __name__ == "__main__":
    asyncio.run(main())
