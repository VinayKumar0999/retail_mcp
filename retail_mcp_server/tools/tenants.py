"""Retail MCP Server - Tenant management tools."""

from typing import Any, Dict, Optional
from mcp.types import Tool

from ..api_client import api_client


async def tenant_onboard(**kwargs: Any) -> Any:
    """Onboard a new tenant. POST /tenants/onboard/ (Bearer)"""
    return await api_client.request("POST", "/tenants/onboard/", body=kwargs)


async def tenant_create_admin(**kwargs: Any) -> Any:
    """Create a tenant admin user. POST /tenants/create-admin/ (Bearer)"""
    return await api_client.request("POST", "/tenants/create-admin/", body=kwargs)


async def tenant_offboard(tenant_id: str, confirm: bool = False) -> Any:
    """Offboard (delete) a tenant. DELETE /tenants/offboarding/ (Bearer). Requires confirm=true."""
    if not confirm:
        return {
            "error": "confirm must be true to offboard a tenant. This is a destructive operation."
        }
    return await api_client.request(
        "DELETE", "/tenants/offboarding/", body={"tenant_id": tenant_id}
    )


# Tool definitions for MCP
TENANT_TOOLS = [
    Tool(
        name="tenant_onboard",
        description="Onboard a new tenant — POST /tenants/onboard/",
        inputSchema={
            "type": "object",
            "properties": {
                "name": {"type": "string", "description": "Tenant name"},
                "domain": {"type": "string", "description": "Tenant domain"},
                "email": {"type": "string", "description": "Tenant email (optional)"},
            },
            "required": ["name", "domain"],
        },
    ),
    Tool(
        name="tenant_create_admin",
        description="Create a tenant admin user — POST /tenants/create-admin/",
        inputSchema={
            "type": "object",
            "properties": {
                "username": {"type": "string", "description": "Admin username"},
                "password": {"type": "string", "description": "Admin password"},
                "email": {"type": "string", "description": "Admin email (optional)"},
            },
            "required": ["username", "password"],
        },
    ),
    Tool(
        name="tenant_offboard",
        description="Delete a tenant — DELETE /tenants/offboarding/ (**destructive**, requires `confirm: true`)",
        inputSchema={
            "type": "object",
            "properties": {
                "tenant_id": {"type": "string", "description": "Tenant ID to offboard"},
                "confirm": {
                    "type": "boolean",
                    "description": "Must be true to proceed with destructive operation",
                    "default": False,
                },
            },
            "required": ["tenant_id"],
        },
    ),
]


# Mapping from tool name to handler function
TENANT_HANDLERS = {
    "tenant_onboard": tenant_onboard,
    "tenant_create_admin": tenant_create_admin,
    "tenant_offboard": tenant_offboard,
}
