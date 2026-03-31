"""Retail MCP Server - Search tools."""

import os
from typing import Any, Dict, Optional
from mcp.types import Tool

from ..api_client import api_client


async def search_query(
    q: str,
    client: str,
    secret_key: Optional[str] = None,
    page: Optional[int] = None,
    page_size: Optional[int] = None,
    **kwargs: Any,
) -> Any:
    """Search catalog. GET /api/search/ (requires client and X-SECRET-KEY headers)"""
    query_params: Dict[str, Any] = {"q": q}
    if page is not None:
        query_params["page"] = page
    if page_size is not None:
        query_params["page_size"] = page_size
    query_params.update(kwargs)

    headers = {"client": client}
    if secret_key:
        headers["X-SECRET-KEY"] = secret_key

    return await api_client.request(
        "GET", "/api/search/", query=query_params, headers=headers, skip_auth=True
    )


async def ai_agent_search(
    q: str, secret_key: Optional[str] = None, **kwargs: Any
) -> Any:
    """AI agent search. GET /ai/agent_search/ (requires X-Secret-key header)"""
    query_params: Dict[str, Any] = {"q": q}
    query_params.update(kwargs)

    effective_key = secret_key or api_client.secret_key
    headers = {"X-Secret-key": effective_key}

    return await api_client.request(
        "GET", "/ai/agent_search/", query=query_params, headers=headers, skip_auth=True
    )


async def ai_agent_suggestions(
    q: str, secret_key: Optional[str] = None, **kwargs: Any
) -> Any:
    """AI agent search suggestions. GET /ai/agent_suggestions/"""
    query_params: Dict[str, Any] = {"q": q}
    query_params.update(kwargs)

    effective_key = secret_key or api_client.secret_key
    headers = {"X-Secret-key": effective_key}

    return await api_client.request(
        "GET", "/ai/agent_suggestions/", query=query_params, headers=headers, skip_auth=True
    )


async def ai_purge(client: str, confirm: bool = False) -> Any:
    """Purge AI search cache. POST /ai/purge/ (Bearer + client). Requires confirm=true."""
    if not confirm:
        return {
            "error": "confirm must be true to purge cache. This is a destructive operation."
        }

    return await api_client.request("POST", "/ai/purge/", headers={"client": client})


# Tool definitions for MCP
SEARCH_TOOLS = [
    Tool(
        name="search_query",
        description="Full-text catalog search — GET /api/search/",
        inputSchema={
            "type": "object",
            "properties": {
                "q": {"type": "string", "description": "Search query"},
                "client": {"type": "string", "description": "Tenant domain"},
                "secret_key": {
                    "type": "string",
                    "description": "Secret key (overrides env SECRET_KEY)",
                },
                "page": {"type": "integer", "description": "Page number"},
                "page_size": {"type": "integer", "description": "Page size"},
            },
            "required": ["q", "client"],
        },
    ),
    Tool(
        name="ai_agent_search",
        description="AI-powered agent search — GET /ai/agent_search/",
        inputSchema={
            "type": "object",
            "properties": {
                "q": {"type": "string", "description": "Search query"},
                "secret_key": {
                    "type": "string",
                    "description": "Secret key (overrides env SECRET_KEY)",
                },
            },
            "required": ["q"],
        },
    ),
    Tool(
        name="ai_agent_suggestions",
        description="AI search suggestions — GET /ai/agent_suggestions/",
        inputSchema={
            "type": "object",
            "properties": {
                "q": {"type": "string", "description": "Partial query for suggestions"},
                "secret_key": {"type": "string", "description": "Secret key (optional)"},
            },
            "required": ["q"],
        },
    ),
    Tool(
        name="ai_purge",
        description="Purge AI search cache — POST /ai/purge/ (**destructive**, requires `confirm: true`)",
        inputSchema={
            "type": "object",
            "properties": {
                "client": {"type": "string", "description": "Tenant domain"},
                "confirm": {
                    "type": "boolean",
                    "description": "Must be true to proceed with destructive purge",
                    "default": False,
                },
            },
            "required": ["client"],
        },
    ),
]


# Mapping from tool name to handler function
SEARCH_HANDLERS = {
    "search_query": search_query,
    "ai_agent_search": ai_agent_search,
    "ai_agent_suggestions": ai_agent_suggestions,
    "ai_purge": ai_purge,
}
