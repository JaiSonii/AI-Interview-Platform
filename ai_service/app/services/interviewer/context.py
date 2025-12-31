from langchain_core.messages import BaseMessage

from typing import List

class Context:
    def __init__(self) -> None:
        self._messages: List[BaseMessage] = []

    @property
    def messages(self) -> List[BaseMessage]:
        return self._messages[-4:]
    
    def add(self, message: BaseMessage):
        self._messages.append(message)