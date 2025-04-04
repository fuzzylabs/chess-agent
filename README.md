<h1 align="center">
    Agent Uno :chess_pawn:
</h1>

An LLM agent built using Model Context Protocol to play online games

# Pre-requisites

- `uv` installable via brew.
- [Claude Desktop](https://claude.ai/download)
- Create [Lichess account](https://lichess.org/signup)
- Create [API key](https://lichess.org/account/oauth/token).
- Add API key to a `.env` file in the projects root directory: `API_KEY = ************`
> [!NOTE]
> When creating an API key only the `board:play` scope is required.
>
> ![create-api-key.png](docs/imgs/create-api-key.png)

Set up project:

```bash
make project-setup
```

# Quick Start

1. Install server in Claude Desktop:

```bash
cd agent_uno
```

```bash
uv run mcp install server.py
```

> [!NOTE]
> If you have Claude Desktop open when you run the above command, you will need to restart it for the server to be available.

> [!WARNING]
> Common Issues:
> 1. `ENOENT` error when opening Claude Desktop.
>   - This is due to Claude Desktop facing issues with running the server with a relative path to `uv`. To fix this, you need to change the `command` in the `claude_desktop_config.json` config to an absolute path. You can find the absolute path by running `which uv` in your terminal.
> 2. Not having `coreutils` installed.
>  - This is required for the `realpath` command. You will see the following error in Claude logs: `realpath: command not found`. You can install it using `brew install coreutils`.

2. Interact with MCP server with Claude Desktop.

:chess_pawn: Agent vs. Stockfish Bot :robot::

> Can you please log into the Chess API and then create a game against an AI. Once the game has been created the opponent will make the first move. Can you use the previous moves and the layout of the board to determine what an optimal next move will be and then make your own move playing continuously back and forth until completion? Please use the UCI chess standard for your moves, e.g., e2e4.

:chess_pawn: Agent vs. User :adult::

1. Ask agent to login and create a game against a user:

> Can you please log into the Chess API and then create a game against the user <insert user>.

2. Once the game has been created and the opponent has connected and made their first move, the agent will make their move.

> Once the game has been created the opponent will make the first move. Can you use the previous moves and the layout of the board to determine what an optimal next move will be and then make your own move playing continuously back and forth until completion? Please use the UCI chess standard for your moves, e.g., e2e4.
