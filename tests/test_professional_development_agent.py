"""
Test suite for the Professional Development Agent using ADK evaluation framework.

This module contains automated tests for evaluating the agent's performance
across various scenarios including skill development, training search,
budget inquiries, and policy questions.
"""

import pytest
from google.adk.evaluation.agent_evaluator import AgentEvaluator


@pytest.mark.asyncio
async def test_improve_current_skills():
    await AgentEvaluator.evaluate(
        agent_module="google_adk_professional_development_agent",
        eval_dataset_file_path_or_dir="tests/improve_current_skills.test.json",
    )


@pytest.mark.asyncio
async def test_improve_future_skills():
    await AgentEvaluator.evaluate(
        agent_module="google_adk_professional_development_agent",
        eval_dataset_file_path_or_dir="tests/improve_future_skills.test.json",
    )


@pytest.mark.asyncio
async def test_question_without_email():
    await AgentEvaluator.evaluate(
        agent_module="google_adk_professional_development_agent",
        eval_dataset_file_path_or_dir="tests/question_without_email.test.json",
    )


@pytest.mark.asyncio
async def test_professional_development_policy_question():
    await AgentEvaluator.evaluate(
        agent_module="google_adk_professional_development_agent",
        eval_dataset_file_path_or_dir="tests/professional_development_policy_question.test.json",
    )
