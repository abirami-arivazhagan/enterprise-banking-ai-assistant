import yaml


with open(
    "config/mcp_servers.yaml",
    "r"
) as file:

    MCP_CONFIG = yaml.safe_load(file)


def get_server_token(server_name):

    server = MCP_CONFIG[
        "servers"
    ].get(server_name)

    return server.get("token")