"""Retail MCP Server - Main server implementation."""

import asyncio
import json
import logging
from typing import Any

from mcp.server import Server
from mcp.server.stdio import stdio_server

from .config import config
from .tools import ALL_TOOLS, ALL_HANDLERS

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("retail-mcp-server")


async def main():
    """Main entry point for the MCP server."""
    logger.info("Starting Retail MCP Server...")
    logger.info(f"Base URL: {config.base_url}")

    # Create MCP server
    server = Server("retail-mcp-server")

    @server.list_tools()
    async def list_tools() -> list[Any]:
        """List all available tools."""
        return ALL_TOOLS

    @server.call_tool()
    async def call_tool(name: str, arguments: dict[str, Any]) -> list[Any]:
        """Handle tool calls."""
        if name not in ALL_HANDLERS:
            raise ValueError(f"Unknown tool: {name}")

        try:
            # Get the handler for this tool
            tool_handler = ALL_HANDLERS[name]

            # Call the handler with the arguments
            result = await tool_handler(**arguments)

            # Return the result as MCP text content
            return [
                {
                    "type": "text",
                    "text": json.dumps(result, indent=2),
                }
            ]
        except Exception as e:
            logger.error(f"Error executing tool {name}: {e}", exc_info=True)
            return [
                {
                    "type": "text",
                    "text": f"Error: {str(e)}",
                }
            ]

    # Run the server using stdio transport
    async with stdio_server() as (read_stream, write_stream):
        logger.info("Server running with stdio transport")
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options(),
        )


def run():
    """Run the server."""
    asyncio.run(main())


if __name__ == "__main__":
    run()
