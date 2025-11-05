# course-creation-agent (Distributed)

A multi-agent system built with Google's Agent Development Kit (ADK) and Agent-to-Agent (A2A) protocol. It features a team of microservice agents that research, judge, and build content, orchestrated to deliver high-quality results.

## Architecture

This project uses a distributed microservices architecture where each agent runs in its own container and communicates via A2A:

*   **Orchestrator Service (`orchestrator/`):** The main entry point. It manages the workflow using `LoopAgent` and `SequentialAgent`, and connects to other agents using `RemoteA2aAgent`. It also serves the frontend.
*   **Researcher Service (`researcher/`):** A standalone agent that gathers information using Google Search.
*   **Judge Service (`judge/`):** A standalone agent that evaluates research quality.
*   **Content Builder Service (`content_builder/`):** A standalone agent that compiles the final course.

## Project Structure

```
course-creation-agent/
├── orchestrator/        # Main service (orchestration + frontend)
│   ├── app/
│   ├── frontend/
│   └── Dockerfile
├── researcher/          # Researcher microservice
│   ├── app/
│   └── Dockerfile
├── judge/               # Judge microservice
│   ├── app/
│   └── Dockerfile
├── content_builder/     # Content Builder microservice
│   ├── app/
│   └── Dockerfile
├── docker-compose.yml   # For running the distributed system locally
├── Makefile             # Command shortcuts
└── ...
```

## Requirements

*   **Docker & Docker Compose**: For running the distributed system.
*   **Google Cloud SDK**: For GCP services and authentication.
*   **uv**: Python package manager (optional, for local non-docker dev).

## Quick Start (Distributed)

1.  **Set up credentials:**
    Ensure you have Google Cloud credentials available to Docker. You might need to run:
    ```bash
    gcloud auth application-default login
    ```
    And ensure your `GOOGLE_CLOUD_PROJECT` and `GOOGLE_API_KEY` (if using Gemini API) environment variables are set.

2.  **Run with Docker Compose:**
    ```bash
    make run-distributed
    ```
    This will build all 4 images and start them.

3.  **Access the App:**
    Open **http://localhost:8000** in your browser.

## Deployment

To deploy to Google Cloud Run, you need to deploy each service individually and then configure the Orchestrator with the URLs of the other services.

1.  **Deploy Researcher, Judge, Content Builder:**
    Deploy each of these folders as a separate Cloud Run service. Note down their URLs (e.g., `https://researcher-xyz.a.run.app`).

2.  **Deploy Orchestrator:**
    Deploy the `orchestrator/` folder to Cloud Run.
    Set the following environment variables on the Orchestrator service:
    *   `RESEARCHER_AGENT_CARD_URL`: `https://<researcher-url>/a2a/researcher_app/.well-known/agent.json`
    *   `JUDGE_AGENT_CARD_URL`: `https://<judge-url>/a2a/judge_app/.well-known/agent.json`
    *   `CONTENT_BUILDER_AGENT_CARD_URL`: `https://<content-builder-url>/a2a/content_builder_app/.well-known/agent.json`
    *   `APP_URL`: `https://<orchestrator-url>`

3.  **Access:**
    Open the Orchestrator's URL in your browser.
