from typing import List, Optional, Union
from openai.types.chat import ChatCompletionMessage, ChatCompletionMessageParam
import json
from cli import print_message
from prompts import initial_message_system_prompt, perform_next_step_system_prompt
from env import DEBUG

MessageType = Union[ChatCompletionMessage, ChatCompletionMessageParam]

class MessageHandler:
    def __init__(self):
        self.messages: List[MessageType] = [initial_message_system_prompt]
        self.debug: bool = DEBUG

    def load_messages(self, add_perform_next_step: bool = True) -> Optional[List[MessageType]]:
        try:
            with open("messages.json", "r", encoding="utf-8") as f:
                messages = json.load(f)
            
            if add_perform_next_step:
                messages.append(perform_next_step_system_prompt)
            
            return messages
        except Exception as e:
            print("Error loading messages", e)
            return None

    def add_message(self, message: MessageType) -> None:
        self.messages.append(message)
        print_message(message, self.debug)

    def add_messages(self, messages: List[MessageType]) -> None:
        for message in messages:
            self.add_message(message)

    def store_messages(self) -> None:
        with open("messages.json", "w", encoding="utf-8") as f:
            json.dump(self.messages, f, indent=2)

    def get_messages(self) -> List[MessageType]:
        return self.messages