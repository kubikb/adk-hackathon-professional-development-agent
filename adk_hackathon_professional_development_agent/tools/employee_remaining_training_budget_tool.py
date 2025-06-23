"""
Employee Remaining Training Budget Tool for Professional Development System.

This tool calculates and tracks the remaining training budget for employees.
It queries BigQuery to sum up all training expenses and compares them against
the annual budget allocation to determine the available funds for future
training.

The tool helps:
- Track budget utilization
- Calculate remaining funds
- Validate training expenses
- Monitor spending patterns
- Ensure budget compliance

Example:
    ```python
    from tools.employee_remaining_training_budget_tool import remaining_budget_tool

    # Check remaining budget for an employee
    budget = remaining_budget_tool.invoke("john.doe@amazincorp.com")
    # Returns the remaining budget amount in USD
    ```

Note:
    The tool assumes a fixed annual budget of $3500 per employee and
    calculates the remaining amount by subtracting all training costs
    for the current year.
"""

import logging
from google.adk.tools import LongRunningFunctionTool
from google.cloud import bigquery
from ..utils.bigquery_operations import query_single_row, get_table_ref


def get_employee_remaining_training_budget(email: str) -> float:
    """Calculate the remaining training budget for an employee.

    This function queries the training history to sum up all expenses
    and subtracts them from the annual budget allocation.

    Args:
        email (str): The email address of the employee

    Returns:
        float: The remaining budget amount in USD. The calculation is:
            3500.0 - SUM(all training costs)

    Raises:
        Exception: If there's an error querying the database
    """
    logging.info(f"Getting remaining training budget for {email}...")

    query = """
        SELECT 
            3500.0 - SUM(cost_usd) as remaining_training_budget
        FROM `{table_ref}`
        WHERE email = @email
    """.format(
        table_ref=get_table_ref("employee_trainings")
    )

    params = [bigquery.ScalarQueryParameter("email", "STRING", email)]

    row = query_single_row(query, params)

    if row:
        return row["remaining_training_budget"]

    logging.warning(f"No training records found for email: {email}")
    return 3500.0  # Return full budget if no training records exist


# Create the tool instance
employee_remaining_training_budget_tool = LongRunningFunctionTool(
    func=get_employee_remaining_training_budget
)
