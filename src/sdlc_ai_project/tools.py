from crewai.tools import tool
from crewai_tools import SerperDevTool, GithubSearchTool
from dotenv import load_dotenv
from embedchain import App
import os

load_dotenv()

@tool("Code Research Tool")
def code_research_tool(query: str):
    """Tool description for clarity."""
    print("CODE RESEARCH TOOL CALLED with query: ", query)
    search_resuts = SerperDevTool(
        search_url = ("Similar github projects for the domain ", query),
        n_results=5
    )
    links = []
    config = {
        "vectordb": {
            "provider": "chroma",
            "config": {
                "collection_name": "default_collection",
                "dir": "./db/default_ragtool_db",
                "allow_reset": False
            }
        }
    }
    print("Search Results:", search_resuts['organic'])
    app = App.from_config(config=config)
    for link in search_resuts['organic']:
        print("LINK:", link['link'])
        try:
            app.add(
                GithubSearchTool(
                    github_repo=link['link'],
                    gh_token = os.environ["gh_key"],
                    content_types=["code"],
                )
            )
        except:
            print("Invalid Github Link")
            continue


    # Perform the query
    result = app.query("Summarize code patterns relevant to", query)
    print("TOOL RESULT: ", result)
    return ("Relevant Context: ", result)

# code_research_tool(query="A simple web application for task management")

