from typing import Optional
from app.config import settings
from fastapi_mail import FastMail, MessageSchema
from itsdangerous import URLSafeTimedSerializer
from fastapi_mail import ConnectionConfig

serializer = URLSafeTimedSerializer(settings.SECRET_KEY)

conf = ConnectionConfig(
    MAIL_USERNAME=settings.EMAIL_USERNAME,
    MAIL_PASSWORD=settings.EMAIL_PASSWORD.get_secret_value(),
    MAIL_FROM=settings.EMAIL_FROM,
    MAIL_PORT=settings.EMAIL_PORT,
    MAIL_SERVER=settings.EMAIL_SERVER,
    MAIL_SSL_TLS=False,
    MAIL_STARTTLS=True,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
)


async def send_confirmation_email(email: str, token: str):
    # Убедитесь, что используете правильный протокол и домен
    confirmation_url = f"http://127.0.0.1:8000/api/confirm-email?token={token}"

    # HTML-код с корректной ссылкой
    html_content = f"""
    <html>
        <body>
            <h1>Подтверждение регистрации</h1>
            <p>Для подтверждения регистрации перейдите по <a href="{confirmation_url}">ссылке</a>.</p>
            <p>Если ссылка не работает, скопируйте и вставьте следующий URL в браузер:</p>
            <p>{confirmation_url}</p>
        </body>
    </html>
    """

    # Создание сообщения
    message = MessageSchema(
        subject="Подтверждение регистрации",
        recipients=[email],
        body=html_content,
        subtype="html",  # Указываем тип содержимого как HTML
    )

    # Отправка сообщения
    fm = FastMail(conf)
    await fm.send_message(message)


def generate_confirmation_token(email: str) -> str:
    """Генерирует токен подтверждения."""
    return serializer.dumps(email, salt=settings.SALT)


def confirm_token(token: str, max_age: int = 3600) -> Optional[str]:
    """Проверяет токен подтверждения."""
    try:
        email = serializer.loads(token, salt=settings.SALT, max_age=max_age)
        return email
    except:
        return None
