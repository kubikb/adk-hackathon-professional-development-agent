"""
Company Information Search Tool for Professional Development System.

This tool provides semantic search capabilities over company documentation
using Vertex AI Search. It enables agents to find relevant information in
company policies, procedures, and documentation stored in Google Cloud Storage.

The tool helps:
- Search company documentation
- Find relevant policies
- Access procedure guides
- Retrieve training materials
- Locate reference documents

Example:
    ```python
    from tools.company_information_search_tool import company_information_search_tool

    # Search for training policy information
    results = company_information_search_tool.invoke(
        "What is the policy for external certification courses?"
    )
    ```

Note:
    This tool uses Vertex AI Search to perform semantic search over PDF
    documents stored in Google Cloud Storage, providing more intelligent
    and context-aware search results than simple keyword matching.
"""

from google.adk.tools import VertexAiSearchTool
from ..config import config

# Create the tool instance with configured data store
company_information_search_tool = VertexAiSearchTool(
    data_store_id=f"projects/{config.google_cloud_project}/locations/{config.vertex_ai_search_data_store_location}/collections/default_collection/dataStores/{config.vertex_ai_search_data_store_id}"
)
