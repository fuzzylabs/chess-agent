"""Top-level package for agent_uno."""  # noqa: N999

from typing import Literal

import click

from .server import mcp_server

Transport = Literal["stdio", "sse"]


@click.command()  # type: ignore
@click.option("--transport", default="stdio", help="The MCP transport type.")  # type: ignore
def main(transport: Transport) -> None:
    """Main function to run the MCP server."""
    mcp_server.run(transport=transport)


if __name__ == "__main__":
    main()
