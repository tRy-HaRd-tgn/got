from datetime import datetime
import uuid
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
            transaction_id = str(uuid.uuid4())  # Генерируем уникальный transaction_id
            payment = PaymentHistory(
                user_id=user_id,
                transaction_id=transaction_id,  # Указываем transaction_id
                amount=amount,
                status=status,
                created_at=datetime.utcnow(),
            )
            session.add(payment)
            await session.commit()
            await session.refresh(payment)
            return payment
