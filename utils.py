import os
import json
import inspect
import google.generativeai as genai
import yaml
from requirements import RequirementAnalyzer
from architecture import ArchitectureDesignAgent
from skeletons import CodeSkeletonGenerator
from dotenv import load_dotenv
from typing import Dict, List, Any, Optional
load_dotenv()

def save_to_file(agent_name: str, data: str):
    filename = f"{agent_name}.txt"
    
    # Delete the file if it exists
    if os.path.exists(filename):
        os.remove(filename)
    
    # Create a new file and write data
    with open(filename, "w") as f:
        f.write(data)
    
    print(f"Output saved to {filename}")

def save_to_json(agent_name: str, data: dict):
    filename = f"{agent_name}.json"
    if not os.path.exists(filename):
        with open(filename, "w") as f:
            json.dump(data, f, indent=2)
        print(f"Output saved to {filename}")
    else:
        print(f"{filename} already exists; skipping file save.")


# -------------------------------
# Helper: Load configuration from config.yaml
# -------------------------------
def load_config():
    config_file = "config2.yaml"
    if os.path.exists(config_file):
        with open(config_file, "r") as f:
            config = yaml.load(f, Loader=yaml.FullLoader)
        return config
    else:
        print("Config file config.yaml not found. Exiting.")
        exit(1)


# -------------------------------
# Main Execution and Agent Orchestration
# -------------------------------
def ensure_config():
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

def modify_requirements(requirement_output):
    """
    Display the extracted requirement tasks and allow the user to add additional tasks.
    The additional tasks are then appended to the 'tasks' list in the requirement output.
    """
    print("\nExtracted Requirement Tasks:")
    print(requirement_output)
    confirm = input("\nAre these requirements okay? (yes/no): ").strip().lower()
    if confirm == "yes":
        return requirement_output

    new_tasks_input = input("Enter additional tasks (comma-separated) to add: ").strip()
    if new_tasks_input:
        if "tasks" not in requirement_output or not isinstance(requirement_output["tasks"], list):
            requirement_output["tasks"] = []
        additional_tasks = [{"task": task.strip()} for task in new_tasks_input.split(",") if task.strip()]
        requirement_output["tasks"].extend(additional_tasks)
    return requirement_output

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
                modified_output = json.loads(modifications)
                return modified_output
            except json.JSONDecodeError:
                print("Invalid JSON format. Please try again.")
        else:
            print("Invalid input. Please enter 'yes', 'no', or 'modify'.")

def collect_requirement_outputs(req_analyzer: RequirementAnalyzer) -> Dict[str, Any]:
    """Collect and validate outputs from requirement analysis tasks."""
    outputs = {}
    
    # Collect and validate each task output
    tasks = [
        ("project_research", req_analyzer.project_research_task()),
        ("intent_analysis", req_analyzer.intent_analysis_task()),
        ("task_generation", req_analyzer.task_generation_task()),
        ("requirement_validation", req_analyzer.requirement_validation_task()),
        ("subtask_breakdown", req_analyzer.subtask_breakdown_task())
    ]
    
    for task_name, task in tasks:
        output = task.execute()
        validated_output = get_user_feedback(output, task_name)
        if validated_output is None:
            print(f"Task {task_name} failed validation. Stopping requirement analysis.")
            return None
        outputs[task_name] = validated_output
    
    return outputs

def requirements_crew(user_requirements: str, project_context: str) -> Optional[Dict[str, Any]]:
    """Run the requirements analysis crew with validation."""
    print("\n--- Running Requirement Analysis Agent ---")
    req_analyzer = RequirementAnalyzer(user_requirements=user_requirements, project_context=project_context)
    outputs = collect_requirement_outputs(req_analyzer)
    
    if outputs:
        # Save validated outputs
        for task_name, output in outputs.items():
            save_to_json(f"requirements_{task_name}", output)
        return outputs
    return None

def architecture_crew(requirement_output: Dict[str, Any], project_context: str, tech_stack: str) -> Optional[Dict[str, Any]]:
    """Run the architecture design crew with validation."""
    print("\n--- Running Architecture Design Agent ---")
    arch_agent = ArchitectureDesignAgent(
        requirement_analysis=requirement_output,
        project_context=project_context,
        tech_stack=tech_stack
    )
    outputs = collect_architecture_outputs(arch_agent)
    
    if outputs:
        # Save validated outputs
        for task_name, output in outputs.items():
            save_to_json(f"architecture_{task_name}", output)
        return outputs
    return None

def collect_architecture_outputs(arch_agent: ArchitectureDesignAgent) -> Dict[str, Any]:
    """Collect and validate outputs from architecture design tasks."""
    outputs = {}
    
    # Collect and validate each task output
    tasks = [
        ("system_research", arch_agent.system_research_task()),
        ("system_flowchart", arch_agent.system_flowchart_task()),
        ("component_diagram", arch_agent.component_diagram_task()),
        ("architecture_blueprint", arch_agent.architecture_blueprint_task()),
        ("architecture_validation", arch_agent.architecture_validation_task())
    ]
    
    for task_name, task in tasks:
        output = task.execute()
        validated_output = get_user_feedback(output, task_name)
        if validated_output is None:
            print(f"Task {task_name} failed validation. Stopping architecture design.")
            return None
        outputs[task_name] = validated_output
    
    return outputs

def skeletons_crew(architecture_output: Dict[str, Any], project_context: str) -> Optional[Dict[str, Any]]:
    """Run the code skeleton generation crew with validation."""
    print("\n--- Running Code Skeleton Generation Agent ---")
    skeleton_agent = CodeSkeletonGenerator(
        architecture_design=architecture_output,
        project_context=project_context
    )
    outputs = collect_skeleton_outputs(skeleton_agent)
    
    if outputs:
        # Save validated outputs
        for task_name, output in outputs.items():
            save_to_json(f"skeleton_{task_name}", output)
        return outputs
    return None

def collect_skeleton_outputs(skeleton_agent: CodeSkeletonGenerator) -> Dict[str, Any]:
    """Collect and validate outputs from code skeleton generation tasks."""
    outputs = {}
    
    # Collect and validate each task output
    tasks = [
        ("code_research", skeleton_agent.code_research_task()),
        ("code_skeleton", skeleton_agent.code_skeleton_task()),
        ("module_boilerplate", skeleton_agent.module_boilerplate_task()),
        ("testing_boilerplate", skeleton_agent.testing_boilerplate_task()),
        ("documentation", skeleton_agent.documentation_task())
    ]
    
    for task_name, task in tasks:
        output = task.execute()
        validated_output = get_user_feedback(output, task_name)
        if validated_output is None:
            print(f"Task {task_name} failed validation. Stopping code skeleton generation.")
            return None
        outputs[task_name] = validated_output
    
    return outputs
