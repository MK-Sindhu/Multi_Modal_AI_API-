from fastapi import APIRouter
from utils.id import get_container_id
from pydantic_schemas.health import HealthResponse

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
async def health():
    return {"status": "ok", "container_id": get_container_id()}
