from pydantic import BaseModel, Field
from typing import List, TypedDict, Optional

class Exp(TypedDict):
    min_exp : int
    max_exp : int

class JobInfo(TypedDict):
    role : str
    exp : Exp
    description : str

class MonthYear(TypedDict):
    month : int
    year : int

class ExperienceDuration(TypedDict):
    start : MonthYear
    end : MonthYear

class Education(TypedDict):
    uni_name : str
    start_year : int
    end_year : Optional[int]
    sgpa : float

class Project(TypedDict):
    name : str
    skills : List[str]
    description : List[str]

class Experience(TypedDict):
    role : str
    company : str
    duration : ExperienceDuration
    skills : List[str]
    description : List[str]

class CandidateInfo(TypedDict):
    name : str
    total_exp : float
    education : Education
    projects : List[Project]
    experience : List[Experience]

class InterviewTopic(BaseModel):
    id: str = Field(description="Unique ID for tracking, e.g., 'topic_1'")
    topic_name: str = Field(description="The technical concept being tested, e.g., 'Database Locking'")
    base_question: str = Field(description="The initial question to ask the candidate about this topic")
    difficulty: str = Field(description="Easy, Medium, or Hard")


class ResumeQuestionsOutput(BaseModel):
    introduction: InterviewTopic = Field(
        description="The initial ice-breaker question, usually 'Tell me about yourself' or similar."
    )
    experience: List[InterviewTopic] = Field(
        description="Questions specific to their work history (companies, roles, achievements)."
    )
    projects: List[InterviewTopic] = Field(
        description="Questions specific to their technical projects."
    )