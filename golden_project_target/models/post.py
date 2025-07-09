from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from models.base import BaseModel


class Post(BaseModel):
    __tablename__ = "posts"
    
    title = Column(String, nullable=False)
    content = Column(Text)
    published = Column(Boolean, default=False)
    views = Column(Integer, default=0)
    user_id = Column(Integer, ForeignKey("users.id"))
    
    user = relationship("User", back_populates="posts")