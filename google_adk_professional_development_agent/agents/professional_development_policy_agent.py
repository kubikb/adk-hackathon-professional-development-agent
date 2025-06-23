"""
Professional Development Policy Agent for Professional Development System.

This agent specializes in explaining and interpreting the company's professional
development policies. It provides clear, consistent information about training
budgets, approval processes, and development opportunities using Vertex AI Search
to access official policy documentation.

Example:
    ```python
    from agents.professional_development_policy_agent import professional_development_policy_agent

    # Get information about training budget policies
    response = professional_development_policy_agent.invoke(
        "What is the annual training budget per employee?"
    )
    ```

Note:
    This agent works in conjunction with the company_information_agent but focuses
    specifically on professional development and training-related policies.
"""

from google.adk.agents import LlmAgent

from ..config import config
from ..tools.company_information_tool import (
    company_information_tool,
)

professional_development_policy_agent = LlmAgent(
    name="ProfessionalDevelopmentPolicyAgent",
    model=config.model_name,
    description="Describes and answers questions about the employee professional development company policy.",
    instruction=(
        "You are a helpful agent who can describe and answer questions about the employee professional development company policy. "
        "You will be given a question about the employee professional development company policy. "
        "You will need to describe the employee professional development company policy and answer the question. "
        "You will need to make sure your recommendations align with the company policy. "
        "Use the 'get_employee_professional_development_company_policy' tool to get the actual employee professional development company policy. "
    ),
    tools=[company_information_tool],
)
