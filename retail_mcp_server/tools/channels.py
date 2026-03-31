"""Retail MCP Server - Channel tools."""

import os
from typing import Any, Dict, Optional
from mcp.types import Tool

from ..api_client import api_client


async def channels_search(
    q: str, client: str, secret_key: Optional[str] = None, **kwargs: Any
) -> Any:
    """Search channels. GET /api/channels/search/ (requires client and X-SECRET-KEY headers)"""
    effective_secret_key = secret_key or os.getenv("SECRET_KEY")
    if not effective_secret_key:
        raise ValueError(
            "channels_search requires a secret key: provide 'secret_key' in the tool arguments "
            "or set the SECRET_KEY environment variable."
        )

    query_params: Dict[str, Any] = {"q": q}
    query_params.update(kwargs)

    headers = {"client": client, "X-SECRET-KEY": effective_secret_key}

    return await api_client.request(
        "GET", "/api/channels/search/", query=query_params, headers=headers, skip_auth=True
    )


async def channels_brands() -> Any:
    """Get channel brands. GET /api/channels/brands/ (Bearer)"""
    return await api_client.request("GET", "/api/channels/brands/")


async def channels_synonyms() -> Any:
    """Get channel synonyms. GET /api/channels/synonyms/ (Bearer)"""
    return await api_client.request("GET", "/api/channels/synonyms/")


# Tool definitions for MCP
CHANNEL_TOOLS = [
    Tool(
        name="channels_search",
        description="Search channels — GET /api/channels/search/",
        inputSchema={
            "type": "object",
            "properties": {
                "q": {"type": "string", "description": "Search query"},
                "client": {"type": "string", "description": "Tenant domain"},
                "secret_key": {"type": "string", "description": "Secret key override"},
            },
            "required": ["q", "client"],
        },
    ),
    Tool(
        name="channels_brands",
        description="Get channel brands — GET /api/channels/brands/",
        inputSchema={"type": "object", "properties": {}},
    ),
    Tool(
        name="channels_synonyms",
        description="Get channel synonyms — GET /api/channels/synonyms/",
        inputSchema={"type": "object", "properties": {}},
    ),
]


# Mapping from tool name to handler function
CHANNEL_HANDLERS = {
    "channels_search": channels_search,
    "channels_brands": channels_brands,
    "channels_synonyms": channels_synonyms,
}
