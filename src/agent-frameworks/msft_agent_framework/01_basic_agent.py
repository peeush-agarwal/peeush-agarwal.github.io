import asyncio
from azure.identity.aio import AzureCliCredential
from agent_framework import ChatAgent
from agent_framework.azure import AzureAIAgentClient
from dotenv import load_dotenv


load_dotenv(override=True)


async def main():
    async with (
        AzureCliCredential() as credential,
        ChatAgent(
            chat_client=AzureAIAgentClient(async_credential=credential),
            instructions="You are good at telling jokes.",
        ) as agent,
    ):
        result = await agent.run("Tell me a joke about a pirate.")
        print(result.text)


asyncio.run(main())
