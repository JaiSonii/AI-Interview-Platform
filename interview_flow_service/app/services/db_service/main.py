from app.config import settings
from prisma import Prisma
from typing import Dict, Any


class DBService:
    def __init__(self):
        self._client = Prisma()

    async def connect(self):
        if not self._client.is_connected():
            await self._client.connect()

    async def disconnect(self):
        if self._client.is_connected():
            await self._client.disconnect()

    async def get_job_by_id(self, job_id: str):
        """
        Fetch a Job by job id
        """
        return await self._client.job.find_unique(
            where={'id' : job_id}
        )
    
    async def save_job_questions(self, job_id: str, job_questions: list):
        await self._client.job.update(
            where={"id" : job_id},
            data={"roadmap" : job_questions} #type: ignore
        )

    async def get_application_by_id(self, application_id: str):
        """
        Fetch a Job application by application ID
        Args:
            application_id: Application ID
        """
        return await self._client.application.find_unique(
            where={"id" : application_id},
            include={"job" : True}
        )


    async def save_interview_flow(self, application_id: str, interview_flow_data: Dict[str, Any]):
        """
        Save generated interview flow to the DB
        Args:
            application_id : application_id of the candidate
            interview_flow_data: the dict containing the interview flow generated from LLM
        Returns:
            Dict containing the updated application
        """
        updated_application = await self._client.application.update(
            where={"id" : application_id},
            data={"flow" : interview_flow_data, "status" : "FLOW_READY"}, #type: ignore
            include={"job" : True}
        )
        return updated_application

