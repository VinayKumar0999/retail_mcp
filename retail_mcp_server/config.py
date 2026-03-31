"""Retail MCP Server - Configuration management."""

import os
from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    """Application configuration loaded from environment variables."""

    base_url: str = "http://172.168.168.36:8006"
    access_token: str = ""
    refresh_token: str = ""
    tenant_domain: str = ""
    secret_key: str = ""
    port: int = 3000

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


# Global configuration instance
config = Config()
