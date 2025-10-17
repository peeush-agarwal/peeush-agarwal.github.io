import asyncio
from typing import Annotated
from dotenv import load_dotenv
from pydantic import Field

from azure.identity.aio import AzureCliCredential
from agent_framework.azure import AzureAIAgentClient
from agent_framework import ChatAgent


load_dotenv(override=True)


class WeatherTools:
    def __init__(self):
        self.last_location = None

    def get_weather(
        self,
        location: Annotated[
            str, Field(description="Location name to get the weather for")
        ],
    ) -> str:
        """Gets the weather for specified location."""
        return f"Weather for {location} is sunny and exciting."

    def get_weather_details(self) -> str:
        """Gets the Weather details for last location"""
        if self.last_location:
            return f"The weather details for {self.last_location} are max of 25, min of 15, humidity is 30 and feels like exciting."
        return "No location specified yet."


async def main():
    weather_tools = WeatherTools()
    async with (
        AzureCliCredential() as credential,
        ChatAgent(
            chat_client=AzureAIAgentClient(async_credential=credential),
            name="Function Agent",
            instructions="You are a helpful assistant",
            tools=[weather_tools.get_weather, weather_tools.get_weather_details],
        ) as agent,
    ):
        result = await agent.run("What's the weather like in Tampa?")
        print(result.text)


asyncio.run(main())
