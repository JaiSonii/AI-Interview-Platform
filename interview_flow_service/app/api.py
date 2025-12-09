from fastapi import APIRouter, File, UploadFile, Request, Depends
from fastapi.exceptions import HTTPException
from app.services.interview_flow import get_interview_flow_service, InterviewFlow
from app.services.resume_parser import get_resume_parser_service, ResumeParser
from app.services.db_service import get_candidate_info
from app.services.resume_parser.models import StructuredResume
from app.services.interview_flow.models import ResumeQuestionsOutput

router = APIRouter(prefix="/api")

MAX_FILE_SIZE = 5 * 1024 * 1024  # 10 MB

async def verify_file(request : Request):
    """
    Verify the size of the uploaded file
    
    :param file: the uploaded file
    :type file: UploadFile
    """
    size = int(request.headers.get('content-length', 0))
    if size > MAX_FILE_SIZE:
        raise HTTPException(status_code=413, detail="File too large")
    

@router.post('/interview-flow/{id}', response_model=dict)
async def get_interview_flow(
    id: str, file: UploadFile = File(...),
     _: None = Depends(verify_file),
     resume_parser: ResumeParser = Depends(get_resume_parser_service),
     interview_flow: InterviewFlow = Depends(get_interview_flow_service)
    ):
    """
    Endpoint to handle interview flow with file upload

    :param id: The interview flow ID
    :type id: str
    :param file: The uploaded file
    :type file: UploadFile
    """
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file uploaded")
    ext = file.filename.split('.')[-1].lower()
    if ext != 'pdf':
        raise HTTPException(status_code=400, detail="Unsupported file type")
    
    try:
        file_bytes = await file.read()
        application_data = await get_candidate_info(id)
        application = application_data.get('application') if application_data else None
        print(application)
        if not application or application.get('job') is None:
            raise HTTPException(status_code=404, detail="Application info not found")
        resume_data: StructuredResume = await resume_parser.invoke(bytes_data= file_bytes) # type: ignore
        
        interview_flow_data: ResumeQuestionsOutput = await interview_flow.invoke( # type: ignore
            job_info = application.get('job', {}),
            candidate_info=resume_data.model_dump()
        )
        return interview_flow_data.model_dump()
    except Exception as e:
        print(f"Error in /interview-flow/{id} : {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")