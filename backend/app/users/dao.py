from sqlalchemy import update
from app.dao.base import BaseDAO
from app.models import User
from app.database import async_session_maker


class UsersDAO(BaseDAO):
    model = User

    @classmethod
    async def update(cls, user_id: int, **kwargs):
        async with async_session_maker() as session:
            stmt = (
                update(User)
                .where(User.id == user_id)
                .values(**kwargs)  # Обновляем переданные поля
            )
            await session.execute(stmt)
            await session.commit()

    @classmethod
    async def add(
        cls,
        login: str,
        email: str,
        hashed_password: str,
        balance: float = 0,
        is_verified: bool = False,
    ) -> User:
        """
        Добавляет нового пользователя и возвращает его.
        """
        async with async_session_maker() as session:
            # Создаем нового пользователя
            user = User(
                login=login,
                email=email,
                hashed_password=hashed_password,
                balance=balance,
                is_verified=is_verified,
            )
            session.add(user)
            await session.commit()
            await session.refresh(user)  # Обновляем объект, чтобы получить его ID
            return user  # Возвращаем созданного пользователя
