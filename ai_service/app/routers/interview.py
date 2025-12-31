from fastapi import APIRouter

router = APIRouter(prefix='/interview')

@router.get('/{application_id}')
async def start_interview(application_id: str):
    """
    This routes will start the interview with the help of interview manager
    """
    pass