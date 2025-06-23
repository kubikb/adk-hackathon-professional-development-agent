"""
Project Portfolio Tool for Professional Development System.

This tool provides access to the company's project portfolio information stored
in BigQuery. It retrieves information about current and upcoming projects,
including required skills, customer details, and project status. This information
is used by agents to recommend relevant training based on project needs.

The tool helps:
- Identify skill requirements for projects
- Track project status and timelines
- Match employee skills to project needs
- Guide professional development planning

Example:
    ```python
    from tools.project_portfolio_tool import project_portfolio_tool

    # Get all active projects
    projects = project_portfolio_tool.invoke()
    # Returns list of projects with details about required skills,
    # customer information, and current status
    ```
"""

import logging
from google.adk.tools import LongRunningFunctionTool
from ..utils.bigquery_operations import query_multiple_rows, get_table_ref


# Instead of directly querying the BigQuery table, we could use MCP Toolbox for Databases.
# Sample for BigQuery here: https://googleapis.github.io/genai-toolbox/samples/bigquery/mcp_quickstart/
def get_project_portfolio() -> list[dict]:
    """Retrieve the company's project portfolio from BigQuery.

    This function fetches all projects and their details, including:
    - Project name and description
    - Customer information
    - Required skills
    - Project status

    Returns:
        list[dict]: List of project dictionaries, each containing:
            - name (str): Project name
            - customer (str): Customer name
            - customer_profile (str): Type of customer
            - customer_location (str): Customer's location
            - description (str): Project description
            - skills_needed (str): Required skills
            - status (str): Current project status

    Raises:
        Exception: If there's an error querying the database
    """
    logging.info("Getting project portfolio...")

    query = """
        SELECT 
            name,
            customer,
            customer_profile,
            customer_location,
            description,
            skills_needed,
            status
        FROM `{table_ref}`
    """.format(
        table_ref=get_table_ref("project_portfolio")
    )

    return query_multiple_rows(query)


project_portfolio_tool = LongRunningFunctionTool(func=get_project_portfolio)
