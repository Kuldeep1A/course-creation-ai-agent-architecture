import os
import google.auth
from google.adk.agents import Agent
from google.adk.apps.app import App
from google.adk.tools import google_search

# --- Configuration ---
_, project_id = google.auth.default()
os.environ.setdefault("GOOGLE_CLOUD_PROJECT", project_id)
os.environ.setdefault("GOOGLE_CLOUD_LOCATION", "us-central1")
# Default to False for local dev if not set by environment
os.environ.setdefault("GOOGLE_GENAI_USE_VERTEXAI", "False")

# --- Researcher Agent ---
researcher = Agent(
    name="researcher",
    model="gemini-2.5-flash",
    description="Gathers information on a topic using Google Search.",
    instruction="""
    You are an expert researcher. Your goal is to find comprehensive and accurate information on the user's topic.
    Use the `google_search` tool to find relevant information.
    Summarize your findings clearly.
    If you receive feedback that your research is insufficient, use the feedback to refine your next search.
    """,
    tools=[google_search],
)

app = App(root_agent=researcher, name="researcher")