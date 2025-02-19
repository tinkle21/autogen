# Autogen Learning

## Installation
```bash
# Clone the repository
git clone https://github.com/tinkle21/autogen.git

# Navigate into the project directory
cd autogen

## Create a Virtual Enviornment
python -m venv autogen-venv

## Activate Newly created enviornment
source autogen-venv/bin/activate
![alt text](image.png)

## Install required depedency
pip install -r requirements.txt

## Update .env file
All application using Azure OpenAI endpoint, gpt-4o model and Key. update .env file accoridngly.

## Application to generate Kids story using Story writer and Story Reviewer agent.
This uses roundrobinchat to review and re-write story until "APPROVE" is not passed by Reviewer
```bash
python teams.py

## Application to generate Kids story using Planner,Story writer,Story Moral writer and Story Reviewer agent.
This uses Selectorgroupchat to plan,review,provide moral ending and re-write story until "APPROVE" is not passed by Reviewer or Max turn reached to 10
```bash
python selector.py

## Travel agnet Application .
This uses roundrobinchat to planner_agent, local_agent, language_agent, travel_summary_agent until "TERMINATE" is not passed by planner_agent 
```bash
python travel_agents.py

## company research Application by creating new tools.
This application create tools googlesearch, and tock analysis and use it by agents stock_analysis_agent, search_agent, report_agent to analysis stock of a company.
```bash
python company_research.py

## Start a autogen studio .
autogenstudio ui --port 8081 --appdir ./<new_dir_name> 

## code to generate json for autogenstudio UI teams from python script.Used in teams.py
This dump can pe copy paste in any new teams UI<-->JSON
```bash
config = team.dump_component()
print(config.model_dump_json())


