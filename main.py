#TODO: indivual task content flow
#TODO

import os
import yaml
import json
from typing import Optional, Dict, Any
from utils import (
    requirements_crew,
    architecture_crew,
    skeletons_crew,
    save_to_file,
    save_to_json,
    ensure_config,
    load_config,
    get_user_feedback
)
from dotenv import load_dotenv
load_dotenv()

def load_project_config() -> Dict[str, Any]:
    """Load and validate project configuration."""
    config = load_config()
    required_fields = ["domain", "objective", "tech_stack"]
    
    for field in required_fields:
        if field not in config:
            raise ValueError(f"Missing required field in config: {field}")
    
    return {
        "domain": config["domain"].strip(),
        "objective": config["objective"].strip(),
        "tech_stack": config["tech_stack"].strip(),
        "agents": config.get("agents", "1,2,3").strip()  # Default to all agents if not specified
    }

def validate_agent_selection(agent_choices: str) -> set:
    """Validate and process agent selection."""
    valid_choices = {"1", "2", "3"}
    selected_agents = set(choice.strip() for choice in agent_choices.split(",") if choice.strip())
    
    if not selected_agents:
        raise ValueError("No agents selected")
    
    invalid_choices = selected_agents - valid_choices
    if invalid_choices:
        raise ValueError(f"Invalid agent choices: {invalid_choices}")
    
    return selected_agents

def build_project_context(domain: str, tech_stack: str) -> str:
    """Build project context string from domain and tech stack."""
    context_parts = []
    if domain:
        context_parts.append(f"Domain: {domain}")
    if tech_stack:
        context_parts.append(f"Preferred Tech Stack: {tech_stack}")
    return " | ".join(context_parts) if context_parts else "General"

def main():
    try:
        # Initialize configuration
        ensure_config()
        config = load_project_config()
        selected_agents = validate_agent_selection(config["agents"])
        
        # Build project context
        project_context = build_project_context(config["domain"], config["tech_stack"])
        
        # Track outputs for validation
        requirement_outputs: Optional[Dict[str, Any]] = None
        architecture_outputs: Optional[Dict[str, Any]] = None
        skeleton_outputs: Optional[Dict[str, Any]] = None
        
        # --- Step 1: Requirement Analysis ---
        if "1" in selected_agents:
            print("\n=== Starting Requirement Analysis ===")
            requirement_outputs = requirements_crew(
                user_requirements=config["objective"],
                project_context=project_context
            )
            
            if requirement_outputs is None:
                print("Requirement analysis failed. Stopping workflow.")
                return
                
            # Save requirement outputs
            for task_name, output in requirement_outputs.items():
                save_to_json(f"requirements_{task_name}", output)
        
        # --- Step 2: Architecture Design ---
        if "2" in selected_agents:
            print("\n=== Starting Architecture Design ===")
            if requirement_outputs is None:
                print("Requirement outputs not available. Cannot proceed with architecture design.")
                return
                
            architecture_outputs = architecture_crew(
                requirement_output=requirement_outputs,
                project_context=project_context,
                tech_stack=config["tech_stack"]
            )
            
            if architecture_outputs is None:
                print("Architecture design failed. Stopping workflow.")
                return
                
            # Save architecture outputs
            for task_name, output in architecture_outputs.items():
                save_to_json(f"architecture_{task_name}", output)
        
        # --- Step 3: Code Skeleton Generation ---
        if "3" in selected_agents:
            print("\n=== Starting Code Skeleton Generation ===")
            if architecture_outputs is None:
                print("Architecture outputs not available. Cannot proceed with code skeleton generation.")
                return
                
            skeleton_outputs = skeletons_crew(
                architecture_output=architecture_outputs,
                project_context=project_context
            )
            
            if skeleton_outputs is None:
                print("Code skeleton generation failed. Stopping workflow.")
                return
                
            # Save skeleton outputs
            for task_name, output in skeleton_outputs.items():
                save_to_json(f"skeleton_{task_name}", output)
        
        print("\n=== Workflow Completed Successfully ===")
        print("All outputs have been saved to JSON files.")
        
    except ValueError as e:
        print(f"Configuration Error: {str(e)}")
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")

if __name__ == "__main__":
    main()