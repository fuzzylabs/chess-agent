"""An MCP server for playing Chess with LiChess.

Aim:
# 1. Agent logs in with an API key
# 2. Agent is able to start a game
# 3. Agent is able to play the game by getting the current state and making moves.
"""

import datetime
from typing import cast

from berserk import Client, TokenSession  # type: ignore [import-not-found]
from mcp.server.fastmcp import FastMCP  # type: ignore [import-not-found]
from pydantic import BaseModel, Field


class AccountInfo(BaseModel):
    """The account info of a LiChess user."""

    id: str
    username: str
    perfs: dict[str, dict[str, int | bool]]
    created_at: datetime.datetime = Field(alias="createdAt")
    seen_at: datetime.datetime = Field(alias="seenAt")
    play_time: dict[str, int] = Field(alias="playTime")
    url: str
    count: dict[str, int]
    followable: bool
    following: bool
    blocking: bool


class CreatedGame(BaseModel):
    """The response of creating a new game."""

    id: str
    rated: bool
    variant: dict[str, str]
    fen: str
    turns: int
    source: str
    speed: str
    perf: str
    created_at: datetime.datetime = Field(alias="createdAt")
    status: dict[str, str | int]
    player: str
    full_id: str = Field(alias="fullId")


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


@mcp.tool(description="Create a new game.")  # type: ignore
async def create_game() -> str:
    """An endpoint for creating a new game."""
    response = CreatedGame(
        **session_state["client"].challenges.create_ai(color="black")
    )

    session_state["id"] = response.id

    return f"You can view the game taking place here: https://lichess-org.github.io/api-demo/#!/game/{response.id}"


@mcp.tool(description="End game.")  # type: ignore
async def end_game() -> None:
    """End the current game."""
    session_state["client"].board.resign_game(session_state["id"])


@mcp.tool(description="Get the current game state.")  # type: ignore
async def get_game_state() -> str:
    """Get the current game state."""
    current_state = next(
        session_state["client"].board.stream_game_state(session_state["id"])
    )
    return cast(str, current_state["state"]["moves"])


@mcp.tool(description="Make a move.")  # type: ignore
async def make_move(move: str) -> None:
    """Make a move in the current game."""
    session_state["client"].board.make_move(session_state["id"], move)
