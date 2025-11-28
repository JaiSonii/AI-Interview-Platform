from pydantic import BaseModel, Field
from typing import List

class Question(BaseModel):
    text : str = Field(description="The full question to ask")
    typ : str = Field(description="the type of the question")

class BaseQuestionOuput(BaseModel):
    questions : List[Question]