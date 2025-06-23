"""
Vertex AI Agent Engine Deployment Script for Professional Development System.

This script handles the deployment of the Professional Development Agent system
to Google Cloud's Vertex AI Agent Engine. It sets up the necessary environment,
initializes the Vertex AI client, and deploys the intent detection agent along
with all required dependencies.

The deployment process:
1. Initializes Vertex AI with project and location settings
2. Creates an ADK App instance with tracing enabled
3. Deploys the agent with required environment variables
4. Sets up dependencies and additional packages

Required Environment Variables (from Config):
    - GOOGLE_CLOUD_PROJECT: Google Cloud project ID
    - GOOGLE_CLOUD_LOCATION: Deployment location (e.g., "us-central1")
    - VERTEX_AI_STAGING_BUCKET: GCS bucket for staging deployment files
    - BIGQUERY_DATASET_ID: Dataset ID for BigQuery operations
    - VERTEX_AI_SEARCH_DATA_STORE_ID: Vertex AI Search data store identifier

Dependencies:
    - google-cloud-aiplatform[adk,agent_engines]: Core ADK and Agent Engine support
    - google-cloud-bigquery: For database operations
    - google-cloud-discoveryengine: For Vertex AI Search integration

Example:
    ```bash
    # Deploy the agent to Vertex AI Agent Engine
    python deploy_to_vertex_ai_agent_engine.py
    ```

Note:
    The script uses the intent_detection_agent as the main entry point,
    which then coordinates with other specialized agents based on the
    detected user intent.
"""

import logging

import vertexai
from vertexai import agent_engines
from vertexai.preview import reasoning_engines

from adk_hackathon_professional_development_agent.config import Config
from adk_hackathon_professional_development_agent.agents.intent_detection_agent import (
    intent_detection_agent,
)

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

if __name__ == "__main__":
    vertexai.init(
        project=Config.google_cloud_project,
        location=Config.google_cloud_location,
        staging_bucket=f"gs://{Config.vertex_ai_staging_bucket}",
    )

    app = reasoning_engines.AdkApp(
        agent=intent_detection_agent,
        enable_tracing=True,
    )

    remote_app = agent_engines.create(
        agent_engine=intent_detection_agent,
        env_vars={
            "BIGQUERY_DATASET_ID": Config.bigquery_dataset_id,
            "VERTEX_AI_SEARCH_DATA_STORE_ID": Config.vertex_ai_search_data_store_id,
        },
        extra_packages=[
            "google_adk_professional_development_agent",
        ],
        requirements=[
            "google-cloud-aiplatform[adk,agent_engines]",
            "google-cloud-bigquery",
            "google-cloud-discoveryengine",
        ],
    )

    logging.info(
        f"Agent deployed to Vertex AI Agent Engine: {remote_app.resource_name}"
    )
