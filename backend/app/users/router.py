from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app.mailer.mailer import generate_confirmation_token, send_confirmation_email
from app.users.dao import UsersDAO
from app.users.schemas import UserProfile, UserRegister, Token, UserLogin
from app.users.auth import create_access_token, hash_password, verify_password
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from app.config import settings
from app.users.dao import UsersDAO
from app.models import User
from app.users.dependencies import get_current_user
from app.skins.dependencies import SkinService


router = APIRouter(
    prefix="/users",
    tags=["Reg && Login"],
)


@router.post("/register", response_model=Token)
async def register_user(user: UserRegister):
    # Проверяем, существует ли пользователь с таким логином или email
    existing_user = await UsersDAO.find_one_or_none(login=user.login)
    if existing_user:
        raise HTTPException(status_code=400, detail="Логин уже используется")

    existing_email = await UsersDAO.find_one_or_none(email=user.email)
    if existing_email:
        raise HTTPException(status_code=400, detail="Email уже используется")

    # Создаем пользователя
    new_user = await UsersDAO.add(
        login=user.login,
        email=user.email,
        hashed_password=hash_password(user.password),
        balance=0,
        is_verified=False,
    )

    # Создаем базовый скин
    skin_url = await SkinService.create_base_skin(user.login)

    # Обновляем профиль пользователя с URL скина
    await UsersDAO.update(new_user.id, skin_url=skin_url)

    # Генерируем токен подтверждения и отправляем письмо
    token = generate_confirmation_token(user.email)
    await send_confirmation_email(user.email, token)

    # Создаем access token для авторизации
    access_token = create_access_token(data={"sub": user.login})
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/login", response_model=Token)
async def login_user(form_data: OAuth2PasswordRequestForm = Depends()):
    # Проверяем логин и пароль
    db_user = await UsersDAO.find_one_or_none(login=form_data.username)
    if not db_user or not verify_password(form_data.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Неверный логин или пароль")

    # Проверяем, подтвержден ли email
    if not db_user.is_verified:
        raise HTTPException(status_code=403, detail="Email не подтверждён")

    # Создаем access token
    access_token = create_access_token(data={"sub": db_user.login})
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/profile", response_model=UserProfile)
async def get_profile(current_user: User = Depends(get_current_user)):
    """
    Возвращает информацию о текущем пользователе (личный кабинет).
    """
    return {
        "login": current_user.login,
        "email": current_user.email,
        "balance": current_user.balance,
        "created_at": current_user.created_at,
        "skin_url": current_user.skin_url,  # URL скина
    }
