from google.adk.tools.agent_tool import AgentTool

from ..agents.company_information_agent import company_information_agent

# The only reason the company_information_search_tool is not used directly is because, currently,
# only one built-in tool is supported for each root agent or single agent. No other tools of any type can be used in the same agent.
# This is a way to circumvent this limitation.
# For more information, see https://google.github.io/adk-docs/tools/built-in-tools/#limitations
company_information_tool = AgentTool(company_information_agent)
