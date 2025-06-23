"""
Skills Development Agent for Professional Development System.

This agent helps employees assess their current skills and plan their future
skill development. It analyzes the employee's current skill set against company
project requirements and industry trends to provide personalized development
recommendations.

The agent can:
- Assess current skills
- Identify skill gaps
- Recommend learning paths
- Match skills to projects
- Suggest career development opportunities
- Track skill progression

Example:
    ```python
    from agents.current_or_future_skills_development_agent import skills_development_agent

    # Get skill development recommendations
    response = skills_development_agent.invoke(
        "What skills should I develop to work on cloud migration projects?"
    )
    ```

Note:
    This agent works closely with the project_portfolio_tool to align skill
    development recommendations with actual project needs and opportunities
    within the company.
"""

from google.adk.agents import LlmAgent

from ..config import config
from ..tools.company_information_tool import company_information_tool
from ..tools.employee_profile_tool import employee_profile_tool
from ..tools.project_portfolio_tool import project_portfolio_tool
from ..tools.training_finder_tool import training_finder_tool


current_or_future_skills_development_agent = LlmAgent(
    name="CurrentOrFutureSkillsDevelopmentAgent",
    model=config.model_name,
    description="Detects employee current or future professional skills development needs based on the current skills and company information.",
    instruction=(
        "You are a helpful agent who can detect employee current professional skills development needs based on the current skills and company information. "
        "Based on the passed email address, call the 'get_employee_profile_tool' tool to get the employee profile and current skills. "
        "Get the company information by calling the 'company_information_tool' tool. "
        "Get the project portfolio by calling the 'get_project_portfolio_tool' tool. "
        "Get the employee professional development company policy by calling the 'company_information_tool' tool. Make sure your recommendations align with the company policy. "
        "If the user would like to find training opportunities, call the 'training_finder_tool' tool to find training opportunities. Make sure to display the training's name, description, skills, date when it can be started, cost in USD, and URL in a structured format to the user for all training opportunities even if the training_finder_tool already returned them."
    ),
    output_key="current_skills_development_needs",
    tools=[
        company_information_tool,
        employee_profile_tool,
        project_portfolio_tool,
        training_finder_tool,
    ],
)
