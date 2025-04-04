"""Top-level package for agent_uno."""  # noqa: N999

from .server import mcp_server


def main() -> None:
    """Main function to run the MCP server."""
    mcp_server.run()


if __name__ == "__main__":
    main()
