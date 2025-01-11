from fastapi import APIRouter, HTTPException

from app.mailer.mailer import confirm_token
from app.users.dao import UsersDAO
from app.skins.dependencies import SkinService


router = APIRouter(tags=["Mailer"])


@router.get("/confirm-email")
async def confirm_email(token: str):
    email = confirm_token(token)
    if not email:
        raise HTTPException(status_code=400, detail="Неверный или устаревший токен")

    user = await UsersDAO.find_one_or_none(email=email)
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")

    # Создаем базовый скин
    skin_url = await SkinService.create_base_skin(user.login)

    await UsersDAO.update(user.id, skin_url=skin_url, is_verified=True)

    return {"message": "Email успешно подтверждён"}
