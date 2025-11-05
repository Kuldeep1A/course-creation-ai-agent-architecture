# Distributed Agent Deployment Guide

This guide details how to deploy the multi-agent system to Google Cloud Run. Each agent will run as an independent microservice.

## Prerequisites

1.  **Google Cloud Project**: Ensure you have a GCP project and the `gcloud` CLI installed and authenticated.
    ```bash
    gcloud auth login
    gcloud config set project YOUR_PROJECT_ID
    ```
2.  **APIs Enabled**: Ensure Cloud Run and Container Registry/Artifact Registry APIs are enabled.
    ```bash
    gcloud services enable run.googleapis.com containerregistry.googleapis.com
    ```

## 1. Deploy Microservices

We will deploy the standalone agents first. Note the URL of each service after deployment.

### Deploy Researcher Agent

```bash
gcloud run deploy researcher \
    --source ./researcher \
    --region us-central1 \
    --allow-unauthenticated \
    --set-env-vars GOOGLE_CLOUD_PROJECT=$(gcloud config get-value project) \
    --set-env-vars GOOGLE_CLOUD_LOCATION=us-central1 \
    --set-env-vars GOOGLE_GENAI_USE_VERTEXAI=True
```
*Copy the Service URL (e.g., `https://researcher-xyz.a.run.app`).*

### Deploy Judge Agent

```bash
gcloud run deploy judge \
    --source ./judge \
    --region us-central1 \
    --allow-unauthenticated \
    --set-env-vars GOOGLE_CLOUD_PROJECT=$(gcloud config get-value project) \
    --set-env-vars GOOGLE_CLOUD_LOCATION=us-central1 \
    --set-env-vars GOOGLE_GENAI_USE_VERTEXAI=True
```
*Copy the Service URL (e.g., `https://judge-xyz.a.run.app`).*

### Deploy Content Builder Agent

```bash
gcloud run deploy content-builder \
    --source ./content_builder \
    --region us-central1 \
    --allow-unauthenticated \
    --set-env-vars GOOGLE_CLOUD_PROJECT=$(gcloud config get-value project) \
    --set-env-vars GOOGLE_CLOUD_LOCATION=us-central1 \
    --set-env-vars GOOGLE_GENAI_USE_VERTEXAI=True
```
*Copy the Service URL (e.g., `https://content-builder-xyz.a.run.app`).*

## 2. Deploy Orchestrator

Now deploy the orchestrator, providing it with the URLs of the services you just deployed.

Replace the placeholder URLs below with your actual service URLs.

```bash
gcloud run deploy orchestrator \
    --source ./orchestrator \
    --region us-central1 \
    --allow-unauthenticated \
    --set-env-vars GOOGLE_CLOUD_PROJECT=$(gcloud config get-value project) \
    --set-env-vars GOOGLE_CLOUD_LOCATION=us-central1 \
    --set-env-vars GOOGLE_GENAI_USE_VERTEXAI=True \
    --set-env-vars RESEARCHER_AGENT_CARD_URL=https://researcher-xyz.a.run.app/.well-known/agent.json \
    --set-env-vars JUDGE_AGENT_CARD_URL=https://judge-xyz.a.run.app/.well-known/agent.json \
    --set-env-vars CONTENT_BUILDER_AGENT_CARD_URL=https://content-builder-xyz.a.run.app/.well-known/agent.json
```

**Important**:
*   Ensure you append `/.well-known/agent.json` to each service URL.
*   The `APP_URL` for the orchestrator will be automatically set by Cloud Run, but if you need to override it, you can add `--set-env-vars APP_URL=...`. Usually it's not strictly needed if it just serves the frontend.

## 3. Verification

Open the Orchestrator's Service URL in your browser. You should see the Course Creation Agent frontend. Enter a topic and watch the distributed agents work together!

