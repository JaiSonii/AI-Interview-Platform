from fastapi import APIRouter

router = APIRouter(prefix="/api")

@router.post('/interview-flow')
async def interview_flow():
    pass