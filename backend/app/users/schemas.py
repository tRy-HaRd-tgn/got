from datetime import datetime
from pydantic import BaseModel, EmailStr


class UserRegister(BaseModel):
    login: str
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    login: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class UserProfile(BaseModel):
    login: str
    email: str
    balance: float
    created_at: datetime
