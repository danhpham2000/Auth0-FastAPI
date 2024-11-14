from pydantic import BaseModel, BeforeValidator, Field
from datetime import datetime
from typing import Annotated, Optional, List

PyObjectId = Annotated[str, BeforeValidator(str)]

class PostModel(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    title: str = Field(...)
    detail: str = Field(...)
    isCompleted: bool = False
    createdAt: int = int(datetime.timestamp(datetime.now()))


class PostCollection(BaseModel):
    posts: List[PostModel]