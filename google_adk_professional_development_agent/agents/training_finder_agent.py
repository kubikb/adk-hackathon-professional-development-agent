"""
Training Finder Agent for Professional Development System.

This agent specializes in helping users find appropriate training courses. It uses natural language understanding
to interpret user requirements and searches through available training options.

Example:
    ```python
    from agents.training_finder_agent import training_finder_agent

    # Find Python training courses under $500
    response = training_finder_agent.invoke(
        "Find Python courses that cost less than $500"
    )
    ```

Note:
    This agent works in conjunction with the training_registerer_agent as part
    of the training workflow to provide a complete course registration experience.
"""

from google.adk.agents import LlmAgent
from google.adk.tools import google_search

from ..config import config

# Tried calling the training_registerer_agent here, but it was not working due to
# https://github.com/google/adk-python/issues/53
training_finder_agent = LlmAgent(
    name="TrainingFinderAgent",
    model=config.model_name,
    description="Finds training opportunities for employees based on their current skills, company information, and project portfolio.",
    instruction=(
        "You are a helpful agent who can find training opportunities for employees based on their current skills, company profile, and project portfolio. "
        "Use the 'google_search' tool to search the internet for training opportunities that align with the employee's current skills, desired future skills, and company profile. "
        "Make sure to display the training's name, description, skills, date when it can be started, cost in USD, and URL. "
    ),
    tools=[
        google_search,
    ],
)
