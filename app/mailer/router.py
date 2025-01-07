from fastapi import APIRouter, HTTPException

from app.mailer.mailer import confirm_token
from app.users.dao import UsersDAO


router = APIRouter(tags=["Mailer"])


@router.get("/confirm-email")
async def confirm_email(token: str):
    email = confirm_token(token)
    if not email:
        raise HTTPException(status_code=400, detail="Неверный или устаревший токен")

    user = await UsersDAO.find_one_or_none(email=email)
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")

    await UsersDAO.update(user.id, is_verified=True)

    return {"message": "Email успешно подтверждён"}
