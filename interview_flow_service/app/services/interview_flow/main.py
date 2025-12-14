from langchain_core.messages import HumanMessage, SystemMessage, BaseMessage

from .models import ResumeQuestionsOutput, JobInfo, CandidateInfo
from .prompt import INTERVIEW_FLOW_PROMPT
from ..base_ai import BaseAI

from app.config import settings


class InterviewFlow(BaseAI):
    def __init__(self, model="gpt-4o") -> None:
        super().__init__(model, ResumeQuestionsOutput)

    async def invoke(self, **kwargs):
        job_info: JobInfo = kwargs.get('job_info', {})
        candidate_info: CandidateInfo = kwargs.get('candidate_info', {})

        if not job_info:
            raise ValueError(f"Job Info is {job_info}")
        
        if not candidate_info:
            raise ValueError(f"Candidate Info not provided")
        
        max_intro_questions: int = settings.MAX_INTRO_QUESTIONS
        max_proj_and_exp_ques: int = settings.MAX_PROJ_AND_INTERVIEW_QUESTIONS

        system_prompt_inp = {
            "role" : job_info.get('title'),
            "candidate_name" : candidate_info.get('name'),
            "max_intro_questions" : max_intro_questions,
            "max_project_and_exp_ques" : max_proj_and_exp_ques
        }
        messages: list[BaseMessage] =  [
            SystemMessage(content=INTERVIEW_FLOW_PROMPT.format(**system_prompt_inp)),
            HumanMessage(content=f"Generate the interview flow, \nResume Data: \n{str(candidate_info)}")
        ]

        return await self._model.ainvoke(messages)
