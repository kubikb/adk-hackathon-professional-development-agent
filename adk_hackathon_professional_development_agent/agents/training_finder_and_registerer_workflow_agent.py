"""
Training Workflow Agent for Professional Development System.

This agent orchestrates the multi-step process of finding and registering for training
courses. It coordinates between the training finder agent and training registerer agent
to provide a seamless experience for users wanting to find and sign up for training.

The workflow typically follows these steps:
1. Find suitable training options based on user criteria
2. Present options to the user
3. Handle the registration process for the selected training

The agent uses Google's ADK SequentialAgent to ensure proper ordering of operations
and maintain context throughout the workflow.

Example:
    ```python
    from agents.training_finder_and_registerer_workflow_agent import training_workflow_agent

    # Execute the complete find and register workflow
    response = training_workflow_agent.invoke(
        "Find a Python course under $500 and register me for it"
    )
    ```
"""

from google.adk.agents import SequentialAgent

from .training_finder_agent import training_finder_agent
from .training_registerer_agent import training_registerer_agent

training_finder_and_registerer_workflow_agent = SequentialAgent(
    name="TrainingFinderAndRegistererWorkflowAgent",
    description="Executes a sequence of training finding and registration.",
    sub_agents=[training_finder_agent, training_registerer_agent],
)
