from .context import Context
from ..base_ai import BaseAI
from .models import InterviewerOutput, Question, JobInfo
from .prompt import INTERVIEWER_PROMPT, QUESTION

from typing import List, Optional
from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage, AIMessage

class Interviewer(BaseAI):
    def __init__(self, application_id: str, job_info: JobInfo, questions: List[Question]) -> None:
        super().__init__('gpt-4o-mini', InterviewerOutput)
        self._system_prompt = SystemMessage(content=INTERVIEWER_PROMPT.format(**job_info)) 
        self.application_id = application_id
        self.questions: List[Question] = questions
        self._cur_ques_ind: int = 0

        self.context = Context()

    def add_next_question(self) -> Optional[str]:
        if self._cur_ques_ind == len(self.questions):
            return None
        
        question = self.questions[self._cur_ques_ind]
        self._cur_ques_ind += 1
        args = {
            "question" : question.get('base_question'),
            "topic": question.get('topic_name'),
            "diffculty": question.get('difficulty')
        }

        content = QUESTION.format(**args)
        self.context.add(AIMessage(content=content))
        return question.get('base_question')

    def _build_messages(self)-> List[BaseMessage]:
        return [self._system_prompt] + self.context.messages

    async def invoke(self, **kwargs):
        if self._cur_ques_ind == 0:
            first_q = self.add_next_question()
            return first_q

        answer: str = kwargs.get('answer', "I am not so sure about it.")
        self.context.add(HumanMessage(content=answer))
        
        messages = self._build_messages()
        ai_res = await self._model.invoke(input=messages)

        if ai_res.next_q:
            next_q = self.add_next_question()
            return next_q
        return ai_res.question.base_question