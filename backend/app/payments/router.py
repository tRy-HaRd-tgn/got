import hashlib
import uuid
from fastapi import APIRouter, Depends, HTTPException, Form, Response
from app.users.dependencies import get_current_user
from app.models import User
from app.payments.dao import PaymentsDAO  # Ваш DAO для работы с платежами
from app.users.dao import UsersDAO
from app.payments.schemas import PaymentResponse
from app.config import settings

router = APIRouter(prefix="/payments", tags=["Payments"])

FREKASSA_URL = "https://pay.free-kassa.ru/"


def generate_signature(amount: float, order_id: str) -> str:
    """
    Генерирует подпись для формы оплаты:
       merchant_id:amount:secret_word:order_id
    """
    data = f"{settings.FREKASSA_MERCHANT_ID}:{amount}:{settings.FREKASSA_SECRET_WORD}:{order_id}"
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
    intid: str = Form(
        ...
    ),  # Номер операции Free-Kassa (можно сохранить для логирования)
    merchant_order_id: str = Form(..., alias="MERCHANT_ORDER_ID"),
    p_email: str = Form(..., alias="P_EMAIL"),
    p_phone: str = Form(None, alias="P_PHONE"),
    cur_id: str = Form(..., alias="CUR_ID"),
    sign: str = Form(..., alias="SIGN"),
    us_key: str = Form(None),  # дополнительные параметры, если приходят
    payer_account: str = Form(..., alias="payer_account"),
    commission: float = Form(..., alias="commission"),
):
    """
    Обрабатывает callback от Free-Kassa после успешной оплаты.
    Проверяет корректность подписи (с использованием второго секретного слова),
    обновляет статус платежа, пополняет баланс пользователя и возвращает "YES".
    """
    # Проверяем, что MERCHANT_ID соответствует нашему
    if merchant_id != settings.FREKASSA_MERCHANT_ID:
        raise HTTPException(status_code=400, detail="Неверный MERCHANT_ID")

    # Генерируем ожидаемую подпись для callback
    expected_signature = generate_callback_signature(amount, merchant_order_id)
    if sign != expected_signature:
        raise HTTPException(status_code=400, detail="Неверная подпись")

    # Получаем транзакцию по order_id
    transaction = await PaymentsDAO.get_by_order_id(merchant_order_id)
    if not transaction:
        raise HTTPException(status_code=404, detail="Транзакция не найдена")

    # Если транзакция уже обработана, возвращаем YES (чтобы Free-Kassa прекратила повторы)
    if transaction.status != "pending":
        return Response("YES", media_type="text/plain")

    # Обновляем статус транзакции на "success"
    await PaymentsDAO.update_status(merchant_order_id, "success")

    # Обновляем баланс пользователя
    user = await UsersDAO.find_one_or_none(id=transaction.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    user.balance += amount
    await UsersDAO.update(user.id, balance=user.balance)

    # Возвращаем "YES" для подтверждения успешной обработки
    return Response("YES", media_type="text/plain")
