import hashlib
import uuid
from fastapi import APIRouter, Depends, HTTPException, Form, Response
from app.users.dependencies import get_current_user
from app.models import User
from app.payments.dao import PaymentsDAO  # Ваш DAO для работы с платежами
from app.users.dao import UsersDAO
from app.payments.schemas import PaymentResponse
from app.config import settings
from typing import Optional

router = APIRouter(prefix="/payments", tags=["Payments"])

FREKASSA_URL = "https://pay.fk.money/"


def generate_signature(amount: float, order_id: str, currency: str = "RUB") -> str:
    """
    Генерирует подпись для формы оплаты:
      merchant_id:amount:secret_word:currency:order_id

    Форматируем сумму с двумя знаками после запятой, чтобы соответствовать примеру:
      md5('7012:100.11:secret:RUB:154')
    """
    formatted_amount = f"{amount:.2f}"  # например, 100 -> "100.00", 100.11 -> "100.11"
    data = f"{settings.FREKASSA_MERCHANT_ID}:{formatted_amount}:{settings.FREKASSA_SECRET_WORD}:{currency}:{order_id}"
    signature = hashlib.md5(data.encode("utf-8")).hexdigest()
    return signature


def generate_callback_signature(amount: float, order_id: str) -> str:
    """
    Генерирует подпись для проверки данных, пришедших на callback:
       merchant_id:amount:secret_word2:order_id
    """
    data = f"{settings.FREKASSA_MERCHANT_ID}:{amount}:{settings.FREKASSA_SECRET_WORD2}:{order_id}"
    signature = hashlib.md5(data.encode("utf-8")).hexdigest()
    return signature


@router.post("/topup", response_model=PaymentResponse)
async def topup_balance(
    amount: float = Form(...), current_user: User = Depends(get_current_user)
):
    """
    Инициирует пополнение баланса.
    Пользователь указывает сумму пополнения, генерируется уникальный order_id,
    создаётся транзакция, и формируется URL для оплаты.
    """
    if amount <= 0:
        raise HTTPException(
            status_code=400, detail="Сумма пополнения должна быть положительной"
        )

    # Генерируем уникальный order_id для платежа
    order_id = str(uuid.uuid4())

    # Создаем транзакцию с переданным order_id (используем его как transaction_id)
    transaction = await PaymentsDAO.add(
        user_id=current_user.id, amount=amount, status="pending", order_id=order_id
    )

    # Генерируем подпись для формы оплаты
    signature = generate_signature(amount, order_id)

    # Формируем URL для оплаты согласно документации Free-Kassa
    payment_url = (
        f"{FREKASSA_URL}"
        f"?m={settings.FREKASSA_MERCHANT_ID}"
        f"&oa={amount}"
        f"&currency=RUB"  # указываем валюту платежа
        f"&o={order_id}"
        f"&s={signature}"
        f"&lang=ru"
    )

    return {
        "payment_url": payment_url,
        "order_id": order_id,
        "message": "Перейдите по ссылке для оплаты",
    }


@router.post("/freekassa-callback")
async def freekassa_callback(
    merchant_id: str = Form(..., alias="MERCHANT_ID"),
    amount: float = Form(..., alias="AMOUNT"),
    intid: str = Form(...),  # Номер операции Free-Kassa
    merchant_order_id: str = Form(..., alias="MERCHANT_ORDER_ID"),
    p_email: str = Form(..., alias="P_EMAIL"),
    p_phone: Optional[str] = Form(None, alias="P_PHONE"),
    cur_id: Optional[str] = Form(None, alias="CUR_ID"),
    sign: str = Form(..., alias="SIGN"),
    us_key: Optional[str] = Form(None),  # дополнительные параметры, если приходят
    payer_account: Optional[str] = Form(None, alias="payer_account"),
    commission: Optional[float] = Form(None, alias="commission"),
):
    # Логирование входящих данных для отладки
    # Например: print(await request.form())

    # Проверяем, что MERCHANT_ID соответствует нашему
    if merchant_id != settings.FREKASSA_MERCHANT_ID:
        raise HTTPException(status_code=400, detail="Неверный MERCHANT_ID")

    # Генерируем ожидаемую подпись для callback (используем секретное слово 2)
    expected_signature = generate_callback_signature(amount, merchant_order_id)
    if sign != expected_signature:
        raise HTTPException(status_code=400, detail="Неверная подпись")

    # Получаем транзакцию по order_id
    transaction = await PaymentsDAO.get_by_order_id(merchant_order_id)
    if not transaction:
        raise HTTPException(status_code=404, detail="Транзакция не найдена")

    if transaction.status != "pending":
        return Response("YES", media_type="text/plain")

    # Обновляем статус транзакции и баланс пользователя
    await PaymentsDAO.update_status(merchant_order_id, "success")
    user = await UsersDAO.find_one_or_none(id=transaction.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    user.balance += amount
    await UsersDAO.update(user.id, balance=user.balance)

    return Response("YES", media_type="text/plain")
