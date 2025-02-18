import asyncio
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.base import TaskResult
from autogen_agentchat.conditions import ExternalTermination, TextMentionTermination
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.ui import Console
from autogen_ext.models.openai import AzureOpenAIChatCompletionClient
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from dotenv import load_dotenv
import os


load_dotenv()


## Create the token provider
token_provider = get_bearer_token_provider(
    DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default"
)

API_KEY = os.getenv("api-key")
Model_Name = os.getenv("model-name")
API_Version = os.getenv("api-version")
Azure_Endpoint = os.getenv("azure-endpoint")



az_model_client = AzureOpenAIChatCompletionClient(
    azure_deployment=Model_Name,
    model=Model_Name,
    api_version=API_Version,
    azure_endpoint=Azure_Endpoint,
    api_key=API_KEY
)
# Test the model


# Create the primary agent
Story_Writer = AssistantAgent(
    name="Story_Writer",
    model_client=az_model_client,
    system_message = "You are a helpful AI assitant which write the story for kids. Keep the story short and interesting.",
    
)

## Create the Reviewer Agent
Story_reviewer = AssistantAgent(
    name="Story_Reviewer",
    model_client=az_model_client,
    system_message = "You are a helpful AI assitant which provides constructive feedbacks on kids stories to add a positive impactfull ending. When all the feedback are addressed , you can respond with APPROVE.",
    #system_message="You are a helpful assistant that can take in all of the suggestions and advice from the other agents and provide a detailed final travel plan. You must ensure that the final plan is integrated and complete. YOUR FINAL RESPONSE MUST BE THE COMPLETE PLAN. When the plan is complete and all perspectives are integrated, you can respond with TERMINATE.",
)






# Define the termination conditions that stops task of review
termination = TextMentionTermination("APPROVE")
team = RoundRobinGroupChat(
    [Story_Writer, Story_reviewer], termination_condition=termination
)

config = team.dump_component()
print(config.model_dump_json())

# Define the main asynchronous function
#async def main():
#    await Console(team.run_stream(task="write a story on elephent"))

# Run the main function
#if __name__ == "__main__":
#    asyncio.run(main())