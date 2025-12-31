from app.services.interviewer import Interviewer
from typing import List, Optional
from app.services.database import db, DB
from app.services.interviewer.models import JobInfo, ExpRange, Question
from app.logger import logger

class InterviewManager:
    def __init__(self) -> None:
        self.interviews: dict[str, Interviewer]
        self.db: Optional[DB] = db
        if self.db is None:
            raise ValueError("Database is not initalized")
    
    def _prepare_questions(self, application) -> List[Question]:
        roadmap = application.get('job', {}).get('roadmap', [])
        flow = application.get('flow', {})
        questions = roadmap + flow.get('intro_questions') + flow.get('proj_and_exp_ques')
        return questions

    async def add_interview(self, socket_id: str, application_id: str):
        """
        Create a new interview session
        Args:
            socket_id: Socket Id of the client
            application_id: application_id stored in DB
        """
        if self.interviews[socket_id]:
            raise KeyError('Interview is already being conducted')
        
        assert self.db is not None # Just for type annotation
        application = await self.db.get_application_by_id(application_id=application_id)

        if application is None or application.job is None:
            raise KeyError('Invalid Application ID')
        
        import json
        job_info = JobInfo(
            role=application.job.role,
            exp_range=ExpRange(**json.loads(application.job.exp_range)),
            description=application.job.description
        )

        questions = self._prepare_questions(application.model_dump())

        # assign the interview
        self.interviews[socket_id] = Interviewer(application_id, job_info, questions)

    async def invoke(self, socket_id: str):
        """
        Function to get the questions from the interviewer
        Args:
            socket_id: socket_id of the client
        Returns:
            Result from the interviewer
        """
        if self.interviews.get(socket_id, None) is None:
            logger.warning(f"Interview is not initialized for client: {socket_id}")
            return
        
        return await self.interviews[socket_id].invoke()