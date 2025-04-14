import os
import json
from dotenv import load_dotenv
from crewai import Crew
from requirements import RequirementAnalyzer

load_dotenv()

# Initialize the RequirementAnalyzer class
requirement_analyzer = RequirementAnalyzer(
    user_requirements="Build an e-commerce website with product listings, user authentication, and payment integration.",
    project_context="The project is an online marketplace for various products, supporting multiple vendors."
)

ex = requirement_analyzer.extraction_task()

result = requirement_analyzer.crew().kickoff()

# Run each task independently
print(ex.output)

print("-------------------------------------")

print(ex.output.pydantic)
