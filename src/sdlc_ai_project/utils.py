import os
import json
import yaml
from typing import Dict, Any, Optional
from sdlc_ai_project.agents.requirements import RequirementAnalyzer
from dotenv import load_dotenv

load_dotenv()

# -------------------------------
# File Utilities
# -------------------------------
def save_to_file(agent_name: str, data: str):
    """Save data to a text file."""
    filename = f"{agent_name}.txt"
    if os.path.exists(filename):
        os.remove(filename)
    with open(filename, "w") as f:
        f.write(data)
    print(f"Output saved to {filename}")


def save_to_json(agent_name: str, data: dict):
    """Save data to a JSON file."""
    filename = f"{agent_name}.json"
    with open(filename, "w") as f:
        json.dump(data, f, indent=2)
    print(f"Output saved to {filename}")


# -------------------------------
# Configuration Utilities
# -------------------------------
def load_config(config_file: str = "config.yaml") -> Dict[str, Any]:
    """Load configuration from a YAML file."""
    if os.path.exists(config_file):
        with open(config_file, "r") as f:
            return yaml.load(f, Loader=yaml.FullLoader)
    else:
        print(f"Config file {config_file} not found.")
        return {}


def ensure_config():
    """Ensure configuration files exist."""
    config_dir = os.path.join(os.getcwd(), "config")
    agents_config = os.path.join(config_dir, "agents.yaml")
    tasks_config = os.path.join(config_dir, "tasks.yaml")
    if not os.path.exists(config_dir):
        os.makedirs(config_dir)
    if not os.path.exists(agents_config):
        with open(agents_config, "w") as f:
            f.write("agents: {}\n")
    if not os.path.exists(tasks_config):
        with open(tasks_config, "w") as f:
            f.write("tasks: {}\n")


# -------------------------------
# Agent Interaction Utilities
# -------------------------------
def get_user_feedback(output: Any, task_name: str) -> Dict[str, Any]:
    """Get user feedback for a task's output and return modified output if needed."""
    print(f"\n=== {task_name} Output Review ===")
    print(json.dumps(output, indent=2))
    
    while True:
        feedback = input("\nIs this output acceptable? (yes/no/modify): ").strip().lower()
        if feedback == "yes":
            return output
        elif feedback == "no":
            return None
        elif feedback == "modify":
            try:
                modifications = input("Enter modifications (as JSON): ").strip()
                return json.loads(modifications)
            except json.JSONDecodeError:
                print("Invalid JSON format. Please try again.")
        else:
            print("Invalid input. Please enter 'yes', 'no', or 'modify'.")


def collect_task_outputs(agent) -> Dict[str, Any]:
    """Collect and validate outputs from agent tasks."""

    agent_crew = agent.crew()
    agent_crew.kickoff()  # Start the agent's crew
    # agent.crew().kickoff()
    print("\n--- Collecting Task Outputs ---")  

    outputs = {}
    for task in agent.crew().tasks:
        task_name = task.name
        output = task.output.raw
        validated_output = get_user_feedback(output, task_name)
        if validated_output is None:
            print(f"Task {task_name} failed validation. Stopping execution.")
            return None
        outputs[task_name] = validated_output
    return outputs


# -------------------------------
# Requirement Analysis Workflow
# -------------------------------
# def requirements_crew(user_requirements: str, project_context: str) -> Optional[Dict[str, Any]]:
#     """Run the requirements analysis crew with validation."""
#     print("\n--- Running Requirement Analysis Agent ---")
#     req_analyzer = RequirementAnalyzer(user_requirements=user_requirements, project_context=project_context)
    
#     tasks = [
#         ("project_research", req_analyzer.project_research_task()),
#         ("intent_analysis", req_analyzer.intent_analysis_task()),
#         ("task_generation", req_analyzer.task_generation_task()),
#         ("requirement_validation", req_analyzer.requirement_validation_task()),
#         ("subtask_breakdown", req_analyzer.subtask_breakdown_task())
#     ]
    
#     outputs = {}
#     if outputs:
#         for task_name, output in outputs.items():
#             save_to_json(f"requirements_{task_name}", output)
#         return outputs
#     return None

def load_agents(user_requirements: str, project_context: str, llm) -> Optional[Dict[str, Any]]:
    req_analyzer = RequirementAnalyzer(user_requirements=user_requirements, project_context=project_context, llm=llm)
    req_analyzer_outputs = collect_task_outputs(req_analyzer)
    return req_analyzer_outputs