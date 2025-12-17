from fastapi import APIRouter
from datetime import datetime, timezone

router = APIRouter()

@router.get("/")
async def health_check():
    return {
        "status": "HEALTHY",
        "current_time": datetime.now(timezone.utc).isoformat()
    }
