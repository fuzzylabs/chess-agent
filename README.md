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

2. Interact with MCP server with Claude Desktop.

:chess_pawn: Agent vs. Stockfish Bot :robot::

> Can you please log into the Chess API and then create a game against an AI. Once the game has been created the opponent will make the first move. Can you use the previous moves and the layout of the board to determine what an optimal next move will be and then make your own move playing continuously back and forth until completion? Please use the UCI chess standard for your moves, e.g., e2e4.

:chess_pawn: Agent vs. User :adult::

1. Ask agent to login and create a game against a user:

> Can you please log into the Chess API and then create a game against the user <insert user>.

2. Once the game has been created and the opponent has connected and made their first move, the agent will make their move.

> Once the game has been created the opponent will make the first move. Can you use the previous moves and the layout of the board to determine what an optimal next move will be and then make your own move playing continuously back and forth until completion? Please use the UCI chess standard for your moves, e.g., e2e4.

> [!NOTE]
> If you face issues with server starting in the Claude desktop this could be because of the relative path for the `command` in the server config. This will need to be changed to the absolute path to `uv` on your machine in this case. See [GH issue](https://github.com/cline/cline/issues/1160) for more details.
