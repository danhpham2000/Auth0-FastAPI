from fastapi import FastAPI, APIRouter, status
from database import postCollection
from models import PostModel, PostCollection
from typing import List

app = FastAPI()
router = APIRouter()


@router.post("/posts", response_model=PostModel, status_code=status.HTTP_201_CREATED)
async def createPost(post: PostModel):
    """
    Insert new post record
    """
    newPost = await postCollection.insert_one(post.model_dump(by_alias=True, exclude=["id"]))
    createdPost = await postCollection.find_one({"_id": newPost.inserted_id})

    return createdPost

@router.get("/posts", response_model=List[PostModel])
async def getPosts():
    """
    Get all post records
    """
    posts = await postCollection.find().to_list()
    return posts



app.include_router(router)



