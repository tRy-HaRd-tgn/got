from datetime import datetime
from typing import Optional
import uuid
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from app.dao.base import BaseDAO
from app.models import PaymentHistory
from app.database import async_session_maker


class PaymentsDAO(BaseDAO):
    model = PaymentHistory

    @classmethod
    async def add(
        cls,
        user_id: int,
        amount: float,
        status: str = "pending",
    ) -> PaymentHistory:
        async with async_session_maker() as session:
            try:
                transaction_id = str(
                    uuid.uuid4()
                )  # Генерируем уникальный transaction_id
                payment = PaymentHistory(
                    user_id=user_id,
                    transaction_id=transaction_id,
                    amount=amount,
                    status=status,
                    created_at=datetime.utcnow(),
                )
                session.add(payment)
                await session.commit()
                await session.refresh(payment)
                return payment
            except SQLAlchemyError as e:
                await session.rollback()
                raise ValueError(f"Ошибка при добавлении платежа: {e}")

    @classmethod
    async def find_one_or_none(cls, **filters) -> Optional[PaymentHistory]:
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**filters)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def update(cls, payment_id: int, **values) -> Optional[PaymentHistory]:
        async with async_session_maker() as session:
            try:
                # Находим платеж по ID
                payment = await session.get(cls.model, payment_id)
                if not payment:
                    return None

                # Обновляем поля
                for key, value in values.items():
                    setattr(payment, key, value)

                session.add(payment)
                await session.commit()
                await session.refresh(payment)
                return payment
            except SQLAlchemyError as e:
                await session.rollback()
                raise ValueError(f"Ошибка при обновлении платежа: {e}")
