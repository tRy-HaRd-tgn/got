from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app.mailer.mailer import generate_confirmation_token, send_confirmation_email
from app.users.dao import UsersDAO
from app.users.schemas import UserRegister, Token, UserLogin
from app.users.auth import create_access_token, hash_password, verify_password
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from app.config import settings
from app.users.dao import UsersDAO


router = APIRouter(
    prefix="/users",
    tags=["Reg && Login"],
)


@router.post("/register", response_model=Token)
async def register_user(user: UserRegister):
    existing_user = await UsersDAO.find_one_or_none(login=user.login)
    if existing_user:
        raise HTTPException(status_code=400, detail="Логин уже используется")

    existing_email = await UsersDAO.find_one_or_none(email=user.email)
    if existing_email:
        raise HTTPException(status_code=400, detail="Email уже используется")

    new_user = await UsersDAO.add(
        login=user.login,
        email=user.email,
        hashed_password=hash_password(user.password),
        balance=0,
        is_verified=False,
    )
    token = generate_confirmation_token(user.email)

    await send_confirmation_email(user.email, token)

    access_token = create_access_token(data={"sub": user.login})
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/login", response_model=Token)
async def login_user(form_data: OAuth2PasswordRequestForm = Depends()):
    db_user = await UsersDAO.find_one_or_none(login=form_data.username)
    if not db_user or not verify_password(form_data.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Неверный логин или пароль")

    if not db_user.is_verified:
        raise HTTPException(status_code=403, detail="Email не подтверждён")

    access_token = create_access_token(data={"sub": db_user.login})
    return {"access_token": access_token, "token_type": "bearer"}
