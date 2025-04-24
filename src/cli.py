from openai.types.chat import ChatCompletionMessage, ChatCompletionMessageParam
from colorama import Fore, Style
import sys

color_by_role = {
    "system": Fore.GREEN,
    "user": Fore.BLUE,
    "assistant": Fore.RED,
    "tool": Fore.YELLOW,
    "function": Fore.MAGENTA
}

def print_message(message: ChatCompletionMessage | ChatCompletionMessageParam, debug: bool = False) -> None:
    if (message.role in ["system", "tool"]) and not debug:
        return

    print(f"{color_by_role[message.role]}{Style.BRIGHT}{message.role}{Style.RESET_ALL}")

    if message.role == "assistant" and getattr(message, 'tool_calls', None):
        tool_call = message.tool_calls[0]
        print(
            f"The tool {Style.DIM}{tool_call.function.name}{Style.RESET_ALL} "
            f"was called with the arguments: {Style.DIM}{tool_call.function.arguments}{Style.RESET_ALL}"
        )
    else:
        print(message.content)
    
    # Add a line break
    print("")

def ask_for_input() -> str:
    print(f"{Fore.BLUE}{Style.BRIGHT}user{Style.RESET_ALL}")
    result = input(">")
    
    # Move cursor up and clear lines
    sys.stdout.write("\x1b[A")
    sys.stdout.write("\x1b[2K")
    sys.stdout.write("\x1b[A")
    sys.stdout.write("\x1b[2K")
    
    return result