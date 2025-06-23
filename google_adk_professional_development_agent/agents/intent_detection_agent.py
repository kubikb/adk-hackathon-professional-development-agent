"""
Intent Detection Agent for Professional Development System.

This agent serves as the primary entry point for user queries, determining the appropriate
specialized agent to handle each request. It analyzes user input to classify the intent
into predefined categories related to professional development activities.

The agent uses Google's ADK LlmAgent with a specialized system prompt to accurately
categorize user requests into specific intents that map to other agents in the system.

Supported Intents:
    - GET_EMPLOYEE_PROFILE: Retrieve employee information
    - GET_TRAINING_HISTORY: Get past training records
    - GET_REMAINING_BUDGET: Check available training budget
    - REGISTER_TRAINING: Sign up for new training
    - FIND_TRAINING: Search for available training options
    - GET_PROJECT_PORTFOLIO: View company projects
    - GET_COMPANY_INFORMATION: Access company policies and info
    - GET_PROFESSIONAL_DEVELOPMENT_POLICY: Review development policies
    - GET_SKILLS_DEVELOPMENT: Get skills assessment and recommendations
    - UNKNOWN: Default for unrecognized requests

Example:
    ```python
    from agents.intent_detection_agent import intent_detection_agent

    # Get intent for a user query
    response = intent_detection_agent.invoke("I want to find Python training courses")
    # Returns: "FIND_TRAINING"
    ```
"""

from google.adk.agents import LlmAgent

from ..config import config
from .professional_development_policy_agent import professional_development_policy_agent
from .employee_training_history_and_budget_agent import (
    employee_training_history_and_budget_agent,
)
from .current_or_future_skills_development_agent import (
    current_or_future_skills_development_agent,
)
from .training_registerer_agent import training_registerer_agent

intent_detection_agent = LlmAgent(
    name="IntentDetectionAgent",
    model=config.model_name,
    description="Agent to detect the intent of the user's query.",
    instruction=(
        "You are a helpful agent who can detect user intent and contact the appropriate, specialized agent based on the detected intent. "
        "If the user did not pass employee email, refuse to answer the query and ask the user to pass the employee email. "
        "If the user is looking for employee current or future professional skills development needs, contact the 'CurrentOrFutureSkillsDevelopmentAgent' agent. "
        "If the user is looking for their own employee training history and remaining training budget, contact the 'EmployeeTrainingHistoryAndRemainingTrainingBudgetAgent' agent. "
        "If the user is looking for the employee professional development company policy or has questions about the company policy, contact the 'EmployeeProfessionalDevelopmentCompanyPolicyAgent' agent. In this case, do not require the email from the user. "
        "If the user would like to register for a new training, contact the 'TrainingRegistererAgent' agent. If the user wants to find a new course, do not contact the 'TrainingRegistererAgent' agent."
    ),
    sub_agents=[
        current_or_future_skills_development_agent,
        professional_development_policy_agent,
        employee_training_history_and_budget_agent,
        training_registerer_agent,
    ],
    output_key="email",
)
