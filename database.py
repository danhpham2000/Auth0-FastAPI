from dotenv import dotenv_values
from motor.motor_asyncio import AsyncIOMotorClient

import certifi

config = dotenv_values(".env")

mongoClient = AsyncIOMotorClient(config["MONGODB_URI"], tlsCAFile = certifi.where())

mongoDatabase = mongoClient["testing"]

postCollection = mongoDatabase["posts"]