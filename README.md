<h1 align="center">
    agent_uno &#128679;
</h1>

An LLM agent built using Model Context Protocol to play online games

# &#127939; How do I get started?
If you haven't already done so, please read [DEVELOPMENT.md](DEVELOPMENT.md) for instructions on how to set up your virtual environment using Poetry.

# Pre-requisites

- `uv` installable via brew.
- [Claude Desktop](https://claude.ai/download)

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
