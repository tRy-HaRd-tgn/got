from fastapi import APIRouter, Depends, HTTPException, Request, Response
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app.mailer.mailer import generate_confirmation_token, send_confirmation_email
from app.users.dao import UsersDAO
from app.users.schemas import UserProfile, UserRegister, Token, UserLogin
from app.users.auth import (
    create_access_token,
    create_refresh_token,
    decode_token,
    hash_password,
    verify_password,
)
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from app.config import settings
from app.users.dao import UsersDAO
from app.models import User
from app.users.dependencies import get_current_user
from app.skins.dependencies import SkinService
from fastapi_cache.decorator import cache
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(
    prefix="/users",
    tags=["Reg && Login"],
)


@router.post("/register")
async def register_user(user: UserRegister):
    # Проверяем, существует ли пользователь с таким логином или email
    existing_user = await UsersDAO.find_one_or_none(login=user.login)
    if existing_user:
        raise HTTPException(status_code=400, detail="Логин уже используется")

    existing_email = await UsersDAO.find_one_or_none(email=user.email)
    if existing_email:
        raise HTTPException(status_code=400, detail="Email уже используется")

    try:
        # Генерируем токен подтверждения и отправляем письмо
        token = generate_confirmation_token(user.email)
        await send_confirmation_email(user.email, token)

        # Создаем пользователя только после успешной отправки письма
        new_user = await UsersDAO.add(
            login=user.login,
            email=user.email,
            hashed_password=hash_password(user.password),
            balance=0,
            is_verified=False,
        )

        return {"message": "Вы создали аккаунт, подтвердите почту!"}

    except Exception as e:
        # Если произошла ошибка при отправке письма, отменяем создание пользователя
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при регистрации: {str(e)}",
        )


@router.get("/profile", response_model=UserProfile)
@cache(expire=120)
async def get_profile(current_user: User = Depends(get_current_user)):
    """
    Возвращает информацию о текущем пользователе (личный кабинет).
    """
    return {
        "login": current_user.login,
        "email": current_user.email,
        "balance": current_user.balance,
        "created_at": current_user.created_at,
    }


@router.post("/login", response_model=Token)
async def login_user(
    form_data: OAuth2PasswordRequestForm = Depends(),
    response: Response = None,
):
    """
    Авторизация пользователя.
    """
    # Проверяем логин и пароль
    db_user = await UsersDAO.find_one_or_none(login=form_data.username)
    if not db_user or not verify_password(form_data.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Неверный логин или пароль")

    # Проверяем, подтвержден ли email
    if not db_user.is_verified:
        raise HTTPException(status_code=403, detail="Email не подтверждён")

    # Создаем access и refresh токены
    access_token = create_access_token(data={"sub": db_user.login})
    refresh_token = create_refresh_token(data={"sub": db_user.login})

    # Устанавливаем refresh token в куки
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        max_age=settings.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60,
        secure=False,  # Включить secure в production
        samesite="lax",
    )

    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/refresh-token", response_model=Token)
async def refresh_token(request: Request):
    """
    Обновляет access token с помощью refresh token.
    """
    # Получаем refresh token из куки
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        raise HTTPException(status_code=401, detail="Refresh token отсутствует")

    # Декодируем refresh token
    payload = decode_token(refresh_token)
    if not payload:
        raise HTTPException(status_code=401, detail="Неверный refresh token")

    # Получаем пользователя
    user_login = payload.get("sub")
    db_user = await UsersDAO.find_one_or_none(login=user_login)
    if not db_user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")

    # Создаем новый access token
    access_token = create_access_token(data={"sub": db_user.login})

    return {"access_token": access_token, "token_type": "bearer"}
