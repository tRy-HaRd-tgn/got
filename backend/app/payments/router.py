import hashlib
import uuid
from fastapi import APIRouter, Depends, HTTPException, Form, Request, Response
from app.users.dependencies import get_current_user
from app.models import User
from app.payments.dao import PaymentsDAO  # Ваш DAO для работы с платежами
from app.users.dao import UsersDAO
from app.payments.schemas import PaymentResponse
from app.config import settings
from typing import Optional

router = APIRouter(prefix="/payments", tags=["Payments"])

FREKASSA_URL = "https://pay.fk.money/"
ALLOWED_IPS = {"168.119.157.136", "168.119.60.227", "178.154.197.79", "51.250.54.238"}


def generate_signature(amount: float, order_id: str, currency: str = "RUB") -> str:
    """
    Формирует подпись для платежной формы:
      MD5(merchant_id:formatted_amount:secret_word:currency:order_id)

    Сумма форматируется с двумя знаками после запятой (например, 100.11 или 100.00).
    """
    formatted_amount = f"{amount:.2f}"  # например, 100 -> "100.00"
    data = f"{settings.FREKASSA_MERCHANT_ID}:{formatted_amount}:{settings.FREKASSA_SECRET_WORD.get_secret_value()}:{currency}:{order_id}"
    return hashlib.md5(data.encode("utf-8")).hexdigest()


def generate_callback_signature_raw(amount: str, order_id: str) -> str:
    """
    Формирует подпись для callback:
      MD5(merchant_id:amount:secret_word2:order_id)

    ВАЖНО: amount используем как строку, без дополнительного форматирования.
    """
    data = f"{settings.FREKASSA_MERCHANT_ID}:{amount}:{settings.FREKASSA_SECRET_WORD2.get_secret_value()}:{order_id}"
    return hashlib.md5(data.encode("utf-8")).hexdigest()


@router.post("/topup", response_model=PaymentResponse)
async def topup_balance(amount: float, current_user: User = Depends(get_current_user)):
    if amount <= 0:
        raise HTTPException(
            status_code=400, detail="Сумма пополнения должна быть положительной"
        )

    order_id = str(uuid.uuid4())
    # Создаём транзакцию с order_id
    transaction = await PaymentsDAO.add(
        user_id=current_user.id, amount=amount, status="pending", order_id=order_id
    )

    signature = generate_signature(amount, order_id, currency="RUB")

    payment_url = (
        f"{FREKASSA_URL}"
        f"?m={settings.FREKASSA_MERCHANT_ID}"
        f"&oa={amount}"
        f"&currency=RUB"
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
async def freekassa_callback(request: Request):
    # Проверка IP (для тестирования можно закомментировать)
    client_ip = request.client.host
    if client_ip not in ALLOWED_IPS:
        raise HTTPException(status_code=400, detail="Hacking attempt!")

    form_data = await request.form()

    # Извлекаем необходимые параметры (согласно документации)
    merchant_id: Optional[str] = form_data.get("MERCHANT_ID")
    amount: Optional[str] = form_data.get("AMOUNT")
    intid: Optional[str] = form_data.get("intid")  # Номер операции Free-Kassa
    merchant_order_id: Optional[str] = form_data.get("MERCHANT_ORDER_ID")
    p_email: Optional[str] = form_data.get("P_EMAIL")
    p_phone: Optional[str] = form_data.get("P_PHONE")
    cur_id: Optional[str] = form_data.get("CUR_ID")
    sign: Optional[str] = form_data.get("SIGN")
    us_key: Optional[str] = form_data.get("us_key")
    payer_account: Optional[str] = form_data.get("payer_account")
    commission: Optional[str] = form_data.get("commission")

    # Проверяем обязательные поля
    # if not all([merchant_id, amount, merchant_order_id, sign]):
    #     raise HTTPException(
    #         status_code=422, detail="Не все обязательные параметры переданы"
    #     )

    if merchant_id != settings.FREKASSA_MERCHANT_ID:
        raise HTTPException(status_code=400, detail="Неверный MERCHANT_ID")

    expected_sign = generate_callback_signature_raw(amount, merchant_order_id)
    if sign != expected_sign:
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
    try:
        user.balance += float(amount)
    except ValueError:
        raise HTTPException(status_code=400, detail="Неверный формат суммы")
    await UsersDAO.update(user.id, balance=user.balance)

    # Возвращаем "YES" для подтверждения корректной обработки уведомления
    return Response("YES", media_type="text/plain")
