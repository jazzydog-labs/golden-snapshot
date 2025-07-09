from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from schemas.user_schemas import User


class PostBase(BaseModel):
    title: str
    content: Optional[str] = None
    published: bool = False
    views: int = 0


class PostCreate(PostBase):
    pass


class PostUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    published: Optional[bool] = None
    views: Optional[int] = None


class Post(PostBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    user: Optional[User] = None

    class Config:
        from_attributes = True
