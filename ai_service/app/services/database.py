from prisma import Prisma
from typing import Optional

class DB:
    def __init__(self) -> None:
        self._client = Prisma()

    async def connect(self)->None:
        """
        Connect to the DB client
        """
        if not self._client.is_connected():
            await self._client.connect()

    async def disconnect(self):
        """
        Disconnect with the DB Client
        """
        if self._client.is_connected():
            await self._client.disconnect()

    async def get_job_by_id(self, id: str):
        """
        Fetch Job by id
        """
        await self.connect()
        return await self._client.job.find_unique(
            where={'id' : id}
        )
    
    async def get_application_by_id(self, application_id: str):
        """
        Fetch Application by application id
        """
        await self.connect()
        return await self._client.application.find_unique(
            where={"id" : application_id},
            include={"job" : True}
        )
    
db: Optional[DB] = None

def init_db()->DB:
    """
    Initialize the Database. DB will self connect in the first db call.
    """
    global db
    if db is None:
        db = DB()
    return db