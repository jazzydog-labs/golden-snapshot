from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import engine
from models import User, Post
from models.base import Base
from routes import user_router, post_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="BlogAPI", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router)
app.include_router(post_router)


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.get("/")
def root():
    return {"message": "Welcome to BlogAPI"}