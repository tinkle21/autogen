import asyncio
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.base import TaskResult
from autogen_agentchat.conditions import ExternalTermination, TextMentionTermination,MaxMessageTermination
from autogen_agentchat.teams import RoundRobinGroupChat, SelectorGroupChat
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

# Create the planning agent for sotry writing

planning_agent = AssistantAgent(
    "planning_agent",
    model_client=az_model_client,
    description="An agent for planning tasks, this agent should be first to enage when given anew task",
    system_message="""
    You are a planning agent.
    Your Job is to breakdown complex tasks into smaller, manageable substasks.
    Your team members are:
    - Story_Writer:Write story and make corrections.
    - Story_Reviewer: Check if story is for kids and provide constructive feedback to add a positive impactfull ending.
    - Story_moral: Finally, adds a moral to the story.

    You only plan and delegate tasks to your team members.
    You do not execute them yourself.
    You can enage with your team members to get updates on the progress of the task.

    When assigning a task, you can use the following format:
    1. <agent> : <task>

    After all tasks are complete, summarize the findings and end with TERMINATE.
    """
)


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

## Create the Story Moral Agent
Story_moral = AssistantAgent(
    name="Story_Moral",
    model_client=az_model_client,
    system_message = "You are a helpful AI assitant which add the moral of story at the end. Keep the moral positive and impactful.",
)

# Define the termination conditions that stops task of review
text_termination = TextMentionTermination("TERMINATE")
max_message_termination = MaxMessageTermination(max_messages=10)
termination = text_termination | max_message_termination
team = SelectorGroupChat(
    [planning_agent,Story_Writer, Story_reviewer, Story_moral], 
    model_client = az_model_client,
    termination_condition=termination
)

# Define the main asynchronous function
async def main():
    await Console(team.run_stream(task="write a story on rocket crash"))

# Run the main function
if __name__ == "__main__":
    asyncio.run(main())