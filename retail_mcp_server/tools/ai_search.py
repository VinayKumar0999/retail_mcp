"""Retail MCP Server - AI Search tools."""

from typing import Any, Dict, Optional
from mcp.types import Tool

from ..api_client import api_client


async def ai_search(q: str, client: Optional[str] = None, **kwargs: Any) -> Any:
    """AI-powered search. GET /api/ai/ai_search/ (Bearer + client)"""
    query_params: Dict[str, Any] = {"q": q}
    query_params.update(kwargs)

    headers = {"client": client} if client else {}

    return await api_client.request(
        "GET", "/api/ai/ai_search/", query=query_params, headers=headers
    )


# Tool definitions for MCP
AI_SEARCH_TOOLS = [
    Tool(
        name="ai_search",
        description="AI-powered search — GET /api/ai/ai_search/",
        inputSchema={
            "type": "object",
            "properties": {
                "q": {"type": "string", "description": "Search query"},
                "client": {"type": "string", "description": "Tenant domain override"},
            },
            "required": ["q"],
        },
    ),
]


# Mapping from tool name to handler function
AI_SEARCH_HANDLERS = {
    "ai_search": ai_search,
}
