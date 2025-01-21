from datetime import datetime
import re
from pydantic import BaseModel, EmailStr, validator


class UserRegister(BaseModel):
    login: str
    email: EmailStr
    password: str

    # Дополнительные проверки
    @validator("login")
    def validate_login(cls, v):
        if len(v) < 3:
            raise ValueError("Логин должен быть длиннее 3 символов")
        return v

    @validator("password")
    def validate_password(cls, value):
        # Регулярное выражение для пароля (минимум 8 символов, хотя бы одна цифра, одна заглавная буква, и один специальный символ)
        password_regex = r"^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"
        if not re.match(password_regex, value):
            raise ValueError(
                "Пароль должен быть не менее 8 символов и содержать хотя бы одну цифру, одну заглавную букву и один специальный символ"
            )
        return value


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
