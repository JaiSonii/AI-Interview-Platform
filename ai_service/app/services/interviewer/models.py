from pydantic import BaseModel, Field
from typing import TypedDict, Optional

class InterviewTopic(BaseModel):
    id: str = Field(description="Unique ID for tracking, e.g., 'topic_1'")
    topic_name: str = Field(description="The technical concept being tested, e.g., 'Database Locking'")
    base_question: str = Field(description="The initial question to ask the candidate about this topic")
    difficulty: str = Field(description="Easy, Medium, or Hard")

class InterviewerOutput(BaseModel):
    question: Optional[InterviewTopic] = Field(description="The followup question if required")
    next_q: bool = Field(description="True if need to move to next question, False if there is a followup question")

class ExpRange(TypedDict):
    min_exp: int
    max_exp: int

class JobInfo(TypedDict):
    role : str
    exp_range: ExpRange
    description: str
    

class Question(TypedDict):
    id: str
    topic_name: str
    base_question: str
    difficulty: str