import hashlib
import uuid
from fastapi import APIRouter, Depends, HTTPException, Form
from app.users.dependencies import get_current_user
from app.models import User
from app.payments.dao import PaymentsDAO  # Ваш DAO для работы с платежами
from app.users.dao import UsersDAO
from app.payments.schemas import PaymentResponse

router = APIRouter(prefix="/payments", tags=["Payments"])

# Здесь нужно указать реальные данные, полученные от FreeKassa
FREKASSA_MERCHANT_ID = "ВАШ_MERCHANT_ID"
FREKASSA_SECRET_WORD = "ВАШ_SECRET_WORD"
FREKASSA_URL = "https://pay.free-kassa.ru/"


def generate_signature(amount: float, order_id: str) -> str:
    """
    Генерирует подпись в соответствии с требованиями FreeKassa.
    Обычно FreeKassa требует хеширования строки вида:
      merchant_id:amount:secret_word:order_id
    """
    data = f"{FREKASSA_MERCHANT_ID}:{amount}:{FREKASSA_SECRET_WORD}:{order_id}"
    signature = hashlib.md5(data.encode("utf-8")).hexdigest()
    return signature


@router.post("/topup", response_model=PaymentResponse)
async def topup_balance(
    amount: float = Form(...), current_user: User = Depends(get_current_user)
):
    """
    Инициирует пополнение баланса.
    Пользователь указывает сумму пополнения.
    Создаётся транзакция с уникальным order_id, затем формируется URL для оплаты.
    """
    if amount <= 0:
        raise HTTPException(
            status_code=400, detail="Сумма пополнения должна быть положительной"
        )

    # Создаем уникальный order_id для платежа
    order_id = str(uuid.uuid4())

    # Создаем запись транзакции с суммой и статусом "pending".
    # Метод PaymentsDAO.add должен сохранять информацию о платеже,
    # например, поля: user_id, amount, status, order_id и т.д.
    transaction = await PaymentsDAO.add(
        user_id=current_user.id, amount=amount, status="pending", order_id=order_id
    )

    # Генерируем подпись для FreeKassa
    signature = generate_signature(amount, order_id)

    # Формируем URL для оплаты по документации FreeKassa.
    # Обычно URL содержит параметры:
    #   m  - merchant_id,
    #   oa - сумма платежа,
    #   o  - order_id,
    #   s  - сгенерированная подпись,
    #   lang - язык (опционально).
    payment_url = f"{FREKASSA_URL}?m={FREKASSA_MERCHANT_ID}&oa={amount}&o={order_id}&s={signature}&lang=ru"

    return {
        "payment_url": payment_url,
        "order_id": order_id,
        "message": "Перейдите по ссылке для оплаты",
    }


@router.post("/freekassa-callback")
async def freekassa_callback(
    order_id: str = Form(...),
    amount: float = Form(...),
    s: str = Form(...),
    # Можно добавить и другие параметры, если они приходят от FreeKassa
):
    """
    Обрабатывает callback от FreeKassa после успешной оплаты.
    Проверяет корректность подписи, обновляет статус платежа и пополняет баланс пользователя.
    """
    expected_signature = generate_signature(amount, order_id)
    if s != expected_signature:
        raise HTTPException(status_code=400, detail="Неверная подпись")

    # Получаем транзакцию по order_id
    transaction = await PaymentsDAO.get_by_order_id(order_id)
    if not transaction:
        raise HTTPException(status_code=404, detail="Транзакция не найдена")

    # Если транзакция уже обработана, можно просто вернуть сообщение
    if transaction.status != "pending":
        return {"message": "Транзакция уже обработана"}

    # Обновляем статус транзакции на "success"
    await PaymentsDAO.update_status(order_id, "success")

    # Обновляем баланс пользователя
    user = await UsersDAO.find_one_or_none(id=transaction.user_id)

    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    user.balance += amount
    await UsersDAO.update(user.id, balance=user.balance)

    return {"message": "Баланс успешно пополнен"}
