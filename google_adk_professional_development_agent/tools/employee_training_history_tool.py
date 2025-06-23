"""
Employee Training History Tool for Professional Development System.

This tool provides access to employee training records stored in BigQuery.
It retrieves detailed information about completed and ongoing training activities,
including course details, dates, costs, and associated skills.

The tool helps:
- Track training completion
- Monitor training investments
- Analyze learning patterns
- Verify course participation
- Generate training reports

Example:
    ```python
    from tools.employee_training_history_tool import employee_training_history_tool

    # Get training history for an employee
    history = employee_training_history_tool.invoke("john.doe@amazincorp.com")
    # Returns list of training records with details about courses,
    # dates, costs, and skills covered
    ```
"""

import logging

from google.cloud import bigquery
from google.adk.tools import LongRunningFunctionTool

from ..utils.bigquery_operations import query_multiple_rows, get_table_ref


# Instead of directly querying the BigQuery table, we could use MCP Toolbox for Databases.
# Sample for BigQuery here: https://googleapis.github.io/genai-toolbox/samples/bigquery/mcp_quickstart/
def get_employee_training_history(email: str) -> list[dict]:
    """Retrieve an employee's training history from BigQuery.

    This function fetches all training records for a specific employee,
    including details about completed and ongoing courses.

    Args:
        email (str): The email address of the employee

    Returns:
        list[dict]: List of training records, each containing:
            - name (str): Training course name
            - email (str): Employee email
            - description (str): Course description
            - skills (str): Skills covered
            - date (str): Training date (YYYY-MM-DD)
            - cost_usd (float): Course cost
            - url (str): Course URL

    Raises:
        Exception: If there's an error querying the database
    """
    logging.info(f"Getting employee training history for {email}...")

    query = """
        SELECT 
            name,
            email,
            description,
            skills,
            date,
            cost_usd,
            url
        FROM `{table_ref}`
        WHERE email = @email
    """.format(
        table_ref=get_table_ref("employee_trainings")
    )

    params = [bigquery.ScalarQueryParameter("email", "STRING", email)]

    results = query_multiple_rows(query, params)

    # Format dates in the results
    for row in results:
        row["date"] = row["date"].strftime("%Y-%m-%d")

    return results


employee_training_history_tool = LongRunningFunctionTool(
    func=get_employee_training_history
)
