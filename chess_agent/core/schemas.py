"""MCP endpoint schemas."""

import datetime
from enum import StrEnum

from pydantic import BaseModel, Field

PlayerInfo = dict[str, int | str | bool | None]


GAME_EXPLANATION = """You are the Black side in every game, meaning that you will always
control the black pieces. The chessboard is represented in ASCII format, and here’s
how you should understand it:

Uppercase letters represent white pieces:
'K' = White King
'Q' = White Queen
'R' = White Rook
'N' = White Knight
'B' = White Bishop
'P' = White Pawn

Lowercase letters represent black pieces (your pieces):
'k' = Black King
'q' = Black Queen
'r' = Black Rook
'n' = Black Knight
'b' = Black Bishop
'p' = Black Pawn

Empty squares are represented by a dot '.' or a number indicating the count of
consecutive empty squares in that rank. For example, a series of dots (e.g., ...)
means there are empty squares in those positions.
Board Layout:

The chessboard is structured in ranks (1 to 8) and files (a to h). The ranks
represent horizontal rows, with rank 1 at the bottom (white side) and rank 8 at the
top (black side). The files represent vertical columns, labelled from 'a' to 'h'
from left to right.

Here is an example of an initial game state:

  a b c d e f g h
8 r n b q k b n r
7 p p p p p p p p
6 . . . . . . . .
5 . . . . . . . .
4 . . . . . . . .
3 . . . . . . . .
2 P P P P P P P P
1 R N B Q K B N R

Black pieces (your pieces) are located on ranks 7 and 8.
White pieces are located on ranks 1 and 2.

The game is set up such that pawns are in front, and other pieces (rooks, knights,
bishops, queens, and kings) are placed behind the pawns.

Your Role:
As the Black player, you will be making moves using the lowercase pieces
('r', 'n', 'b', 'q', 'k', 'p'). If you are currently in check, you must make to
protect your king, no other moves will be valid.

Summary of the Board:
The agent (you) will always play as Black.
White's pieces are uppercase letters, and your pieces (Black) are lowercase.
The game begins with pieces in their starting positions, and your task is to move
your pieces strategically to win the game."""


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


class CreatedGameAI(BaseModel):
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


class CreatedGamePerson(BaseModel):
    """The response of creating a new game."""

    id: str
    url: str
    status: str
    challenger: dict[str, str | int | None]
    dest_user: dict[str, str | int | None] = Field(alias="destUser")
    variant: dict[str, str]
    time_control: dict[str, str] = Field(alias="timeControl")
    color: str
    final_color: str = Field(alias="finalColor")
    perf: dict[str, str]
    direction: str


class UIConfig(BaseModel):
    """The UI configuration of a game."""

    url: str


class State(BaseModel):
    """A representation of the game state."""

    type: str
    moves: str
    wtime: datetime.datetime
    btime: datetime.datetime
    winc: int
    binc: int
    status: str


class CurrentState(BaseModel):
    """The current state of a game."""

    id: str
    variant: dict[str, str]
    speed: str
    perf: dict[str, str]
    rated: bool
    created_at: datetime.datetime = Field(alias="createdAt")
    white: PlayerInfo
    black: PlayerInfo
    initial_fen: str = Field(alias="initialFen")
    type: str
    state: State


class BoardRepresentation(BaseModel):
    """The board representation of the game."""

    explanation: str = Field(default=GAME_EXPLANATION)
    board: str
    previous_moves: list[str]
    check: bool


class GameStateMsg(StrEnum):
    """Messages for the game state, e.g., whose turn it is."""

    NOT_STARTED = """The game has not started yet please wait until the game has
    started."""
    AGENT_TURN = "It is your turn to make a move."
    OPPONENT_TURN = "It is the opponent's turn. Please wait for them to make a move."
