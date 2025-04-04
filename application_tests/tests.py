"""Application tests for the MCP Chess server."""

import time

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from mcp.types import TextContent

OKGREEN = "\033[92m"
ENDC = "\033[0m"

COMMAND = "python"
ARGS = ["agent_uno/server.py"]
SERVER_PARAMS = StdioServerParameters(
    command=COMMAND,
    args=ARGS,
    env=None,
)

EXPECTED_LIST_TOOLS_RESPONSE = [
    {
        "name": "login",
        "description": "Login to LiChess.",
        "inputSchema": {
            "properties": {},
            "title": "loginArguments",
            "type": "object",
        },
    },
    {
        "name": "get_account_info",
        "description": "Get account info.",
        "inputSchema": {
            "properties": {},
            "title": "get_account_infoArguments",
            "type": "object",
        },
    },
    {
        "name": "create_game_against_ai",
        "description": "Create a new game against an AI.",
        "inputSchema": {
            "properties": {
                "level": {"default": 3, "title": "Level", "type": "integer"}
            },
            "title": "create_game_against_aiArguments",
            "type": "object",
        },
    },
    {
        "name": "create_game_against_person",
        "description": "Create a new game against a person.",
        "inputSchema": {
            "properties": {"username": {"title": "Username", "type": "string"}},
            "required": ["username"],
            "title": "create_game_against_personArguments",
            "type": "object",
        },
    },
    {
        "name": "is_opponent_turn",
        "description": "Whether the opponent had made there first move or not.",
        "inputSchema": {
            "properties": {},
            "title": "is_opponent_turnArguments",
            "type": "object",
        },
    },
    {
        "name": "end_game",
        "description": "End game.",
        "inputSchema": {
            "properties": {},
            "title": "end_gameArguments",
            "type": "object",
        },
    },
    {
        "name": "make_move",
        "description": "Make a move.",
        "inputSchema": {
            "properties": {"move": {"title": "Move", "type": "string"}},
            "required": ["move"],
            "title": "make_moveArguments",
            "type": "object",
        },
    },
    {
        "name": "get_board_representation",
        "description": "Get the current board as an ASCII representation and all "
        "previous\n    moves.",
        "inputSchema": {
            "properties": {},
            "title": "get_board_representationArguments",
            "type": "object",
        },
    },
]

IS_OPPONENT_TURN_ERROR_RESPONSE = [
    TextContent(
        type="text",
        text="Error executing tool is_opponent_turn: id is not set. You need to start "
        "a game first..",
        annotations=None,
    )
]

IS_OPPONENT_TURN_RESPONSE = [
    TextContent(type="text", text="It is your turn to make a move.", annotations=None)
]


async def tests(session: ClientSession) -> None:
    """A function to test MCP server functionality."""
    # list the tools
    tools = await session.list_tools()
    assert [tool.__dict__ for tool in tools.tools] == EXPECTED_LIST_TOOLS_RESPONSE
    print(OKGREEN + "✓ List tools response is valid" + ENDC)

    # call the login tool
    response = await session.call_tool("login")
    assert response.isError is False
    print(OKGREEN + "✓ Login response is valid" + ENDC)

    # call the is_opponent_turn tool before a game starts
    response = await session.call_tool("is_opponent_turn")
    assert response.isError is True
    assert response.content == IS_OPPONENT_TURN_ERROR_RESPONSE
    print(OKGREEN + "✓ Is opponent turn response is valid" + ENDC)

    # call the create_game_against_ai tool
    response = await session.call_tool("create_game_against_ai")
    assert response.isError is False
    print(OKGREEN + "✓ Create game response is valid" + ENDC)

    # sleep to allow AI to move
    time.sleep(3)

    # call the is_opponent_turn tool after a game starts
    response = await session.call_tool("is_opponent_turn")
    assert response.isError is False
    assert response.content == IS_OPPONENT_TURN_RESPONSE
    print(OKGREEN + "✓ Is opponent turn response is valid" + ENDC)

    # call the get_board_representation tool
    response = await session.call_tool("get_board_representation")
    assert response.isError is False
    print(OKGREEN + "✓ Get board representation response is valid" + ENDC)

    # end the game
    response = await session.call_tool("end_game")
    assert response.isError is False
    print(OKGREEN + "✓ Successfully ended the game" + ENDC)


async def run() -> None:
    """A function to start a stdio server and run the tests."""
    async with (
        stdio_client(SERVER_PARAMS) as (read, write),
        ClientSession(read, write) as session,
    ):
        # Initialize the connection
        await session.initialize()

        await tests(session)


if __name__ == "__main__":
    import asyncio

    asyncio.run(run())
