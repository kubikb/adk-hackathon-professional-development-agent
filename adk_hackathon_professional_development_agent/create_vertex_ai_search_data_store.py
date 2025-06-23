"""
Vertex AI Search Data Store Creation and Import Script.

This script provides functionality to:
1. Create a new Vertex AI Search data store
2. Import documents from Google Cloud Storage into the data store

The script uses the Discovery Engine API to create and manage search data stores.
It's designed to work with PDF documents stored in a GCS bucket, making them
searchable through Vertex AI Search.

Example:
    ```bash
    # Run the script with required configuration
    python create_vertex_ai_search_data_store.py
    ```

Note:
    This implementation is based on the official Google Cloud documentation:
    https://cloud.google.com/generative-ai-app-builder/docs/create-data-store-es#storage-import-once
"""

import logging

from google.api_core.client_options import ClientOptions
from google.cloud import discoveryengine

from config import Config

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

# Source: https://cloud.google.com/generative-ai-app-builder/docs/create-data-store-es#storage-import-once


def create_data_store(
    client_options: ClientOptions, project_id: str, location: str, data_store_id: str
) -> str:
    """Create a new Vertex AI Search data store.

    This function creates a new data store in Vertex AI Search with specified
    configuration settings. The data store is configured for generic content
    and search functionality.

    Args:
        client_options (ClientOptions): Configuration options for the API client
        project_id (str): Google Cloud Project ID
        location (str): Geographic location for the data store
        data_store_id (str): Unique identifier for the new data store

    Returns:
        str: The operation name for the create data store request

    Raises:
        Exception: If the data store creation fails
    """
    # Create a client
    client = discoveryengine.DataStoreServiceClient(client_options=client_options)

    # The full resource name of the collection
    # e.g. projects/{project}/locations/{location}/collections/default_collection
    parent = client.collection_path(
        project=project_id,
        location=location,
        collection="default_collection",
    )
    logging.info(f"Parent: {parent}")

    data_store = discoveryengine.DataStore(
        display_name=data_store_id,
        # Options: GENERIC, MEDIA, HEALTHCARE_FHIR
        industry_vertical=discoveryengine.IndustryVertical.GENERIC,
        # Options: SOLUTION_TYPE_RECOMMENDATION, SOLUTION_TYPE_SEARCH, SOLUTION_TYPE_CHAT, SOLUTION_TYPE_GENERATIVE_CHAT
        solution_types=[discoveryengine.SolutionType.SOLUTION_TYPE_SEARCH],
        # TODO(developer): Update content_config based on data store type.
        # Options: NO_CONTENT, CONTENT_REQUIRED, PUBLIC_WEBSITE
        content_config=discoveryengine.DataStore.ContentConfig.CONTENT_REQUIRED,
    )

    request = discoveryengine.CreateDataStoreRequest(
        parent=parent,
        data_store_id=data_store_id,
        data_store=data_store,
    )

    logging.info(f"Request: {request}")

    # Make the request
    operation = client.create_data_store(request=request)

    logging.info(f"Waiting for operation to complete: {operation.operation.name}")
    response = operation.result()

    # After the operation is complete,
    # get information from operation metadata
    metadata = discoveryengine.CreateDataStoreMetadata(operation.metadata)

    # Handle the response
    logging.info(f"Response: {response}")
    logging.info(f"Metadata: {metadata}")

    return operation.operation.name


def import_gcs_data_into_data_store(
    client_options: ClientOptions,
    project_id: str,
    gcs_bucket_name: str,
    location: str,
    data_store_id: str,
) -> str:
    """Import documents from Google Cloud Storage into the data store.

    This function imports PDF documents from a specified GCS bucket into
    the Vertex AI Search data store. It supports incremental updates to
    the document collection.

    Args:
        client_options (ClientOptions): Configuration options for the API client
        project_id (str): Google Cloud Project ID
        gcs_bucket_name (str): Name of the GCS bucket containing the documents
        location (str): Geographic location of the data store
        data_store_id (str): ID of the target data store

    Raises:
        Exception: If the document import operation fails
    """
    # Create a client
    client = discoveryengine.DocumentServiceClient(client_options=client_options)

    # The full resource name of the search engine branch.
    # e.g. projects/{project}/locations/{location}/dataStores/{data_store_id}/branches/{branch}
    parent = client.branch_path(
        project=project_id,
        location=location,
        data_store=data_store_id,
        branch="default_branch",
    )

    request = discoveryengine.ImportDocumentsRequest(
        parent=parent,
        gcs_source=discoveryengine.GcsSource(
            input_uris=[f"gs://{gcs_bucket_name}/*.pdf"],
            data_schema="content",
        ),
        # Options: `FULL`, `INCREMENTAL`
        reconciliation_mode=discoveryengine.ImportDocumentsRequest.ReconciliationMode.INCREMENTAL,
    )

    # Make the request
    operation = client.import_documents(request=request)

    logging.info(f"Waiting for operation to complete: {operation.operation.name}")
    response = operation.result()

    # After the operation is complete,
    # get information from operation metadata
    metadata = discoveryengine.ImportDocumentsMetadata(operation.metadata)

    # Handle the response
    logging.info(f"Response: {response}")
    logging.info(f"Metadata: {metadata}")


if __name__ == "__main__":
    location = Config.vertex_ai_search_data_store_location
    client_options = (
        ClientOptions(api_endpoint=f"{location}-discoveryengine.googleapis.com")
        if location != "global"
        else None
    )
    # Create data store
    create_data_store(
        client_options=client_options,
        project_id=Config.google_cloud_project,
        location=location,
        data_store_id=Config.vertex_ai_search_data_store_id,
    )

    # Import data from GCS
    import_gcs_data_into_data_store(
        client_options=client_options,
        project_id=Config.google_cloud_project,
        location=location,
        data_store_id=Config.vertex_ai_search_data_store_id,
        gcs_bucket_name=Config.vertex_ai_search_data_store_bucket,
    )
