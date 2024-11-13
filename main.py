from fastapi import FastAPI, status
from fastapi.security import HTTPBearer
from dotenv import dotenv_values
from motor.motor_asyncio import AsyncIOMotorClient
from contextlib import asynccontextmanager
from models import Post
from database import init_db
from typing import List
import certifi

config = dotenv_values(".env")

async def start_up(app):
    app.mongodb_client = AsyncIOMotorClient(config["MONGODB_URI"], tlsCAFile=certifi.where())
    app.mongodb = app.mongodb_client.get_database("testing")
    print("Database connected")

async def shutdown(app):
    app.mongodb_client.close()
    print("Database closed")

@asynccontextmanager
async def db_lifespan(app: FastAPI):
    #Startup
    await start_up(app)
    yield

    await shutdown(app)


app = FastAPI(lifespan=db_lifespan)



@app.get("/public")
async def getPublic():
    return "Hello world!"

@app.get("/posts", response_model=List[Post])
async def getPosts(): 
    posts = await app.mongodb["posts"].find().to_list(None)
    return posts

@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=Post)
async def createPost(post: Post):
    result = await app.mongodb["posts"].insert_one()
    return result

