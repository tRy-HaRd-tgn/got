from datetime import datetime
import re
from pydantic import BaseModel, EmailStr, validator


class UserRegister(BaseModel):
    login: str
    email: EmailStr
    password: str

    @validator("login")
    def validate_login(cls, value):
        # Регулярное выражение для логина:
        # - Только буквы и символ `_`.
        # - Без цифр, пробелов.
        # - Длина от 3 до 12 символов.
        login_regex = r"^[a-zA-Z_]{3,12}$"
        if not re.match(login_regex, value):
            raise ValueError(
                "Логин должен быть длиной от 3 до 12 символов, содержать только буквы и символ '_', "
                "цифры и пробелы запрещены."
            )
        return value

    @validator("password")
    def validate_password(cls, value):
        # Регулярное выражение для пароля:
        # - Хотя бы одна буква, цифра, спецсимвол (@$!%*?&.),
        # - Длина от 8 символов.
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
