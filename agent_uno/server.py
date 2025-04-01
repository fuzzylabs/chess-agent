"""An MCP server for playing Chess with LiChess.

Aim:
# 1. Agent logs in with an API key
# 2. Agent is able to start a game
# 3. Agent is able to play the game by getting the current state and making moves.
"""

from berserk import Client, TokenSession  # type: ignore [import-not-found]
from mcp.server.fastmcp import FastMCP  # type: ignore [import-not-found]
from pydantic import BaseModel, Field


class AccountInfo(BaseModel):
    """The account info of a LiChess user."""

    id: str
    username: str
    perfs: dict[str, dict[str, int | bool]]
    created_at: str = Field(alias="createdAt")
    seen_at: str = Field(alias="seenAt")
    play_time: dict[str, int] = Field(alias="playTime")
    url: str
    count: dict[str, int]
    followable: bool
    following: bool
    blocking: bool


mcp = FastMCP("chess-mcp", dependencies=["berserk"])

session_state = {}


@mcp.tool(description="Login to LiChess.")  # type: ignore
async def login(api_key: str) -> None:
    """Login to LiChess using the provided API key.

    Args:
        api_key: The API key to use for logging in.
    """
    session = TokenSession(api_key)
    session_state["client"] = Client(session)


@mcp.tool(description="Get account info.")  # type: ignore
async def get_account_info() -> AccountInfo:
    """Get the account info of the logged in user."""
    return AccountInfo(**session_state["client"].account.get())
