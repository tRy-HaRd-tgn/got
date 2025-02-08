from typing import Optional
from fastapi import UploadFile
from pydantic import BaseModel


class PaymentResponse(BaseModel):
    payment_url: str
    order_id: str
    message: Optional[str]
