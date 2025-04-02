"""MCP endpoint schemas."""

import datetime
from typing import Optional

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
    challenger: dict[str, Optional[str | int]]
    dest_user: dict[str, Optional[str | int]] = Field(alias="destUser")
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
    white: dict[str, int]
    black: dict[str, Optional[str | bool | int]]
    initial_fen: str = Field(alias="initialFen")
    type: str
    state: State
