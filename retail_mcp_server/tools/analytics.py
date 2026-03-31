"""Retail MCP Server - Analytics tools."""

from typing import Any, Dict, Optional
from mcp.types import Tool

from ..api_client import api_client


async def analytics_search_performance(
    client: str,
    range: str,
    start: Optional[str] = None,
    end: Optional[str] = None,
) -> Any:
    """Get search performance analytics. GET /analytics/search_performance/ (client header, range required)"""
    query_params: Dict[str, Any] = {"range": range}
    if start:
        query_params["start"] = start
    if end:
        query_params["end"] = end

    return await api_client.request(
        "GET",
        "/analytics/search_performance/",
        query=query_params,
        headers={"client": client},
        skip_auth=True,
    )


async def analytics_track_event(client: str, event: Dict[str, Any]) -> Any:
    """Track analytics event. POST /analytics/events/ (client header)"""
    return await api_client.request(
        "POST",
        "/analytics/events/",
        body=event,
        headers={"client": client},
        skip_auth=True,
    )


async def analytics_funnel_search(client: Optional[str] = None, **kwargs: Any) -> Any:
    """Get funnel search analytics. GET /analytics/funnel_search/ (Bearer + client)"""
    headers = {"client": client} if client else {}

    return await api_client.request(
        "GET", "/analytics/funnel_search/", query=kwargs, headers=headers
    )


# Tool definitions for MCP
ANALYTICS_TOOLS = [
    Tool(
        name="analytics_search_performance",
        description="Search performance report — GET /analytics/search_performance/",
        inputSchema={
            "type": "object",
            "properties": {
                "client": {"type": "string", "description": "Tenant domain"},
                "range": {
                    "type": "string",
                    "description": "Date range (e.g. last_7_days, last_30_days)",
                },
                "start": {"type": "string", "description": "Start date (ISO 8601)"},
                "end": {"type": "string", "description": "End date (ISO 8601)"},
            },
            "required": ["client", "range"],
        },
    ),
    Tool(
        name="analytics_track_event",
        description="Track an analytics event — POST /analytics/events/",
        inputSchema={
            "type": "object",
            "properties": {
                "client": {"type": "string", "description": "Tenant domain"},
                "event": {"type": "object", "description": "Event payload"},
            },
            "required": ["client", "event"],
        },
    ),
    Tool(
        name="analytics_funnel_search",
        description="Funnel search analytics — GET /analytics/funnel_search/",
        inputSchema={
            "type": "object",
            "properties": {
                "client": {"type": "string", "description": "Tenant domain override"}
            },
        },
    ),
]


# Mapping from tool name to handler function
ANALYTICS_HANDLERS = {
    "analytics_search_performance": analytics_search_performance,
    "analytics_track_event": analytics_track_event,
    "analytics_funnel_search": analytics_funnel_search,
}
