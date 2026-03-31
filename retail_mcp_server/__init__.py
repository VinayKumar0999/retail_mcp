"""Retail MCP Server - Python implementation of retail backoffice APIs as MCP tools."""

__version__ = "1.0.0"

from .config import config
from .api_client import ApiClient, api_client

__all__ = ["config", "ApiClient", "api_client"]
