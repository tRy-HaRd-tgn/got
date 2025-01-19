from pydantic import BaseModel
from typing import Literal, Optional


class DonationCreate(BaseModel):
    name: str
    price: float
    category: Literal["privileges", "pets", "mounts", "other"]
    description: Optional[str] = None
    image_url: Optional[str] = None


class DonationResponse(BaseModel):
    id: int
    name: str
    price: float
    category: Literal["privileges", "pets", "mounts", "other"]
    description: Optional[str] = None
    image_url: Optional[str] = None
