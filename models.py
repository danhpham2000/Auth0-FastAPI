from pydantic import BaseModel

class Post(BaseModel):
    title: str
    detail: str
    createdAt: int
    is_completed: bool = False

