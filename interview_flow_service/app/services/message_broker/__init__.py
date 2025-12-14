from .main import MessageBroker
from typing import Optional
from functools import lru_cache

@lru_cache()
def get_message_broker()->MessageBroker:
    return MessageBroker()
