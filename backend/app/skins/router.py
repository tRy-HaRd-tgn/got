from pathlib import Path
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from app.users.dependencies import get_current_user
from app.models import User
from app.skins.dependencies import SkinService
from app.users.dao import UsersDAO
from fastapi.responses import FileResponse
from app.skins.dependencies import extract_face

from app.images.dependencies import FileService

router = APIRouter(
    prefix="/skins",
    tags=["Skins"],
)


@router.post("/upload-skin")
async def upload_skin(
    skin: UploadFile = File(...),  # Файл скина
    current_user: User = Depends(get_current_user),  # Текущий пользователь
):
    """
    Загружает скин для текущего пользователя и создает аватарку на его основе.
    """
    try:
        # Сохраняем скин на сервере
        skin_url = await SkinService.upload_skin(current_user.login, skin)

        # Получаем путь к аватарке
        avatar_url = SkinService.get_avatar_url(current_user.login)

        # Обновляем URL скина и аватарки в профиле пользователя
        await UsersDAO.update(current_user.id, skin_url=skin_url, avatar_url=avatar_url)

        return {
            "message": "Скин успешно загружен",
            "skin_url": skin_url,
            "avatar_url": avatar_url,
        }

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Ошибка при загрузке скина: {str(e)}"
        )


from fastapi.responses import FileResponse
from fastapi import HTTPException
from pathlib import Path


@router.get("/get-skin")
async def get_skin(current_user: User = Depends(get_current_user)):
    """
    Возвращает скин текущего пользователя с отключенным кешированием.
    """
    # Путь к скину пользователя
    skin_path = Path(f"app/static/skins/{current_user.login}.png")

    if not skin_path.exists():
        base_skin_path = Path("app/static/skins/steve.png")
        if not base_skin_path.exists():
            raise HTTPException(status_code=404, detail="Базовый скин не найден")
        return base_skin_path

    # response = FileResponse(skin_path, media_type="image/png")

    # Отключаем кеширование для скинов (мгновенные обновления)
    # response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    # response.headers["Pragma"] = "no-cache"
    # response.headers["Expires"] = "0"

    # response.headers["ETag"] = ""
    return skin_path


@router.get("/get-avatar")
async def get_avatar(current_user: User = Depends(get_current_user)):
    """
    Возвращает аватарку текущего пользователя.
    Если аватарка не существует, создает её на основе скина.
    Если скин не существует, возвращает базовую аватарку.
    """

    # Путь к аватарке пользователя
    avatar_path = Path(f"app/static/skins/{current_user.login}_face.png")

    if avatar_path.exists():
        return avatar_path

    skin_path = Path(f"app/static/skins/{current_user.login}.png")
    if skin_path.exists():
        extract_face(skin_path, avatar_path)
        return avatar_path

    base_avatar_path = Path("app/static/skins/steve_face.png")
    if base_avatar_path.exists():
        return base_avatar_path

    # Если базовая аватарка не найдена, возвращаем ошибку 404
    raise HTTPException(status_code=404, detail="Аватарка не найдена")
