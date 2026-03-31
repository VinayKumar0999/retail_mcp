"""Retail MCP Server - HTTP API client for retail backoffice APIs."""

import base64
from typing import Any, Dict, Optional, Union
from urllib.parse import urljoin

import httpx

from .config import Config, config as app_config


class ApiClient:
    """HTTP client for interacting with retail backoffice APIs.

    Automatically handles:
    - JWT Bearer token authentication
    - Automatic token refresh on 401 errors
    - Tenant domain (client) header injection
    - Secret key (X-SECRET-KEY) header injection
    - Multipart file uploads
    """

    def __init__(self, cfg: Config):
        """Initialize API client with configuration.

        Args:
            cfg: Application configuration containing API credentials and base URL
        """
        self.base_url = cfg.base_url
        self.access_token = cfg.access_token
        self.refresh_token = cfg.refresh_token
        self.tenant_domain = cfg.tenant_domain
        self.secret_key = cfg.secret_key
        self._client = httpx.AsyncClient(timeout=30.0)

    async def request(
        self,
        method: str,
        path: str,
        *,
        body: Optional[Dict[str, Any]] = None,
        query: Optional[Dict[str, Union[str, int, bool]]] = None,
        headers: Optional[Dict[str, str]] = None,
        multipart: Optional[Dict[str, Union[str, bytes, tuple[bytes, str]]]] = None,
        skip_auth: bool = False,
        skip_default_headers: bool = False,
    ) -> Any:
        """Make an HTTP request to the retail API.

        Args:
            method: HTTP method (GET, POST, PUT, DELETE, etc.)
            path: API endpoint path
            body: JSON request body
            query: URL query parameters
            headers: Additional HTTP headers
            multipart: Multipart form data (for file uploads)
            skip_auth: Skip Bearer token authentication
            skip_default_headers: Skip automatic client and secret key headers

        Returns:
            Response data (typically JSON decoded)

        Raises:
            httpx.HTTPStatusError: For HTTP errors
        """
        url = urljoin(self.base_url, path)

        # Build headers
        req_headers: Dict[str, str] = {**(headers or {})}

        # Add authentication
        if self.access_token and not skip_auth:
            req_headers["Authorization"] = f"Bearer {self.access_token}"

        # Add default headers
        if not skip_default_headers:
            if self.tenant_domain and "client" not in req_headers:
                req_headers["client"] = self.tenant_domain
            if self.secret_key and "X-SECRET-KEY" not in req_headers and "X-Secret-key" not in req_headers:
                req_headers["X-SECRET-KEY"] = self.secret_key

        # Build request kwargs
        kwargs: Dict[str, Any] = {
            "method": method,
            "url": url,
            "headers": req_headers,
        }

        if query:
            kwargs["params"] = {k: v for k, v in query.items() if v is not None}

        if multipart:
            # Handle multipart file uploads
            files = {}
            data = {}
            for key, value in multipart.items():
                if isinstance(value, tuple):
                    # (file_data, filename)
                    files[key] = (value[1], value[0])
                elif isinstance(value, bytes):
                    files[key] = (key, value)
                else:
                    data[key] = value
            kwargs["files"] = files
            if data:
                kwargs["data"] = data
        elif body:
            kwargs["json"] = body

        try:
            response = await self._client.request(**kwargs)
            response.raise_for_status()

            # Try to return JSON, fall back to text
            try:
                return response.json()
            except Exception:
                return response.text

        except httpx.HTTPStatusError as err:
            # Auto-refresh token on 401
            if (
                err.response.status_code == 401
                and self.refresh_token
                and not skip_auth
            ):
                # Refresh the access token
                refresh_url = urljoin(self.base_url, "/api/auth/token/refresh/")
                refresh_resp = await self._client.post(
                    refresh_url,
                    json={"refresh": self.refresh_token},
                )
                refresh_resp.raise_for_status()
                refresh_data = refresh_resp.json()
                self.access_token = refresh_data["access"]

                # Retry with new token
                req_headers["Authorization"] = f"Bearer {self.access_token}"
                kwargs["headers"] = req_headers
                retry_response = await self._client.request(**kwargs)
                retry_response.raise_for_status()

                try:
                    return retry_response.json()
                except Exception:
                    return retry_response.text

            # Re-raise if not handled
            raise Exception(
                f"API error {err.response.status_code}: {err.response.text}"
            ) from err

    async def close(self) -> None:
        """Close the HTTP client connection pool."""
        await self._client.aclose()


# Global API client instance
api_client = ApiClient(app_config)
