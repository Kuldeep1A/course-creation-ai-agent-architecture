import os
from typing import Literal
import google.auth
from google.adk.agents import Agent
from google.adk.apps.app import App
from pydantic import BaseModel, Field

# --- Configuration ---
_, project_id = google.auth.default()
os.environ.setdefault("GOOGLE_CLOUD_PROJECT", project_id)
os.environ.setdefault("GOOGLE_CLOUD_LOCATION", "us-central1")
# Default to False for local dev if not set by environment
os.environ.setdefault("GOOGLE_GENAI_USE_VERTEXAI", "False")

# --- Data Models ---
class JudgeFeedback(BaseModel):
    """Structured feedback from the Judge agent."""
    status: Literal["pass", "fail"] = Field(
        description="Whether the research is sufficient ('pass') or needs more work ('fail')."
    )
    feedback: str = Field(
        description="Detailed feedback on what is missing or needs clarification if status is 'fail'. If 'pass', a brief confirmation."
    )

# --- Judge Agent ---
judge = Agent(
    name="judge",
    model="gemini-2.5-flash",
    description="Evaluates research findings for completeness and accuracy.",
    instruction="""
    You are a strict editor and fact-checker.
    Evaluate the 'research_findings' against the user's original request.
    Determine if the findings are sufficient to create a high-quality course.
    If they are good enough, output status='pass'.
    If they are missing key information, are too vague, or likely inaccurate, output status='fail' and provide specific, constructive 'feedback' on what to research next.
    """,
    output_schema=JudgeFeedback,
    # Disallow transfers as it uses output_schema
    disallow_transfer_to_parent=True,
    disallow_transfer_to_peers=True,
)

app = App(root_agent=judge, name="judge")