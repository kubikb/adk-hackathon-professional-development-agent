"""
Employee Profile Tool for Professional Development System.

This tool provides access to employee profile information stored in BigQuery.
It handles retrieval of employee data including their name, department, role,
and skills. The tool is used by various agents to access and verify employee
information when processing training-related requests.

The tool uses the BigQuery operations utility to safely query the employee_profiles
table and format the results in a consistent structure.

Example:
    ```python
    from tools.employee_profile_tool import employee_profile_tool

    # Get an employee's profile
    profile = employee_profile_tool.invoke("john.doe@amazincorp.com")
    # Returns: {
    #     "name": "John Doe",
    #     "email": "john.doe@amazincorp.com",
    #     "department": "IT",
    #     "role": "Senior Software Engineer",
    #     "skills": ["Python", "Java", "Google Cloud"]
    # }
    ```
"""

import logging
from google.adk.tools import FunctionTool
from google.cloud import bigquery
from ..utils.bigquery_operations import query_single_row, get_table_ref


def get_employee_profile(email: str) -> dict:
    """Retrieve an employee's profile information from BigQuery.

    This function fetches employee data including their name, department,
    role, and skills. It converts the comma-separated skills string into
    a list for easier processing.

    Args:
        email (str): The email address of the employee to look up

    Returns:
        dict: Employee profile information with the following structure:
            - name (str): Full name of the employee
            - email (str): Email address
            - department (str): Department name
            - role (str): Job role/title
            - skills (List[str]): List of employee's skills

        Returns None if no profile is found for the given email.

    Raises:
        Exception: If there's an error querying the database
    """
    logging.info(f"Getting employee profile for {email}...")

    query = """
        SELECT 
            name,
            email,
            department,
            role,
            skills
        FROM `{table_ref}`
        WHERE email = @email
    """.format(
        table_ref=get_table_ref("employee_profiles")
    )

    params = [bigquery.ScalarQueryParameter("email", "STRING", email)]

    row = query_single_row(query, params)

    if row:
        # Convert skills string to list
        row["skills"] = [skill.strip() for skill in row["skills"].split(",")]
        return row

    logging.warning(f"No profile found for email: {email}")
    return None


# Create the tool instance
employee_profile_tool = FunctionTool(func=get_employee_profile)
