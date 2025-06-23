"""
Employee Training History and Budget Agent for Professional Development System.

This agent manages access to employee training records and budget information.
It provides insights into past training activities, tracks budget utilization,
and helps employees understand their remaining training allowance. The agent
uses BigQuery to access and analyze training records.

The agent can:
- Retrieve training history
- Calculate remaining budget
- Track training expenses
- Provide spending analysis
- Generate training summaries

Example:
    ```python
    from agents.employee_training_history_and_budget_agent import training_history_budget_agent

    # Get training history and budget information
    response = training_history_budget_agent.invoke(
        "Show me my training history and remaining budget for this year"
    )
    ```

Note:
    This agent is often consulted by the training_finder_agent and
    training_registerer_agent to validate budget availability for new
    training requests.
"""

from google.adk.agents import LlmAgent

from ..config import config
from ..tools.employee_training_history_tool import employee_training_history_tool
from ..tools.employee_remaining_training_budget_tool import (
    employee_remaining_training_budget_tool,
)

employee_training_history_and_budget_agent = LlmAgent(
    name="EmployeeTrainingHistoryAndRemainingTrainingBudgetAgent",
    model=config.model_name,
    description="Describes and answers questions about the employee training history and remaining training budget.",
    instruction=(
        "You are a helpful agent who can describe and answer questions about the employee training history and remaining training budget. "
        "You will be given a question about the employee training history and remaining training budget. "
        "You will need to describe the employee training history and remaining training budget and answer the question. "
        "Use the 'get_employee_training_history' tool to get the actual employee training history. "
        "Use the 'get_employee_remaining_training_budget' tool to get the actual employee remaining training budget. "
    ),
    tools=[
        employee_training_history_tool,
        employee_remaining_training_budget_tool,
    ],
)
