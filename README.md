<h1 align="center">
    agent_uno &#128679;
</h1>

An LLM agent built using Model Context Protocol to play online games

# &#127939; How do I get started?
If you haven't already done so, please read [DEVELOPMENT.md](DEVELOPMENT.md) for instructions on how to set up your virtual environment using Poetry.

# Pre-requisites

- `uv` installable via brew.
- [Claude Desktop](https://claude.ai/download)
- Create [Lichess account](https://lichess.org/signup) and [API key](https://lichess.org/account/oauth/token).

Set up project:

```bash
make project-setup
```

# Quick Start

1. Install server in Claude Desktop:

```bash
uv run mcp install agent_uno/server.py
```

2. Interact with MCP server with Claude Desktop.

Example prompt:

```
Can you please log into the Chess API with the following API key ************ and then create a game. Once the game has been created the opponent will make the first move. Can you use the state to determine what an optimal next move will be and then make your own move playing continuously back and forth until completion? Please use the UCI chess standard for your moves, e.g., e2e4.
```
