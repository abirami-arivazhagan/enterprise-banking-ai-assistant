import yaml


class MCPRegistry:

    def __init__(
        self,
        config_path="config/mcp_servers.yaml"
    ):

        self.config_path = config_path

        self.config = self._load_config()

    def _load_config(self):

        with open(
            self.config_path,
            "r"
        ) as file:

            return yaml.safe_load(file) or {}

    def list_tools(self):

        return self.config.get(
            "servers",
            {}
        )

    def get_server(
        self,
        name
    ):

        return (
            self.config
            .get(
                "servers",
                {}
            )
            .get(name)
        )
