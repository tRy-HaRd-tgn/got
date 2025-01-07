from typing import Optional
from sqlalchemy import select, update
from app.dao.base import BaseDAO
from app.models import Donation
from app.database import async_session_maker


class DonationsDAO(BaseDAO):
    model = Donation

    @classmethod
    async def add(
        cls,
        name: str,
        price: float,
        category: str,
        description: Optional[str] = None,
        image_url: Optional[str] = None,
    ) -> Donation:
        async with async_session_maker() as session:
            donation = Donation(
                name=name,
                price=price,
                category=category,
                description=description,
                image_url=image_url,
            )
            session.add(donation)
            await session.commit()
            await session.refresh(donation)
            return donation

    @classmethod
    async def get_by_category(cls, category: str) -> list[Donation]:
        async with async_session_maker() as session:
            query = select(Donation).where(Donation.category == category)
            result = await session.execute(query)
            return result.scalars().all()

    @classmethod
    async def find_all(cls) -> list[Donation]:
        async with async_session_maker() as session:
            query = select(Donation)  # Выбираем все объекты Donation
            result = await session.execute(query)
            return result.scalars().all()  # Возвращаем список объектов Donation

    @classmethod
    async def update(
        cls,
        donation_id: int,
        name: Optional[str] = None,
        price: Optional[float] = None,
        category: Optional[str] = None,
        description: Optional[str] = None,
        image_url: Optional[str] = None,
    ) -> Optional[Donation]:
        """
        Обновление доната по его ID.
        Возвращает обновленный донат или None, если донат не найден.
        """
        async with async_session_maker() as session:
            # Формируем словарь с обновляемыми полями
            update_data = {}
            if name is not None:
                update_data["name"] = name
            if price is not None:
                update_data["price"] = price
            if category is not None:
                update_data["category"] = category
            if description is not None:
                update_data["description"] = description
            if image_url is not None:
                update_data["image_url"] = image_url

            # Если есть что обновлять
            if update_data:
                query = (
                    update(Donation)
                    .where(Donation.id == donation_id)
                    .values(**update_data)
                    .returning(Donation)
                )
                result = await session.execute(query)
                await session.commit()
                updated_donation = result.scalars().first()
                return updated_donation

            # Если ничего не обновлялось, возвращаем None
            return None
