from pydantic import BaseModel, Field
from typing import List, Optional, Literal, TypedDict

class ExpRange(TypedDict):
    min_exp : int
    max_exp : int

class Duration(TypedDict):
    start_month : int
    start_year : int
    end_month : int
    end_year : int

class Experience(TypedDict):
    company : str
    duration: Duration
    position : str
    description : str

class Projects(TypedDict):
    name : str
    description : str

class Achievement(TypedDict):
    name : str
    description : str

class Education(TypedDict):
    uni_name : str
    Duration : Duration

class StructuredResume(TypedDict):
    name : str
    summary : str
    skills : list[str]
    experience : list[Experience]
    projects : list[Projects]
    achievements : list[Achievement]
    education : Education

class InterviewTopic(BaseModel):
    id: str = Field(description="Unique ID for tracking, e.g., 'topic_1'")
    topic_name: str = Field(description="The technical concept being tested, e.g., 'Database Locking'")
    base_question: str = Field(description="The initial question to ask the candidate about this topic")
    difficulty: str = Field(description="Easy, Medium, or Hard")

class BaseQuestionOutput(BaseModel):
    roadmap: List[InterviewTopic]

class InterviewInteraction(BaseModel):
    """
    This is the lightweight response from the Light Model.
    It determines the flow of the interview.
    """
    decision: Literal["FOLLOW_UP", "NEXT_TOPIC"] = Field(
        description="Choose FOLLOW_UP if the answer is vague/interesting. Choose NEXT_TOPIC if satisfied."
    )
    reasoning: str = Field(
        description="Brief internal thought on why this decision was made (max 1 sentence)."
    )
    followup_question: Optional[str] = Field(
        default=None, 
        description="If decision is FOLLOW_UP, write the question here. If NEXT_TOPIC, leave None."
    )

