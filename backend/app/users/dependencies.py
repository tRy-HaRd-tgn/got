from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from app.config import settings
from app.users.dao import UsersDAO
from app.users.auth import is_token_revoked

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/users/login")


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Не удалось подтвердить учетные данные",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        login: str = payload.get("sub")
        if login is None:
            raise credentials_exception

        # Проверяем, аннулирован ли токен
        user = await UsersDAO.find_one_or_none(login=login)
        if user and await is_token_revoked(user.id):
            raise credentials_exception

    except JWTError:
        raise credentials_exception

    user = await UsersDAO.find_one_or_none(login=login)
    if user is None:
        raise credentials_exception
    return user
