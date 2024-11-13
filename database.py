from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import dotenv_values
import certifi


config = dotenv_values(".env")

from models import Post

async def init_db():
    client = AsyncIOMotorClient(config["MONGODB_URI"], tlsCAFile=certifi.where())

    await init_beanie(database=client.db_name, document_models=[Post])