from ..base_ai import BaseAI
from .models import BaseQuestionOutput, ExpRange
from .prompts import BASE_QUESTION_GENERATION_HUMAN_PROMPT, BASE_QUESTION_GENERATION_SYSTEM_PROMPT

from typing import Optional

from langchain_core.messages import BaseMessage, SystemMessage, HumanMessage


class JobQuestionGenerator(BaseAI):
    def __init__(self, model: str = 'gpt-4o') -> None:
        super().__init__(model, BaseQuestionOutput)

    def _create_messages(self, role: str, exp_range: ExpRange, description: str) -> list[BaseMessage]:
        """Create Human and System prompt"""
        min_exp = exp_range.get('min_exp')
        max_exp = exp_range.get('max_exp')
        formatted_exp = f"{min_exp} - {max_exp} years"
        
        messages: list[BaseMessage] = [
            SystemMessage(content=BASE_QUESTION_GENERATION_SYSTEM_PROMPT.format(role=role)),
            HumanMessage(content=BASE_QUESTION_GENERATION_HUMAN_PROMPT.format(
                role=role, 
                exp_range=formatted_exp, 
                description=description
            ))
        ]
        return messages

    async def invoke(self, **kwargs):
        """
        Generates the static Roadmap for the job posting.
        """
        role: Optional[str] = kwargs.get('role', None)
        exp_range: Optional[ExpRange] = kwargs.get('exp_range', None)
        description: Optional[str] = kwargs.get('description', None)

        missing_fields = []
        if not role: missing_fields.append("role")
        if not exp_range: missing_fields.append("exp_range")
        if not description: missing_fields.append("description")
        
        if missing_fields:
            raise ValueError(f"Missing required arguments: {', '.join(missing_fields)}")

        assert role is not None and exp_range is not None and description is not None

        msgs = self._create_messages(role, exp_range, description)
        
        return await self._model.ainvoke(input=msgs)