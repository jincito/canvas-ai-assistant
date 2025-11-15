#!/usr/bin/env python3
"""
Entry point for Canvas AI Assistant MCP Server.

This script starts the MCP server that can be connected to by
MCP-compatible clients like Claude Desktop.
"""

import asyncio
from mcp_server.mcp_app import main
import sys
import os

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


if __name__ == "__main__":
    asyncio.run(main())
