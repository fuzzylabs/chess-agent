"""An MCP server for playing Chess with LiChess.

Aim:
# 1. Agent logs in with an API key
# 2. Agent is able to start a game
# 3. Agent is able to play the game by getting the current state and making moves.
"""

import os
from collections.abc import Callable
from typing import Any, Optional, cast

from berserk import Client, TokenSession, exceptions
from chess import Board
from core.exceptions import GameNotStartedError, MissingSessionStateError
from core.schemas import (
    AccountInfo,
    BoardRepresentation,
    CreatedGameAI,
    CreatedGamePerson,
    CurrentState,
    GameStateMsg,
    UIConfig,
)
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

load_dotenv()

mcp = FastMCP("chess-mcp", dependencies=["berserk", "python-chess"])

BOT_LEVEL = 3
LICHESS_ADDRESS = "https://lichess.org"
COLOR = "black"

SESSION_STATE = {}


def _is_value_in_session_state(value: str, msg: str) -> None:
    if value not in SESSION_STATE:
        raise MissingSessionStateError(f"{value} is not set. {msg}.")


def client_is_set_handler(func: Callable[[], Any]) -> Callable[[], Any]:
    """A decorator to check if the client is set."""

    def is_set_wrapper(*args: Any, **kwargs: dict[str, Any]) -> Any:
        _is_value_in_session_state("client", "You need to log in first.")
        return func(*args, **kwargs)

    return is_set_wrapper


def id_is_set_handler(func: Callable[[], Any]) -> Callable[[], Any]:
    """A decorator to check if the ID is set."""

    def is_set_wrapper(*args: Any, **kwargs: dict[str, Any]) -> Any:
        _is_value_in_session_state("id", "You need to start a game first.")
        return func(*args, **kwargs)

    return is_set_wrapper


@mcp.tool(description="Login to LiChess.")  # type: ignore
async def login() -> None:
    """Login to LiChess using the provided API key.

    Args:
        api_key: The API key to use for logging in.
    """
    api_key: Optional[str] = os.getenv("API_KEY")
    if not api_key:
        raise ValueError(
            "API_KEY not found in environment variables. Please set it in your .env"
        )
    session = TokenSession(api_key)
    SESSION_STATE["client"] = Client(session)


@client_is_set_handler
@mcp.tool(description="Get account info.")  # type: ignore
async def get_account_info() -> AccountInfo:
    """Get the account info of the logged in user."""
    return AccountInfo(**SESSION_STATE["client"].account.get())


@client_is_set_handler
@mcp.tool(description="Create a new game against an AI.")  # type: ignore
async def create_game_against_ai(level: int = BOT_LEVEL) -> UIConfig:
    """An endpoint for creating a new game."""
    response = CreatedGameAI(
        **SESSION_STATE["client"].challenges.create_ai(color=COLOR, level=level)
    )
    SESSION_STATE["id"] = response.id

    return UIConfig(url=f"{LICHESS_ADDRESS}/{response.id}")


@client_is_set_handler
@mcp.tool(description="Create a new game against a person.")  # type: ignore
async def create_game_against_person(username: str) -> UIConfig:
    """An endpoint for creating a new game."""
    response = CreatedGamePerson(
        **SESSION_STATE["client"].challenges.create(
            color=COLOR, username=username, rated=False
        )
    )
    SESSION_STATE["id"] = response.id

    return UIConfig(url=f"{LICHESS_ADDRESS}/{response.id}")


@client_is_set_handler
@mcp.tool(description="Whether the opponent had made there first move or not.")  # type: ignore
async def is_opponent_turn() -> GameStateMsg:
    """Whether the opponent had made there first move or not."""
    moves = await get_previous_moves()
    if isinstance(moves, str):
        raise GameNotStartedError()

    n_moves = len(moves)

    if n_moves % 2 == 0 or n_moves == 0:
        return GameStateMsg.OPPONENT_TURN
    else:
        return GameStateMsg.AGENT_TURN


@client_is_set_handler
@id_is_set_handler
@mcp.tool(description="End game.")  # type: ignore
async def end_game() -> None:
    """End the current game."""
    SESSION_STATE["client"].board.resign_game(SESSION_STATE["id"])


@client_is_set_handler
@id_is_set_handler
async def get_game_state() -> CurrentState:
    """Get the current game state."""
    return CurrentState(
        **next(SESSION_STATE["client"].board.stream_game_state(SESSION_STATE["id"]))
    )


@client_is_set_handler
@id_is_set_handler
@mcp.tool(description="Make a move.")  # type: ignore
async def make_move(move: str) -> None:
    """Make a move in the current game."""
    SESSION_STATE["client"].board.make_move(SESSION_STATE["id"], move)


async def get_previous_moves() -> list[str]:
    """Get all previous moves in the match."""
    try:
        current_state = await get_game_state()
    except exceptions.ResponseError:
        raise GameNotStartedError()
    return cast(list[str], current_state.state.moves.split())


async def get_board() -> str:
    """An endpoint for getting the current board as an ASCII representation."""
    moves = await get_previous_moves()

    board = Board()

    for move in moves:
        board.push_uci(move)

    return cast(str, board.__str__())


@mcp.tool(description="Get the current board as an ASCII representation.")  # type: ignore
async def get_board_representation() -> BoardRepresentation | GameStateMsg:
    """An endpoint for getting the current board as an ASCII representation."""
    board = await get_board()
    previous_moves = await get_previous_moves()

    return BoardRepresentation(board=board, previous_moves=previous_moves)
