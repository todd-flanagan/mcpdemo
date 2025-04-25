from openai import OpenAI
from client import mcp_client, initialize_client
from openai_utils import apply_tool_calls_if_present, is_done, map_tool_list_to_openai_tools
from env import OPENAI_API_KEY, OPENAI_MODEL
from messages import MessageHandler, MessageType
from prompts import perform_next_step_system_prompt
from cli import ask_for_input

async def agent_loop(
    openai: OpenAI,
    openai_tools: list,
    messages_handler: MessageHandler
) -> None:
    # Maximum number of autonomous steps
    max_iterations = 10
    
    for i in range(max_iterations):
        response = await openai.chat.completions.create(
            model=OPENAI_MODEL,
            temperature=0.2,
            messages=messages_handler.get_messages(),
            tools=openai_tools
        )
        
        messages_handler.add_message(response.choices[0].message)
        
        if is_done(response):
            break
            
        tool_call_response = await apply_tool_calls_if_present(response)
        if tool_call_response:
            messages_handler.add_messages(tool_call_response)
            
        messages_handler.add_message(perform_next_step_system_prompt)

async def main():
    messages_handler = MessageHandler()
    openai = OpenAI(api_key=OPENAI_API_KEY)
    
    mcp_tools_list = await mcp_client.list_tools()
    openai_tools = map_tool_list_to_openai_tools(mcp_tools_list)
    
    try:
        while True:
            user_input = await ask_for_input()
            if user_input == "exit":
                messages_handler.store_messages()
                break
                
            messages_handler.add_message({
                "role": "user",
                "content": user_input
            })
            
            await agent_loop(openai, openai_tools, messages_handler)
            
    except Exception as error:
        print(f"Error: {error}")
        messages_handler.store_messages()
    finally:
        mcp_client.close()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())