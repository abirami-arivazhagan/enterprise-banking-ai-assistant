import requests

from mcp.registry import (
    MCPRegistry
)


class MCPToolAdapter:

    def __init__(
        self,
        registry=None
    ):

        self.registry = registry or MCPRegistry()

    def execute(
        self,
        server_name,
        tool_name,
        params
    ):

        server = self.registry.get_server(
            server_name
        )

        if server is None:

            return {
                "error":
                f"MCP server not found: {server_name}"
            }

        url = (
            f"{server['url'].rstrip('/')}"
            f"/tools/{tool_name}"
        )

        headers = {
            "Authorization":
            f"Bearer {server.get('token', '')}"
        }

        response = requests.post(
            url,
            json=params,
            headers=headers,
            timeout=30
        )

        response.raise_for_status()

        return response.json()
