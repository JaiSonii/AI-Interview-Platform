from abc import ABC, abstractmethod
from langchain_openai.chat_models import ChatOpenAI
from langchain_core.runnables import Runnable
from langchain_openai.chat_models.base import _DictOrPydanticClass
from pydantic import SecretStr
import os
from app.config import settings

class BaseAI(ABC):
    """
    This is the base class, which provides a blue print for rest of the AI based classes
    """
    def __init__(self, model: str, output_schema: _DictOrPydanticClass ) -> None:
        self._model = self._init_model(model, output_schema)

    def _init_model(self, model_name: str, output_schema: _DictOrPydanticClass)->Runnable:
        """
        Create an instance of the Chat Mode
        Args:
            model_name: name of the model(LLM)
            output_schema: the pydantic schema requried for structured output

        Returns:
            an instance of a Runnable from Langchain OpenAI
        """
        api_key = settings.OPENAI_API_KEY
        if api_key is None:
            raise ValueError("OPENAI API Key not provided")
        
        model = ChatOpenAI(
            model=model_name,
            api_key=SecretStr(api_key),
            temperature=0.1
        )

        if output_schema:
            return model.with_structured_output(output_schema)
        return model

    @abstractmethod
    async def invoke(self, **kwargs):
        """Main invoke method to invoke the API call to LLM"""
        pass