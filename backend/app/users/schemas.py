from datetime import datetime
import re
from pydantic import BaseModel, EmailStr, validator


from fastapi import HTTPException


import re
from pydantic import BaseModel, EmailStr, field_validator
from fastapi import HTTPException


class UserRegister(BaseModel):
    login: str
    email: EmailStr
    password: str

    @field_validator("login")
    @classmethod
    def validate_login(cls, value: str) -> str:
        login_regex = r"^[a-zA-Z_]{3,12}$"
        if not re.match(login_regex, value):
            raise ValueError(
                "Логин должен быть длиной от 3 до 12 символов, содержать только буквы и символ '_', "
                "цифры и пробелы запрещены."
            )
        return value

    @field_validator("password")
    @classmethod
    def validate_password(cls, value: str) -> str:
        password_regex = (
            r"^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*?&\.])[A-Za-z\d@$!%*?&\.]{8,}$"
        )
        if not re.match(password_regex, value):
            raise ValueError(
                "Пароль должен быть длиной от 8 символов, содержать хотя бы одну букву, одну цифру "
                "и один из специальных символов: @$!%*?&."
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
