from ..base_generator import BaseGenerator
from .models import StructuredResume

from typing import List

from langchain_core.messages import BaseMessage, SystemMessage, HumanMessage

SYSTEM_PROMPT = """
You are a proficient resume parser, and can extract resumes in any given format.
You are given text of a resume. Your task is to parse the resume and return the feilds as requested.
"""

USER_MESSAGE = """
Resume text : 
{resume_text}
"""

class ResumeParser(BaseGenerator):
    """
    This module is specifically responsible for creating structured resumes.
    It is recommended to use a light weight fast model for this process
    """
    def __init__(self, model_name : str = 'gpt-4o-mini') -> None:
        super().__init__(model_name, StructuredResume)

    async def invoke(self, **kwargs):
        resume_text: str = kwargs.get('resume_text', "")
        if not resume_text:
            raise ValueError("Resume text not provided")
        messages: List[BaseMessage] = [
            SystemMessage(SYSTEM_PROMPT),
            HumanMessage(USER_MESSAGE.format(resume_text = resume_text))
        ]

        return await self._model.ainvoke(messages)