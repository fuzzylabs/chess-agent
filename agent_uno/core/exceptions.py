"""Exceptions for the MCP server."""

from .schemas import GameStateMsg


class GameNotStartedError(Exception):
    """The game has not been started yet."""

    def __init__(self) -> None:
        """The constructor for the GameNotStartedError exception."""
        super().__init__(GameStateMsg.NOT_STARTED)


class MissingSessionStateError(Exception):
    """The session state is missing."""

    def __init__(self, message: str) -> None:
        """The constructor for the MissingSessionStateError exception."""
        self.message = message
        super().__init__(self.message)
