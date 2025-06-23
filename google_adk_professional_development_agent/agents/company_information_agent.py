"""
Company Information Agent for Professional Development System.

This agent provides access to company-wide information, policies, and resources
related to professional development. It uses Vertex AI Search to find relevant
information from company documentation and provides contextual responses to
user queries.

The agent can:
- Explain company policies
- Provide information about benefits
- Detail development programs
- Answer questions about company culture
- Guide users to relevant resources

Example:
    ```python
    from agents.company_information_agent import company_information_agent

    # Get information about training policies
    response = company_information_agent.invoke(
        "What is our company's policy on external training courses?"
    )
    ```

Note:
    This agent uses Vertex AI Search to access and search through company
    documentation stored in Google Cloud Storage.
"""

from google.adk.agents import LlmAgent

from ..config import config
from ..tools.company_information_search_tool import company_information_search_tool

# The only reason the company_information_search_tool is not used directly is because, currently,
# only one built-in tool is supported for each root agent or single agent. No other tools of any type can be used in the same agent.
# Using the agent as AgentTool circumvents this limitation.
# For more information, see https://google.github.io/adk-docs/tools/built-in-tools/#limitations
company_information_agent = LlmAgent(
    name="CompanyInformationAgent",
    model=config.model_name,
    description="Can answer questions about the company's information.",
    instruction=(
        "You are a helpful agent who can answer questions about the company's information. "
        "You can answer questions and return information about the company's information, such as the company's history, mission, values, and more. "
        "You can also answer questions and return information about the company's professional development policy. "
    ),
    tools=[
        company_information_search_tool,
    ],
)
