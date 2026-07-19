from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings

class Database:
    client: AsyncIOMotorClient = None

db = Database()

async def connect_to_mongo():
    db.client = AsyncIOMotorClient(settings.MONGO_URL)
    # Ping the server to verify connection
    await db.client.admin.command('ping')

async def close_mongo_connection():
    db.client.close()
