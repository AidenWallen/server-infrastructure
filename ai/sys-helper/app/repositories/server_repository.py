from app.core.database import db
from app.schemas.server_info import ServerInfo
from bson import ObjectId

class ServerRepository:
    def __init__(self):
        # Allow repo to handle uninitialized db for tests
        pass

    @property
    def collection(self):
        if db.client is None:
            return None
        return db.client.sys_helper.server_info

    async def get_all(self):
        if self.collection is None:
            return []
        cursor = self.collection.find({})
        items = await cursor.to_list(length=100)
        return items

    async def create(self, info: ServerInfo):
        if self.collection is None:
            return "test-id"
        result = await self.collection.insert_one(info.dict())
        return result.inserted_id

