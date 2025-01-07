from pydantic import BaseModel
from typing import Optional


class DonationCreate(BaseModel):
    name: str
    price: float
    category: str
    description: Optional[str] = None
    image_url: Optional[str] = None


class DonationResponse(BaseModel):
    id: int
    name: str
    price: float
    category: str
    description: Optional[str] = None
    image_url: Optional[str] = None
