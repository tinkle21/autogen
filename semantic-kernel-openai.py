import os

from autogen_core.models import UserMessage
from autogen_ext.models.semantic_kernel import SKChatCompletionAdapter
from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.openai import OpenAIChatCompletionClient, OpenAIChatPromptExecutionSettings
from semantic_kernel.connectors.ai.anthropic import AnthropicChatCompletion, AnthropicChatPromptExecutionSettings
from semantic_kernel.memory.null_memory import NullMemory
import asyncio

sk_client = OpenAIChatCompletionClient(
    ai_model_id="gpt-4o-2024-08-06",
    api_key=os.environ["OPEN_API_KEY"],
    service_id="my-service-id",  # Optional; for targeting specific services within Semantic Kernel
)
settings = OpenAIChatPromptExecutionSettings(
    temperature=0.2,
)

openai_model_client = SKChatCompletionAdapter(
    sk_client, kernel=Kernel(memory=NullMemory()), prompt_settings=settings
)

async def main():
    # Call the model directly.
    model_result = await openai_model_client.create(
    messages=[UserMessage(content="What is the capital of France?", source="User")])
    print(model_result)

asyncio.run(main())