from langchain_core.messages import HumanMessage, SystemMessage, BaseMessage

from .models import ResumeQuestionsOutput, JobInfo, CandidateInfo
from .prompt import INTERVIEW_FLOW_PROMPT
from ..base_generator import BaseGenerator


class InterviewFlow(BaseGenerator):
    def __init__(self, model="gpt-4o") -> None:
        super().__init__(model, ResumeQuestionsOutput)

    async def invoke(self, **kwargs):
        job_info: JobInfo = kwargs.get('job_info', {})
        candidate_info: CandidateInfo = kwargs.get('candidate_info', {})

        if not job_info:
            raise ValueError(f"Job Info is {job_info}")
        
        if not candidate_info:
            raise ValueError(f"Candidate Info not provided")
        
        max_intro_questions: int = kwargs.get('max_interview_ques', 1)
        max_proj_and_exp_ques: int = kwargs.get('max_proj_and_interview_ques', 5)

        system_prompt_inp = {
            "role" : job_info.get('role'),
            "candidate_name" : candidate_info.get('name'),
            "max_intro_questions" : max_intro_questions,
            "max_project_and_exp_ques" : max_proj_and_exp_ques
        }
        messages: list[BaseMessage] =  [
            SystemMessage(INTERVIEW_FLOW_PROMPT.format(system_prompt_inp)),
            HumanMessage("Generate the interview flow")
        ]

        return await self._model.ainvoke(messages)
