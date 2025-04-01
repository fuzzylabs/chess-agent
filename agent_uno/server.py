"""An MCP server for playing Chess with LiChess.

Aim:
# 1. Agent logs in with an API key
# 2. Agent is able to start a game
# 3. Agent is able to play the game by getting the current state and making moves.
"""

from collections.abc import Callable
from typing import Any, cast

from berserk import Client, TokenSession  # type: ignore [import-not-found]
from chess import Board  # type: ignore [import-not-found]
from mcp.server.fastmcp import FastMCP  # type: ignore [import-not-found]

from agent_uno.schemas import AccountInfo, CreatedGame, CurrentState

mcp = FastMCP("chess-mcp", dependencies=["berserk"])

session_state = {}


def client_is_set(func: Callable[[], Any]) -> Callable[[], Any]:
    """A decorator to check if the client is set."""

    def is_set_wrapper(*args: Any, **kwargs: dict[str, Any]) -> Any:
        if "client" not in session_state:
            raise Exception("Client is not set. You need to log in first.")
        return func(*args, **kwargs)

    return is_set_wrapper


def id_is_set(func: Callable[[], Any]) -> Callable[[], Any]:
    """A decorator to check if the ID is set."""

    def is_set_wrapper(*args: Any, **kwargs: dict[str, Any]) -> Any:
        if "id" not in session_state:
            raise Exception("ID is not set. You need to start a game first.")
        return func(*args, **kwargs)

    return is_set_wrapper


@mcp.tool(description="Login to LiChess.")  # type: ignore
async def login(api_key: str) -> None:
    """Login to LiChess using the provided API key.

    Args:
        api_key: The API key to use for logging in.
    """
    session = TokenSession(api_key)
    session_state["client"] = Client(session)


@client_is_set
@mcp.tool(description="Get account info.")  # type: ignore
async def get_account_info() -> AccountInfo:
    """Get the account info of the logged in user."""
    return AccountInfo(**session_state["client"].account.get())


@client_is_set
@mcp.tool(description="Create a new game.")  # type: ignore
async def create_game() -> str:
    """An endpoint for creating a new game."""
    response = CreatedGame(
        **session_state["client"].challenges.create_ai(color="black")
    )

    session_state["id"] = response.id

    return f"You can view the game taking place here: https://lichess-org.github.io/api-demo/#!/game/{response.id}"


@client_is_set
@id_is_set
@mcp.tool(description="End game.")  # type: ignore
async def end_game() -> None:
    """End the current game."""
    session_state["client"].board.resign_game(session_state["id"])


@client_is_set
@id_is_set
@mcp.tool(description="Get the current game state.")  # type: ignore
async def get_game_state() -> CurrentState:
    """Get the current game state."""
    return CurrentState(
        **next(session_state["client"].board.stream_game_state(session_state["id"]))
    )


@mcp.tool(description="Get all previous moves in the match.")  # type: ignore
async def get_previous_moves() -> list[str]:
    """Get all previous moves in the match."""
    current_state = await get_game_state()
    return cast(list[str], current_state.state.moves.split())


@client_is_set
@id_is_set
@mcp.tool(description="Make a move.")  # type: ignore
async def make_move(move: str) -> None:
    """Make a move in the current game."""
    session_state["client"].board.make_move(session_state["id"], move)


@mcp.tool(description="Get the current board.")  # type: ignore
async def get_board() -> str:
    """An endpoint for getting the current board as an ASCII representation."""
    board = Board()

    for move in await get_previous_moves():
        board.push_uci(move)

    return cast(str, board.__str__())
