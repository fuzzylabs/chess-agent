# Direct Execution

## Inspector Tool

Currently testing of endpoints can be performed with the following command:

```bash
uv run mcp dev server.py
```

This will start a local server running `Inspector` than can be used to interact with the MCP tools.

![inspector](docs/imgs/inspector.png)

## Under the hood

You can run the server directly with the following command:

```bash
uv run mcp run server.py --transport sse
```

> [!NOTE]
> This will start a local MCP server on port `8000`.

Setting `sse` allows us to communicate with the server via HTTP using the `Server-Sent Events` protocol. This is a one-way communication channel from the server to the client. The client can send messages to the server using the `POST` method, but the server can only send messages to the client using the `GET` method.

We can establish an MCP client by making a request to the `sse` endpoint of the server:

```bash
curl http://0.0.0.0:8000/sse
```

This will return an output of the form:

```
event: endpoint
data: /messages/?session_id=<session_id>
```

and then ping incrementally.

As per the MCP docmentation, a client-server lifecycle consists of three stages: connection, exchange, and termination.

> The lifecycle of an MCP connection involves three main stages:
>
> Initialization:
>
> The client sends an initialize request, including its protocol version and capabilities.
> The server responds with its protocol version and capabilities.
> The client sends an initialized notification to acknowledge.
> Normal message exchange begins.
> Message Exchange: After initialization, clients and servers can exchange messages using these patterns:
>
> Request-Response: The client sends a request, and the server responds.
> Notifications: Either side sends one-way messages (no response expected).
> Termination: The connection can be terminated in several ways:
>
> Clean shutdown via a close() method.
> Transport disconnection.
> Error conditions.

### Initialisation Requests

1. Send an initialisation request.

```bash
curl "http://0.0.0.0:8000/messages/?session_id=<session_id>" \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{
  "method": "initialize",
  "params": {
    "protocolVersion": "2024-11-05",
    "capabilities": {
      "sampling": {},
      "roots": {
        "listChanged":true
        }
      },
      "clientInfo": {
        "name": "mcp-inspector",
        "version": "0.8.0"
        }
      },
      "jsonrpc":"2.0",
      "id":0
    }
}'
```

2. Send an initialisation notification.

```bash
curl "http://0.0.0.0:8000/messages/?session_id=<session_id>" \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{
        "method": "notifications/initialized",
        "jsonrpc": "2.0"
    }'
```

Now the server and client are initialised and ready to exchange messages.

### Message Exchange

1. We can now start to interact with the server. Typically, the client might start by listing the tools.

```bash
curl "http://0.0.0.0:8000/messages/?session_id=<session_id>" \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{
        "method": "tools/list",
        "params": {},
        "jsonrpc": "2.0",
        "id": 1
    }'
```
