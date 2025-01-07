from datetime import datetime
from typing import Optional
from sqlalchemy import insert, select, update
from app.dao.base import BaseDAO
from sqlalchemy.orm import joinedload
from app.models import Post
from app.database import async_session_maker


class PostsDAO(BaseDAO):
    model = Post

    @classmethod
    async def find_all(cls):
        async with async_session_maker() as session:
            query = select(Post).options(
                joinedload(Post.author)
            )  # Загружаем связанного автора
            result = await session.execute(query)
            return result.scalars().all()

    @classmethod
    async def add(
        cls,
        title: str,
        content: str,
        author_id: int,
        image_url: Optional[str] = None,
        discord_url: Optional[str] = None,
    ) -> Post:
        async with async_session_maker() as session:
            post = Post(
                title=title,
                content=content,
                author_id=author_id,
                image_url=image_url,
                discord_url=discord_url,
                created_at=datetime.now(),  # Устанавливаем текущую дату и время
            )
            session.add(post)
            await session.commit()
            await session.refresh(post)
            return post

    @classmethod
    async def find_one_or_none(cls, **filters):
        async with async_session_maker() as session:
            query = (
                select(Post)
                .options(joinedload(Post.author))  # Жадная загрузка автора
                .filter_by(**filters)
            )
            result = await session.execute(query)
            return result.scalars().first()
