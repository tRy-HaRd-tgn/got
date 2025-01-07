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
