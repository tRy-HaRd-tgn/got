from typing import Optional
from fastapi import UploadFile
from pydantic import BaseModel


class PostCreate(BaseModel):
    title: str
    content: str
    image: UploadFile
    discord_url: str


class PostResponse(BaseModel):
    id: int
    title: str
    content: str
    discord_url: str
    image_url: Optional[str]
    author_login: str
    created_at: str
