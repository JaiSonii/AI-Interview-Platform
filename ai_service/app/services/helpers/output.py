from pydantic import BaseModel, Field
from typing import Literal, Optional

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