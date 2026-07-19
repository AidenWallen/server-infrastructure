from app.repositories.server_repository import ServerRepository
from app.core.logger import logger
from app.schemas.server_info import ServerInfo

class ServerService:
    def __init__(self):
        self.repo = ServerRepository()

    async def get_all_server_info(self):
        logger.info("Service: Fetching all server info")
        return await self.repo.get_all()
    
    async def add_server_info(self, info: ServerInfo):
        logger.info(f"Service: Adding new server info for {info.id}")
        return await self.repo.create(info)
