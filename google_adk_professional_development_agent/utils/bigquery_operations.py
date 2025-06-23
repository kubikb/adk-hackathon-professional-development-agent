"""
BigQuery Operations Utility Module.

This module provides a set of utility functions for interacting with Google BigQuery,
specifically tailored for the professional development system's data needs. It handles
common operations like querying employee profiles, training history, and project data.

The module uses the Google Cloud BigQuery client library and provides error handling
and logging for all database operations.

Functions:
    query_single_row: Execute a query expecting a single row result
    query_multiple_rows: Execute a query expecting multiple row results
    insert_json_row: Insert a new row of JSON data into a specified table

Example:
    ```python
    from utils.bigquery_operations import query_single_row, query_multiple_rows

    # Query a single employee profile
    profile = query_single_row(
        "SELECT * FROM `project.dataset.employee_profiles` WHERE email = @email",
        [{"name": "email", "value": "john.doe@example.com"}]
    )

    # Query all training records
    trainings = query_multiple_rows(
        "SELECT * FROM `project.dataset.employee_trainings`"
    )
    ```
"""

import logging
import io
import json
from typing import List, Dict, Any, Optional

from google.cloud import bigquery
from ..config import config

# Instead of directly querying the BigQuery table, we could use MCP Toolbox for Databases.
# Sample for BigQuery here: https://googleapis.github.io/genai-toolbox/samples/bigquery/mcp_quickstart/

# Initialize BigQuery client
_client = bigquery.Client(project=config.google_cloud_project)
_project_id = _client.project
_dataset_id = config.bigquery_dataset_id


def get_table_ref(table_id: str) -> str:
    """Get fully qualified BigQuery table reference.

    Args:
        table_id (str): The ID of the table without project and dataset

    Returns:
        str: Fully qualified table reference in format 'project.dataset.table'
    """
    return f"{_project_id}.{_dataset_id}.{table_id}"


def query_single_row(
    query: str, params: Optional[List[Dict[str, Any]]] = None
) -> Optional[Dict[str, Any]]:
    """Execute a BigQuery query expecting a single row result.

    This function is optimized for queries that should return exactly one row,
    such as looking up an employee profile by email.

    Args:
        query (str): The SQL query to execute
        params (List[Dict[str, Any]], optional): Query parameters for safe SQL execution

    Returns:
        Optional[Dict[str, Any]]: The first row as a dictionary, or None if no results

    Raises:
        Exception: If the query execution fails
    """
    try:
        job_config = bigquery.QueryJobConfig(query_parameters=params or [])
        query_job = _client.query(query, job_config=job_config)
        results = query_job.result()
        row = next(iter(results), None)
        return dict(row) if row else None
    except Exception as e:
        logging.error(f"Error executing single row query: {str(e)}")
        raise


def query_multiple_rows(
    query: str, params: Optional[List[Dict[str, Any]]] = None
) -> List[Dict[str, Any]]:
    """Execute a BigQuery query expecting multiple row results.

    This function is designed for queries that return multiple rows,
    such as fetching training history or project portfolio data.

    Args:
        query (str): The SQL query to execute
        params (List[Dict[str, Any]], optional): Query parameters for safe SQL execution

    Returns:
        List[Dict[str, Any]]: List of rows as dictionaries

    Raises:
        Exception: If the query execution fails
    """
    try:
        job_config = bigquery.QueryJobConfig(query_parameters=params or [])
        query_job = _client.query(query, job_config=job_config)
        results = query_job.result()
        return [dict(row) for row in results]
    except Exception as e:
        logging.error(f"Error executing multiple row query: {str(e)}")
        raise


def insert_json_row(table_id: str, row_data: Dict[str, Any]) -> None:
    """Insert a single row of JSON data into a BigQuery table.

    This function handles the insertion of new records, such as registering
    new training entries or updating employee profiles.

    Args:
        table_id (str): The ID of the target table without project and dataset
        row_data (Dict[str, Any]): The data to insert as a dictionary

    Raises:
        Exception: If the insert operation fails
    """
    try:
        json_data = io.StringIO(json.dumps(row_data) + "\n")

        job_config = bigquery.LoadJobConfig(
            source_format=bigquery.SourceFormat.NEWLINE_DELIMITED_JSON,
            write_disposition=bigquery.WriteDisposition.WRITE_APPEND,
        )

        load_job = _client.load_table_from_file(
            json_data, get_table_ref(table_id), job_config=job_config
        )
        load_job.result()
    except Exception as e:
        logging.error(f"Error inserting row: {str(e)}")
        raise
