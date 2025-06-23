"""
Training Registerer Agent for Professional Development System.

This agent handles the process of registering employees for training courses.
It manages the entire registration workflow, including budget verification,
approval processes, and registration confirmation. The agent works closely
with the training finder agent to complete the course registration process.

The agent can:
- Verify training budget availability
- Process registration requests
- Handle approval workflows
- Confirm registrations
- Update training records
- Send confirmation details

Example:
    ```python
    from agents.training_registerer_agent import training_registerer_agent

    # Register for a specific training course
    response = training_registerer_agent.invoke(
        "Register me for the Python Advanced Course starting next month"
    )
    ```

Note:
    This agent is typically used as part of a workflow with the training_finder_agent,
    but can also be used independently when course details are already known.
"""

from google.adk.agents import LlmAgent

from ..config import config
from ..tools.register_new_training_tool import register_new_training_tool


training_registerer_agent = LlmAgent(
    name="TrainingRegistererAgent",
    model=config.model_name,
    description="Registers new training opportunities for employees.",
    instruction=(
        "You are a helpful agent who can register new training opportunities for employees. "
        "You will be given a new training opportunity by the user. "
        "You will need to register the new training opportunity in the database. "
        "Access the chosen training in session state under key 'chosen_training'. "
        "Use the 'register_new_employee_training_tool' tool to register the new training. "
    ),
    tools=[
        register_new_training_tool,
    ],
)
