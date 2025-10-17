import asyncio
from agent_framework import ChatAgent
from agent_framework.azure import AzureAIAgentClient
from azure.identity.aio import AzureCliCredential
from agent_framework import ChatMessage, TextContent, UriContent, Role
from dotenv import load_dotenv


load_dotenv(override=True)


async def main():
    async with (
        AzureCliCredential() as credential,
        ChatAgent(
            chat_client=AzureAIAgentClient(async_credential=credential),
            instructions="You are a helpful assistant and can analyze images",
        ) as agent,
    ):
        # message = ChatMessage(
        #     role=Role.USER,
        #     contents=[
        #         TextContent(text="Tell me a joke about this image?"),
        #         UriContent(
        #             uri="https://samplesite.org/clown.jpg", media_type="image/jpeg"
        #         ),
        #     ],
        # )
        message = ChatMessage(
            role=Role.USER,
            contents=[
                TextContent(text="Tell me a joke about pirate"),
            ],
        )

        result = await agent.run(message)
        print(result.text)


asyncio.run(main())
