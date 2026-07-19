from fastapi import APIRouter
from app.services.server_service import ServerService
from app.schemas.server_info import ServerInfo

router = APIRouter(prefix="/server", tags=["server"])
service = ServerService()

@router.get("/")
async def get_all():
    return await service.get_all_server_info()

@router.post("/")
async def create(info: ServerInfo):
    return await service.add_server_info(info)
