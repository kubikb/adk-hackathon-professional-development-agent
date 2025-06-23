"""
Training Finder Tool for Professional Development System.

This is an AgentTool that uses the training_finder_agent to find training opportunities.

Note:
    This tool works in conjunction with the training_registerer_tool to provide a complete course discovery and registration workflow.
"""

from google.adk.tools.agent_tool import AgentTool

from ..agents.training_finder_agent import training_finder_agent

training_finder_tool = AgentTool(training_finder_agent)
