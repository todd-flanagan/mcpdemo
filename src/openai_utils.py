from typing import List, Dict, Any, TypedDict
from openai.types.chat import ChatCompletion
from messages import MessageType
from mcptool import call_tool
from client import mcp_client

class OpenAiToolsInput(TypedDict):
    type: str
    function: Dict[str, Any]

class ToolsListServerResponse(TypedDict):
    tools: List[Dict[str, Any]]

def map_tool_list_to_openai_tools(tool_list: ToolsListServerResponse) -> List[OpenAiToolsInput]:
    return [
        {
            "type": "function",
            "function": {
                "name": tool["name"],
                "description": tool.get("description"),
                "parameters": tool["inputSchema"]
            }
        }
        for tool in tool_list["tools"]
    ]

async def apply_tool_calls_if_present(response: ChatCompletion) -> List[MessageType]:
    if not response.choices[0].message.tool_calls:
        return []

    tool_call_results: List[MessageType] = []
    
    for tool_call in response.choices[0].message.tool_calls:
        tool_call_id = tool_call.id
        name = tool_call.function.name
        args = tool_call.function.arguments
        
        err, result = await call_tool(mcp_client, name, args)
        
        if err:
            tool_call_results.append({
                "role": "tool",
                "content": f"ERROR: Tool call failed - {err}",
                "tool_call_id": tool_call_id
            })
            continue
            
        if not result.get("content"):
            tool_call_results.append({
                "role": "tool",
                "content": "WARNING: No content returned from tool",
                "tool_call_id": tool_call_id
            })
            continue
            
        content = result["content"][0]
        if content["type"] == "text":
            tool_call_results.append({
                "role": "tool",
                "content": content["text"],
                "tool_call_id": tool_call_id
            })
        else:
            raise ValueError(f"Unknown content type returned from tool: {content}")
            
    return tool_call_results

def is_done(response: ChatCompletion) -> bool:
    if not response.choices:
        raise ValueError("No choices found in response")
    return response.choices[0].finish_reason == "stop"