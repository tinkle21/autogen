import asyncio
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.base import TaskResult
from autogen_agentchat.conditions import ExternalTermination, TextMentionTermination
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.ui import Console
from autogen_ext.models.openai import AzureOpenAIChatCompletionClient
from autogen_core.tools import FunctionTool
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from dotenv import load_dotenv
import os
from google_search import google_search, analyze_stock

load_dotenv()


## Create the token provider
token_provider = get_bearer_token_provider(
    DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default"
)

API_KEY = os.getenv("api-key")
Model_Name = os.getenv("model-name")
API_Version = os.getenv("api-version")
Azure_Endpoint = os.getenv("azure-endpoint")

# Define a simple function tool that the agent can use.
google_search_tool = FunctionTool(
    google_search, description="Search Google for information, returns results with a snippet and body content"
)
stock_analysis_tool = FunctionTool(analyze_stock, description="Analyze stock data and generate a plot")

az_model_client = AzureOpenAIChatCompletionClient(
    azure_deployment=Model_Name,
    model=Model_Name,
    api_version=API_Version,
    azure_endpoint=Azure_Endpoint,
    api_key=API_KEY
)


# Define agents 
search_agent = AssistantAgent(
    name="Google_Search_Agent",
    model_client=az_model_client,
    tools=[google_search_tool],
    description="Search Google for information, returns top 2 results with a snippet and body content",
    system_message="You are a helpful AI assistant. Solve tasks using your tools.",
)

stock_analysis_agent = AssistantAgent(
    name="Stock_Analysis_Agent",
    model_client=az_model_client,
    tools=[stock_analysis_tool],
    description="Analyze stock data and generate a plot",
    system_message="Perform data analysis.",
)

report_agent = AssistantAgent(
    name="Report_Agent",
    model_client=az_model_client,
    description="Generate a report based the search and results of stock analysis",
    system_message="You are a helpful assistant that can generate a comprehensive report on a given topic based on search and stock analysis. When you done with generating the report, reply with TERMINATE.",
)

team = RoundRobinGroupChat([stock_analysis_agent, search_agent, report_agent], max_turns=3)

async def main() -> None:
    stream = team.run_stream(task="Write a financial report on American airlines")
    await Console(stream)



if __name__ == "__main__":
    asyncio.run(main())

