from datetime import datetime
from typing import Optional
from sqlalchemy import delete, insert, select, update
from app.dao.base import BaseDAO
from sqlalchemy.orm import joinedload
from app.models import Post
from app.database import async_session_maker


class PostsDAO(BaseDAO):
    model = Post

    @classmethod
    async def find_all(cls):
        """
        Возвращает все посты с загрузкой автора.
        """
        async with async_session_maker() as session:
            query = select(Post).options(joinedload(Post.author))
            result = await session.execute(query)
            return result.scalars().all()

    @classmethod
    async def add(
        cls,
        title: str,
        content: str,
        author_id: int,
        discord_url: Optional[str] = None,
        image_url: Optional[str] = None,  # Добавляем параметр image_url
    ) -> Post:
        """
        Добавляет новый пост и возвращает его.
        """
        async with async_session_maker() as session:
            post = Post(
                title=title,
                content=content,
                author_id=author_id,
                discord_url=discord_url,
                image_url=image_url,  # Передаем image_url
                created_at=datetime.now(),
            )
            session.add(post)
            await session.commit()
            await session.refresh(post)
            return post

    @classmethod
    async def find_one_or_none(cls, **filters):
        """
        Возвращает один пост по фильтрам с загрузкой автора.
        """
        async with async_session_maker() as session:
            query = select(Post).options(joinedload(Post.author)).filter_by(**filters)
            result = await session.execute(query)
            return result.scalars().first()

    @classmethod
    async def update(
        cls,
        post_id: int,
        title: Optional[str] = None,
        content: Optional[str] = None,
        discord_url: Optional[str] = None,
        image_url: Optional[str] = None,
    ) -> Optional[Post]:
        """
        Обновляет пост по его ID.
        Возвращает обновленный пост или None, если пост не найден.
        """
        async with async_session_maker() as session:
            update_data = {}
            if title is not None:
                update_data["title"] = title
            if content is not None:
                update_data["content"] = content
            if discord_url is not None:
                update_data["discord_url"] = discord_url
            if image_url is not None:
                update_data["image_url"] = image_url

            if update_data:
                query = (
                    update(Post)
                    .where(Post.id == post_id)
                    .values(**update_data)
                    .returning(Post)
                )
                result = await session.execute(query)
                await session.commit()
                updated_post = result.scalars().first()
                return updated_post

            return None

    @classmethod
    async def delete(cls, post_id: int) -> Optional[Post]:
        """
        Удаляет пост по его ID.
        Возвращает удаленный пост или None, если пост не найден.
        """
        async with async_session_maker() as session:
            query = select(Post).where(Post.id == post_id)
            result = await session.execute(query)
            post = result.scalars().first()

            if post:
                delete_query = delete(Post).where(Post.id == post_id)
                await session.execute(delete_query)
                await session.commit()
                return post

            return None
