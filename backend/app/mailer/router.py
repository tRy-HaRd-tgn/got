from fastapi import APIRouter, HTTPException

from app.mailer.mailer import confirm_token
from app.users.dao import UsersDAO
from app.skins.dependencies import SkinService
from fastapi.responses import RedirectResponse

router = APIRouter(tags=["Mailer"])


@router.get("/confirm-email")
async def confirm_email(token: str):
    """
    Подтверждает email пользователя и создает базовый скин и аватарку.
    """
    email = confirm_token(token)
    if not email:
        raise HTTPException(status_code=400, detail="Неверный или устаревший токен")

    user = await UsersDAO.find_one_or_none(email=email)
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")

    try:
        # Создаем базовый скин и аватарку
        skin_url = await SkinService.create_base_skin(user.login)

        # Обновляем данные пользователя
        await UsersDAO.update(
            user.id,
            skin_url=skin_url,
            avatar_url=f"/static/skins/{user.login}_face.png",
            is_verified=True,
        )

        return RedirectResponse(url="https://tortugagot.com/logReg")

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Ошибка при подтверждении email: {str(e)}"
        )
