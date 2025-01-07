from typing import Optional
from sqlalchemy import select
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
