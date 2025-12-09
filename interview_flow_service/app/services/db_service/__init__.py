import httpx
from app.config import settings

async def get_candidate_info(id: str):
    try:
        async with httpx.AsyncClient(timeout=5) as client:
            res = await client.get(f"{settings.JOB_SERVICE_URL}/application/{id}")
            
            if res.status_code == 200:
                print("Response : --------------------------------")
                print(res.json())
                return res.json()
    except Exception as e:
        print(f"Error fetching candidate info: {e}")
    
    return None
