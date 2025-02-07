import uuid
from datetime import datetime
from typing import Optional
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
        order_id: str,  # добавляем параметр order_id
        status: str = "pending",
    ) -> PaymentHistory:
        """
        Создает новую запись платежа с переданным order_id,
        сохраняет платеж в базе данных и возвращает созданный объект.
        """
        async with async_session_maker() as session:
            try:
                payment = PaymentHistory(
                    user_id=user_id,
                    transaction_id=order_id,  # используем переданный order_id
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
        """
        Ищет платеж по переданным фильтрам.
        """
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**filters)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def update(cls, payment_id: int, **values) -> Optional[PaymentHistory]:
        """
        Обновляет поля платежа с заданным ID.
        """
        async with async_session_maker() as session:
            try:
                payment = await session.get(cls.model, payment_id)
                if not payment:
                    return None

                for key, value in values.items():
                    setattr(payment, key, value)

                session.add(payment)
                await session.commit()
                await session.refresh(payment)
                return payment
            except SQLAlchemyError as e:
                await session.rollback()
                raise ValueError(f"Ошибка при обновлении платежа: {e}")

    @classmethod
    async def get_by_order_id(cls, order_id: str) -> Optional[PaymentHistory]:
        """
        Ищет платеж, используя уникальный идентификатор order_id (transaction_id).
        """
        async with async_session_maker() as session:
            query = select(cls.model).where(cls.model.transaction_id == order_id)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def update_status(
        cls, order_id: str, new_status: str
    ) -> Optional[PaymentHistory]:
        """
        Обновляет статус платежа, найденного по order_id.
        Можно расширить логику обновления, добавив сохранение дополнительных данных,
        полученных в callback от платежной системы.
        """
        async with async_session_maker() as session:
            query = select(cls.model).where(cls.model.transaction_id == order_id)
            result = await session.execute(query)
            payment = result.scalar_one_or_none()
            if not payment:
                return None

            payment.status = new_status
            session.add(payment)
            await session.commit()
            await session.refresh(payment)
            return payment
