from mcp import Client
from mcp import StdioClientTransport
from env import MCP_SERVER_ARGS, MCP_SERVER_COMMAND

transport = StdioClientTransport(
    command=MCP_SERVER_COMMAND,
    args=MCP_SERVER_ARGS
)

mcp_client = Client(
    {
        "name": "example-client",
        "version": "1.0.0"
    },
    {
        "capabilities": {}
    }
)

async def initialize_client():
    await mcp_client.connect(transport)
    return mcp_client