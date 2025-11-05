import os
import google.auth
from google.adk.agents import Agent
from google.adk.apps.app import App

# --- Configuration ---
_, project_id = google.auth.default()
os.environ.setdefault("GOOGLE_CLOUD_PROJECT", project_id)
os.environ.setdefault("GOOGLE_CLOUD_LOCATION", "us-central1")
# Default to False for local dev if not set by environment
os.environ.setdefault("GOOGLE_GENAI_USE_VERTEXAI", "False")

# --- Content Builder Agent ---
content_builder = Agent(
    name="content_builder",
    model="gemini-2.5-pro",
    description="Transforms research findings into a structured course.",
    instruction="""
    You are an expert course creator.
    Take the approved 'research_findings' and transform them into a well-structured, engaging course module.
    
    **Formatting Rules:**
    1. Start with a main title using a single `#` (H1).
    2. Use `##` (H2) for main section headings. These will be used for the Table of Contents.
    3. Use bullet points and clear paragraphs.
    4. Maintain a professional but engaging tone.
    
    Ensure the content directly addresses the user's original request.
    """,
)

app = App(root_agent=content_builder, name="content_builder")
