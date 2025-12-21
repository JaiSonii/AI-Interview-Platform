from fastapi import APIRouter, UploadFile, File, status, Form
from fastapi.exceptions import HTTPException
from typing import Annotated
from app.logger import logger
from app.services.aws import aws
from app.services.message_broker import msg_broker

router = APIRouter(prefix='/api/resume', tags=['resume'])

@router.post('/{application_id}', response_model=dict)
async def post_resume(
    application_id: str, 
    session_id: Annotated[str, Form(...)], 
    file : Annotated[UploadFile, File(...)]
    ):
    try:
        if msg_broker is None:
            raise ValueError('Consumer is not initialized')
        if not file.filename:
            raise HTTPException(status_code=400, detail="No file uploaded")
        resume_url = await aws.upload_and_get_url(file, f"resumes/{application_id}")
        payload = {
            "application_id" : application_id,
            "resume_url" : resume_url,
            "session_id" : session_id
        }
        await msg_broker.send_message('interview.exchange', 'flow.create', payload)
        return {
            "message": "Resume uploaded successfully",
            "url" : resume_url
        }
    except Exception as e:
        logger.error(f"Error in posting resume : {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="internal server error"
        )