from .main import InterviewFlow
from functools import lru_cache

@lru_cache()
def get_interview_flow_service()->InterviewFlow:
    return InterviewFlow(model="gpt-4o")

