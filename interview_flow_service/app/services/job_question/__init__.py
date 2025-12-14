from functools import lru_cache
from .main import JobQuestionGenerator

@lru_cache()
def get_job_question_service()->JobQuestionGenerator:
    return JobQuestionGenerator()