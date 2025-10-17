import asyncio
from dotenv import load_dotenv
from azure.identity.aio import AzureCliCredential
from agent_framework import ChatAgent
from agent_framework.azure import AzureAIAgentClient


load_dotenv(override=True)


async def main():
    async with (
        AzureCliCredential() as credential,
        ChatAgent(
            chat_client=AzureAIAgentClient(async_credential=credential),
            name="StateAgent",
            instructions="You are a helpful assistant that can tell jokes.",
        ) as agent,
    ):
        thread1 = agent.get_new_thread()
        thread2 = agent.get_new_thread()

        result = await agent.run("Tell me a joke about a pirate", thread=thread1)
        print(result.text)

        result = await agent.run("Tell me a joke about a robot", thread=thread2)
        print(result.text)

        result = await agent.run(
            "Now add lots of emojis and rewrite the joke", thread=thread1
        )
        print(result.text)

        result = await agent.run(
            "Now add lots of emojis and rewrite the joke", thread=thread2
        )
        print(result.text)


asyncio.run(main())
