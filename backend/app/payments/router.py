from fastapi import APIRouter, Depends, HTTPException

from app.models import User
from app.users.dependencies import get_current_user
from app.payments.dao import PaymentsDAO
from app.users.dao import UsersDAO
from app.payments.dependencies import generate_freekassa_payment_url


router = APIRouter(
    prefix="/payment",
    tags=["Payment"],
)


@router.post("/confirm")
async def confirm_payment(
    transaction_id: int,
    status: str,
    current_user: User = Depends(get_current_user),
):
    transaction = await PaymentsDAO.find_one_or_none(id=transaction_id)
    if not transaction:
        raise HTTPException(status_code=404, detail="Транзакция не найдена")

    if transaction.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Нет доступа к этой транзакции")

    transaction.status = status
    await PaymentsDAO.update(transaction.id, status=status)

    if status == "success":
        current_user.balance += transaction.amount
        await UsersDAO.update(current_user.id, balance=current_user.balance)

    return {"message": f"Статус платежа обновлен: {status}"}


@router.post("/balance/top-up")
async def top_up_balance(
    amount: float,
    current_user: User = Depends(get_current_user),
):
    transaction = await PaymentsDAO.add(
        user_id=current_user.id,
        amount=amount,
        status="pending",  # Статус "в ожидании"
    )

    payment_url = generate_freekassa_payment_url(
        amount, transaction.id, current_user.email
    )

    return {
        "message": "Перейдите по ссылке для оплаты",
        "payment_url": payment_url,
    }
