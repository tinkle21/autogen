# Autogen Learning

## Installation

```bash
# Clone the repository
git clone https://github.com/tinkle21/autogen.git

# Navigate into the project directory
cd autogen

# Create a Virtual Environment
python -m venv autogen-venv

# Activate the newly created environment
source autogen-venv/bin/activate
```

## Install Required Dependencies

```bash
pip install -r requirements.txt
```

## Update `.env` File
Ensure that the `.env` file is updated with the necessary credentials for Azure OpenAI, using the `gpt-4o` model and API key.

## Applications

### Kids Story Generation with Story Writer & Story Reviewer Agents
This application uses `RoundRobinChat` to iteratively review and refine a story until the Reviewer approves it.

```bash
python teams.py
```

### Kids Story Generation with Planner, Story Writer, Moral Writer & Reviewer Agents
This application uses `SelectorGroupChat` to plan, review, provide a moral ending, and refine the story until the Reviewer approves it or a maximum of 10 turns is reached.

```bash
python selector.py
```

### Travel Agent Application
This application utilizes `RoundRobinChat` to coordinate between `planner_agent`, `local_agent`, `language_agent`, and `travel_summary_agent` until `TERMINATE` is passed by `planner_agent`.

```bash
python travel_agents.py
```

### Company Research Application with Custom Tools
This application creates custom tools (`googlesearch` and `stock_analysis`) and utilizes agents (`stock_analysis_agent`, `search_agent`, `report_agent`) to analyze a company's stock.

```bash
python company_research.py
```

## Start Autogen Studio
Using Autogen Studio, either we can build similar agentic application through UI from scratch or see above built application in UI mode by exporting above application code as json dump(as below). This command will start autogen studio in your local host and save your studio working in provided app directory.
```bash
autogenstudio ui --port 8081 --appdir ./<new_dir_name>
```

## Generate JSON for Autogen Studio UI Teams from Python Script
This script generates JSON that can be copied and pasted into any new Teams UI configuration.

```python
config = team.dump_component()
print(config.model_dump_json())
