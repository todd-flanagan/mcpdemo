from mcp import ClientSession, StdioServerParameters, types
from mcp.client.stdio import stdio_client
from env import MCP_SERVER_ARGS, MCP_SERVER_COMMAND

transport = StdioServerParameters(
    command=MCP_SERVER_COMMAND,
    args=MCP_SERVER_ARGS
)

async def handle_sampling_message(
    message: types.CreateMessageRequestParams,
) -> types.CreateMessageResult:
    return types.CreateMessageResult(
        role="assistant",
        content=types.TextContent(
            type="text",
            text="Hello, world! from model",
        ),
        model="gpt-3.5-turbo",
        stopReason="endTurn",
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