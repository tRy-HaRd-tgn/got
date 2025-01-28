import hashlib
from app.config import settings


def generate_freekassa_payment_url(
    amount: float, transaction_id: int, email: str
) -> str:
    merchant_id = "ваш_merchant_id"
    secret_key = settings.SECRET_KEY
    order_id = str(transaction_id)
    currency = "RUB"
    email = email  # Можно получить из текущего пользователя

    # Формируем подпись
    sign = hashlib.md5(
        f"{merchant_id}:{amount}:{secret_key}:{currency}:{order_id}".encode()
    ).hexdigest()

    # Формируем URL для оплаты
    payment_url = f"https://pay.freekassa.ru/?m={merchant_id}&oa={amount}&o={order_id}&s={sign}&currency={currency}&em={email}"

    return payment_url
