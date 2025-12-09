from .main import ResumeParser
from functools import lru_cache

@lru_cache()
def get_resume_parser_service()->ResumeParser:
    return ResumeParser(model_name='gpt-4o-mini')