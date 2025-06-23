"""
Register New Training Tool for Professional Development System.

This tool handles the registration of new training activities in the system.
It creates new training records in BigQuery with all relevant details about
the course, including cost, date, and associated skills. The tool is used
by the training registerer agent to complete course registrations.

The tool helps:
- Record new training registrations
- Store course details
- Track training costs
- Maintain training history
- Link skills to courses

Example:
    ```python
    from tools.register_new_training_tool import register_new_training_tool

    # Register a new training course
    register_new_training_tool.invoke(
        email="john.doe@amazincorp.com",
        name="Advanced Python Programming",
        description="Deep dive into Python advanced features",
        skills="Python, Software Development",
        date="2024-04-15",
        cost_usd=299.99,
        url="https://example.com/python-course"
    )
    ```

Note:
    This tool should be used after budget verification and approval
    processes have been completed.
"""

import logging
from google.adk.tools import LongRunningFunctionTool
from ..utils.bigquery_operations import insert_json_row


# Instead of directly querying the BigQuery table, we could use MCP Toolbox for Databases.
# Sample for BigQuery here: https://googleapis.github.io/genai-toolbox/samples/bigquery/mcp_quickstart/
def register_new_training(
    email: str,
    name: str,
    description: str,
    skills: str,
    date: str,
    cost_usd: float,
    url: str,
) -> None:
    """Register a new training course for an employee.

    This function creates a new training record in the database with
    all the relevant course information.

    Args:
        email (str): Employee's email address
        name (str): Name of the training course
        description (str): Course description
        skills (str): Comma-separated list of skills covered
        date (str): Course date in YYYY-MM-DD format
        cost_usd (float): Course cost in USD
        url (str): Course URL or registration link

    Raises:
        Exception: If there's an error inserting the record
    """
    logging.info(f"Registering new training for {email}...")

    training_data = {
        "email": email,
        "name": name,
        "description": description,
        "skills": skills,
        "date": date,
        "cost_usd": cost_usd,
        "url": url,
    }

    insert_json_row("employee_trainings", training_data)
    logging.info("Training registration completed successfully")


# Create the tool instance
register_new_training_tool = LongRunningFunctionTool(func=register_new_training)
