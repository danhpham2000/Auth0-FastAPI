from fastapi import FastAPI, APIRouter, status, HTTPException
from database import postCollection
from models import PostModel, PostCollection
from typing import List
from bson.objectid import ObjectId

app = FastAPI()
router = APIRouter()


@router.post("/posts", response_model=PostModel, status_code=status.HTTP_201_CREATED)
async def createPost(post: PostModel):
    """
    Insert new post record
    """
    try:
        newPost = await postCollection.insert_one(post.model_dump(by_alias=True, exclude=["id"]))
        createdPost = await postCollection.find_one({"_id": newPost.inserted_id})

        return createdPost
    except Exception as e:
        return HTTPException(detail=e)

    

@router.get("/posts", response_model=List[PostModel])
async def getPosts():
    """
    Get all post records
    """
    posts = await postCollection.find().to_list()
    return posts

@router.put("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def updatePost(id: str, post: PostModel):
    id = ObjectId(id)
    try:
        currentPost = await postCollection.find_one_and_update({"_id": id}, {"$set": post.model_dump(by_alias=True, exclude=["id"])})
        if not currentPost:
            return HTTPException(status_code=404, detail="Post not found")
    except Exception as e:
        return HTTPException(detail=e, status_code=404)
    
@router.get("/posts/{id}", response_model=PostModel)
async def getPost(id: str):
    try:
        id = ObjectId(id)
        currentPost = await postCollection.find_one({"_id": id})
        if not currentPost:
            return HTTPException(status_code=404, detail="Post not found")
        return currentPost
    except Exception as e:
        return HTTPException(detail=e)


app.include_router(router)



