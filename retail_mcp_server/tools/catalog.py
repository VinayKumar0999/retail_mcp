"""Retail MCP Server - Catalog tools."""

import base64
from typing import Any, Dict, List, Optional
from mcp.types import Tool

from ..api_client import api_client


async def catalog_settings_bulk_create(settings: List[Dict[str, Any]]) -> Any:
    """Bulk create catalog settings. POST /api/catalog/settings/bulk-create/ (Bearer)"""
    return await api_client.request(
        "POST", "/api/catalog/settings/bulk-create/", body={"settings": settings}
    )


async def catalog_settings_active_fields(client: Optional[str] = None) -> Any:
    """Get active catalog settings fields. GET /api/catalog/settings/fields/active/ (Bearer)"""
    headers = {"client": client} if client else {}
    return await api_client.request(
        "GET", "/api/catalog/settings/fields/active/", headers=headers
    )


async def catalog_settings_search_fields_active() -> Any:
    """Get active search fields. GET /api/catalog/settings/search-fields/active/ (Bearer)"""
    return await api_client.request("GET", "/api/catalog/settings/search-fields/active/")


async def catalog_settings_create_search_fields(fields: List[Dict[str, Any]]) -> Any:
    """Create search field settings. POST /api/catalog/settings/search-fields/ (Bearer)"""
    return await api_client.request(
        "POST", "/api/catalog/settings/search-fields/", body={"fields": fields}
    )


async def catalog_sync_status() -> Any:
    """Get catalog sync status. GET /api/catalog/sync/ (Bearer)"""
    return await api_client.request("GET", "/api/catalog/sync/")


async def catalog_sync_trigger(**kwargs: Any) -> Any:
    """Trigger a catalog sync. POST /api/catalog/sync/ (Bearer)"""
    return await api_client.request("POST", "/api/catalog/sync/", body=kwargs)


async def catalog_upload(
    file_base64: Optional[str] = None,
    file_url: Optional[str] = None,
    filename: str = "catalog.csv",
) -> Any:
    """Upload catalog file. POST /tenants/catalog/upload/ (multipart).
    Provide file as base64 string or a URL.
    """
    if not file_base64 and not file_url:
        raise ValueError("Provide either file_base64 or file_url")

    if file_base64:
        file_buffer = base64.b64decode(file_base64)
    elif file_url:
        import httpx

        async with httpx.AsyncClient() as client:
            resp = await client.get(file_url)
            resp.raise_for_status()
            file_buffer = resp.content
    else:
        raise ValueError("file_base64 or file_url required")

    return await api_client.request(
        "POST",
        "/tenants/catalog/upload/",
        multipart={"file": (file_buffer, filename)},
    )


# Tool definitions for MCP
CATALOG_TOOLS = [
    Tool(
        name="catalog_settings_bulk_create",
        description="Bulk create catalog settings — POST /api/catalog/settings/bulk-create/",
        inputSchema={
            "type": "object",
            "properties": {
                "settings": {
                    "type": "array",
                    "description": "Array of catalog setting objects",
                    "items": {"type": "object"},
                }
            },
            "required": ["settings"],
        },
    ),
    Tool(
        name="catalog_settings_active_fields",
        description="Get active catalog fields — GET /api/catalog/settings/fields/active/",
        inputSchema={
            "type": "object",
            "properties": {
                "client": {
                    "type": "string",
                    "description": "Tenant domain (optional client header override)",
                }
            },
        },
    ),
    Tool(
        name="catalog_settings_search_fields_active",
        description="Get active search fields — GET /api/catalog/settings/search-fields/active/",
        inputSchema={"type": "object", "properties": {}},
    ),
    Tool(
        name="catalog_settings_create_search_fields",
        description="Create search fields — POST /api/catalog/settings/search-fields/",
        inputSchema={
            "type": "object",
            "properties": {
                "fields": {
                    "type": "array",
                    "description": "Array of search field objects",
                    "items": {"type": "object"},
                }
            },
            "required": ["fields"],
        },
    ),
    Tool(
        name="catalog_sync_status",
        description="Get catalog sync status — GET /api/catalog/sync/",
        inputSchema={"type": "object", "properties": {}},
    ),
    Tool(
        name="catalog_sync_trigger",
        description="Trigger a catalog sync — POST /api/catalog/sync/",
        inputSchema={
            "type": "object",
            "properties": {
                "full_sync": {"type": "boolean", "description": "Trigger a full sync"}
            },
        },
    ),
    Tool(
        name="catalog_upload",
        description="Upload catalog file (multipart) — POST /tenants/catalog/upload/",
        inputSchema={
            "type": "object",
            "properties": {
                "file_base64": {
                    "type": "string",
                    "description": "Base64-encoded file content",
                },
                "file_url": {"type": "string", "description": "URL to download the file from"},
                "filename": {"type": "string", "description": "Filename for the upload"},
            },
        },
    ),
]


# Mapping from tool name to handler function
CATALOG_HANDLERS = {
    "catalog_settings_bulk_create": catalog_settings_bulk_create,
    "catalog_settings_active_fields": catalog_settings_active_fields,
    "catalog_settings_search_fields_active": catalog_settings_search_fields_active,
    "catalog_settings_create_search_fields": catalog_settings_create_search_fields,
    "catalog_sync_status": catalog_sync_status,
    "catalog_sync_trigger": catalog_sync_trigger,
    "catalog_upload": catalog_upload,
}
