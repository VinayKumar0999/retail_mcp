"""Retail MCP Server - Authentication tools."""

from typing import Any, Dict
from mcp.types import Tool

from ..api_client import api_client


async def auth_admin_login(username: str, password: str) -> Any:
    """Admin login (no client header). POST /tenants/login/"""
    return await api_client.request(
        "POST",
        "/tenants/login/",
        body={"username": username, "password": password},
        skip_auth=True,
        skip_default_headers=True,
    )


async def auth_tenant_login(username: str, password: str, client: str) -> Any:
    """Tenant login with client header. POST /tenants/login/"""
    return await api_client.request(
        "POST",
        "/tenants/login/",
        body={"username": username, "password": password},
        headers={"client": client},
        skip_auth=True,
    )


async def auth_refresh_token(refresh: str) -> Any:
    """Refresh access token. POST /api/auth/token/refresh/"""
    return await api_client.request(
        "POST",
        "/api/auth/token/refresh/",
        body={"refresh": refresh},
        skip_auth=True,
        skip_default_headers=True,
    )


async def auth_client_login(username: str, password: str, client: str) -> Any:
    """Client login with client header. POST /api/auth/login/"""
    return await api_client.request(
        "POST",
        "/api/auth/login/",
        body={"username": username, "password": password},
        headers={"client": client},
        skip_auth=True,
    )


# Tool definitions for MCP
AUTH_TOOLS = [
    Tool(
        name="auth_admin_login",
        description="Admin login — POST /tenants/login/ (no client header)",
        inputSchema={
            "type": "object",
            "properties": {
                "username": {"type": "string", "description": "Admin username"},
                "password": {"type": "string", "description": "Admin password"},
            },
            "required": ["username", "password"],
        },
    ),
    Tool(
        name="auth_tenant_login",
        description="Tenant login — POST /tenants/login/ (with client header)",
        inputSchema={
            "type": "object",
            "properties": {
                "username": {"type": "string", "description": "Username"},
                "password": {"type": "string", "description": "Password"},
                "client": {"type": "string", "description": "Tenant domain for the client header"},
            },
            "required": ["username", "password", "client"],
        },
    ),
    Tool(
        name="auth_refresh_token",
        description="Refresh JWT access token — POST /api/auth/token/refresh/",
        inputSchema={
            "type": "object",
            "properties": {
                "refresh": {"type": "string", "description": "Refresh token"},
            },
            "required": ["refresh"],
        },
    ),
    Tool(
        name="auth_client_login",
        description="Client login — POST /api/auth/login/ (with client header)",
        inputSchema={
            "type": "object",
            "properties": {
                "username": {"type": "string", "description": "Username"},
                "password": {"type": "string", "description": "Password"},
                "client": {"type": "string", "description": "Tenant domain for the client header"},
            },
            "required": ["username", "password", "client"],
        },
    ),
]


# Mapping from tool name to handler function
AUTH_HANDLERS = {
    "auth_admin_login": auth_admin_login,
    "auth_tenant_login": auth_tenant_login,
    "auth_refresh_token": auth_refresh_token,
    "auth_client_login": auth_client_login,
}
