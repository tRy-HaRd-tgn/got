from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from app.database import async_session_maker  # ваш async session maker
from app.models import PurchasedDonation
import datetime


class PurchasedDonationsDAO:
    @classmethod
    async def add(cls, user_id: int, donation_id: int) -> PurchasedDonation:
        """
        Создает запись о покупке доната.
        """
        async with async_session_maker() as session:
            try:
                purchased_donation = PurchasedDonation(
                    user_id=user_id,
                    donation_id=donation_id,
                    purchase_date=datetime.datetime.utcnow(),  # можно не указывать, если уже стоит default
                    is_active=True,
                )
                session.add(purchased_donation)
                await session.commit()
                await session.refresh(purchased_donation)
                return purchased_donation
            except SQLAlchemyError as e:
                await session.rollback()
                raise ValueError(f"Ошибка при добавлении купленного доната: {e}")

    @classmethod
    async def find_by_user_id(cls, user_id: int) -> list[PurchasedDonation]:
        """
        Находит все покупки донатов для заданного пользователя.
        """
        async with async_session_maker() as session:
            result = await session.execute(
                select(PurchasedDonation).where(PurchasedDonation.user_id == user_id)
            )
            return result.scalars().all()
