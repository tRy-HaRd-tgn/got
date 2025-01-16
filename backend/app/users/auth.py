from jose import JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
import jwt
from app.config import settings
from app.database import redis

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encoded_jwt


def create_refresh_token(data: dict) -> str:
    """
    Создает refresh token.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encoded_jwt


def decode_token(token: str) -> dict:
    """
    Декодирует токен (access или refresh).
    """
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        return payload
    except JWTError:
        return None


async def revoke_token(user_id: int, token: str):
    """
    Аннулирует текущий токен пользователя.
    """
    ttl = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    await redis.set(
        f"revoked_token:{user_id}:{token}",  # Ключ включает user_id и токен
        str(datetime.utcnow()),
        ex=int(ttl.total_seconds()),  # Устанавливаем TTL
    )


async def is_token_revoked(user_id: int, token: str) -> bool:
    """
    Проверяет, аннулирован ли текущий токен пользователя.
    """
    return await redis.exists(f"revoked_token:{user_id}:{token}") == 1


async def save_refresh_token(user_id: int, refresh_token: str):
    """
    Сохраняет refresh token в Redis.
    """
    await redis.set(f"refresh_token:{user_id}", refresh_token)


async def get_refresh_token(user_id: int) -> str:
    """
    Получает refresh token из Redis.
    """
    return await redis.get(f"refresh_token:{user_id}")


async def delete_refresh_token(user_id: int):
    """
    Удаляет refresh token из Redis.
    """
    await redis.delete(f"refresh_token:{user_id}")
