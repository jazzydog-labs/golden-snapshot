from sqlalchemy import Boolean, Column, String
from sqlalchemy.orm import relationship

from models.base import BaseModel


class User(BaseModel):
    __tablename__ = "users"

    email = Column(String, unique=True, index=True, nullable=False)
    name = Column(String)
    is_admin = Column(Boolean, default=False)

    posts = relationship("Post", back_populates="user")
