from typing import Tuple, Any, Union
from modelcontextprotocol.sdk.client import Client
import json

async def call_tool(client: Client, tool_name: str, input_args: str) -> Tuple[Union[str, None], Union[Any, None]]:
    try:
        args = json.loads(input_args)
        resource_content = await client.call_tool(
            name=tool_name,
            arguments=args
        )
        return None, resource_content
    except Exception as error:
        return str(error), None