from ..base_generator import BaseGenerator
from .models import StructuredResume
import pypdfium2 as pdf_parser

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

    def _get_text(self, pdf_bytes : bytes)->str:
        """
        Extract text from pdf
        """
        pdf = pdf_parser.PdfDocument(pdf_bytes)
        txt = ""

        for page_num in range(len(pdf)):
            page = pdf.get_page(page_num)
            textpage = page.get_textpage()
            txt += textpage.get_text_range()
            textpage.close()
            page.close()
        return txt
    
    async def invoke(self, **kwargs):
        data: bytes = kwargs.get('bytes_data')  # type: ignore
        if data is None:
            raise ValueError("bytes_data not provided")
    
        resume_text = self._get_text(data)
        if not resume_text:
            raise ValueError("Resume text not provided")
        
        messages: List[BaseMessage] = [
            SystemMessage(SYSTEM_PROMPT),
            HumanMessage(USER_MESSAGE.format(resume_text = resume_text))
        ]

        return await self._model.ainvoke(messages)

