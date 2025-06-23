"""
Configuration module for the Professional Development Agent.

This module provides a centralized configuration management system for the application.
It handles all environment variables and configuration settings needed across the application,
including Google Cloud Project settings, BigQuery configurations, and Vertex AI Search parameters.

Environment Variables:
    GOOGLE_CLOUD_PROJECT (str): The Google Cloud Project ID
    BIGQUERY_DATASET_ID (str): The BigQuery dataset ID (defaults to "amazincorp")
    VERTEX_AI_SEARCH_DATA_STORE_ID (str): The Vertex AI Search data store ID
    VERTEX_AI_SEARCH_DATA_STORE_LOCATION (str): The location for Vertex AI Search data store
    VERTEX_AI_SEARCH_DATA_STORE_BUCKET (str): The GCS bucket for Vertex AI Search data
    MODEL_NAME (str): The name of the LLM model to use (defaults to "gemini-2.0-flash")
    VERTEX_AI_STAGING_BUCKET (str): The GCS bucket for Vertex AI staging

Example:
    ```python
    from config import Config

    # Access configuration values
    project_id = Config.google_cloud_project
    dataset_id = Config.bigquery_dataset_id
    ```
"""

import os
from dataclasses import dataclass


@dataclass
class Config:
    """Configuration class that holds all environment variables and settings.

    This class uses the dataclass decorator to create an immutable configuration object.
    It provides type hints and default values for all configuration parameters.

    Attributes:
        google_cloud_project (str): Google Cloud Project ID
        bigquery_dataset_id (str): BigQuery dataset ID
        vertex_ai_search_data_store_id (str): Vertex AI Search data store ID
        vertex_ai_search_data_store_location (str): Location for Vertex AI Search
        vertex_ai_search_data_store_bucket (str): GCS bucket for Vertex AI Search
        model_name (str): Name of the LLM model to use
        vertex_ai_staging_bucket (str): GCS bucket for Vertex AI staging
    """

    # Google Cloud Project configuration
    google_cloud_project: str = os.getenv("GOOGLE_CLOUD_PROJECT", "")

    # Google Cloud Location
    google_cloud_location: str = os.getenv("GOOGLE_CLOUD_LOCATION", "US")

    # BigQuery configuration
    bigquery_dataset_id: str = os.getenv("BIGQUERY_DATASET_ID", "amazincorp")

    # Vertex AI Search configuration
    vertex_ai_search_data_store_id: str = os.getenv(
        "VERTEX_AI_SEARCH_DATA_STORE_ID", ""
    )
    vertex_ai_search_data_store_location: str = os.getenv(
        "VERTEX_AI_SEARCH_DATA_STORE_LOCATION", "global"
    )
    vertex_ai_search_data_store_bucket: str = os.getenv(
        "VERTEX_AI_SEARCH_DATA_STORE_BUCKET", ""
    )

    # LLM Model configuration
    model_name: str = os.getenv("MODEL_NAME", "gemini-2.0-flash")

    # Vertex AI staging bucket
    vertex_ai_staging_bucket: str = os.getenv("VERTEX_AI_STAGING_BUCKET")

    @property
    def is_valid(self) -> bool:
        """Check if all required configuration values are set.

        Returns:
            bool: True if all required values are set, False otherwise.
        """
        return bool(
            self.google_cloud_project
            and self.bigquery_dataset_id
            and self.vertex_ai_search_data_store_id
            and self.model_name
        )

    def validate(self) -> None:
        """Validate the configuration and raise an error if invalid.

        This method checks all required configuration values and raises a ValueError
        if any required values are missing.

        Raises:
            ValueError: If any required configuration values are missing.
        """
        if not self.is_valid:
            missing = []
            if not self.google_cloud_project:
                missing.append("GOOGLE_CLOUD_PROJECT")
            if not self.bigquery_dataset_id:
                missing.append("BIGQUERY_DATASET_ID")
            if not self.vertex_ai_search_data_store_id:
                missing.append("VERTEX_AI_SEARCH_DATA_STORE_ID")
            if not self.model_name:
                missing.append("MODEL_NAME")

            raise ValueError(
                f"Missing required environment variables: {', '.join(missing)}"
            )


# Create a singleton instance
config = Config()

# Validate configuration on import
config.validate()
