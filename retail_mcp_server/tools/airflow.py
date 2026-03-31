"""Retail MCP Server - Airflow tools."""

from typing import Any, Dict, Optional
from mcp.types import Tool

from ..api_client import api_client


async def airflow_trigger_dag(
    dag_id: str, conf: Optional[Dict[str, Any]] = None
) -> Any:
    """Trigger an Airflow DAG. POST /api/airflow/trigger-dag/ (Bearer)"""
    body: Dict[str, Any] = {"dag_id": dag_id}
    if conf:
        body["conf"] = conf

    return await api_client.request("POST", "/api/airflow/trigger-dag/", body=body)


# Tool definitions for MCP
AIRFLOW_TOOLS = [
    Tool(
        name="airflow_trigger_dag",
        description="Trigger an Airflow DAG — POST /api/airflow/trigger-dag/",
        inputSchema={
            "type": "object",
            "properties": {
                "dag_id": {"type": "string", "description": "DAG ID to trigger"},
                "conf": {
                    "type": "object",
                    "description": "Optional DAG run configuration",
                },
            },
            "required": ["dag_id"],
        },
    ),
]


# Mapping from tool name to handler function
AIRFLOW_HANDLERS = {
    "airflow_trigger_dag": airflow_trigger_dag,
}
