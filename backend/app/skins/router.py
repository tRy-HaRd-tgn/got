from pathlib import Path
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from app.users.dependencies import get_current_user
from app.models import User
from app.skins.dependencies import SkinService
from app.users.dao import UsersDAO
from fastapi.responses import FileResponse
from app.skins.dependencies import extract_face
from fastapi_cache.decorator import cache

router = APIRouter(
    prefix="/users",
    tags=["Skins"],
)


@router.post("/upload-skin")
async def upload_skin(
    skin: UploadFile = File(...),  # Файл скина
    current_user: User = Depends(get_current_user),  # Текущий пользователь
):
    """
    Загружает скин для текущего пользователя.
    """
    try:
        # Сохраняем скин на сервере
        skin_path = Path(f"app/static/skins/{current_user.login}.png")
        with open(skin_path, "wb") as buffer:
            buffer.write(await skin.read())

        # Извлекаем аватарку
        avatar_path = Path(f"app/static/skins/{current_user.login}_face.png")
        extract_face(skin_path, avatar_path)

        # Обновляем URL скина в профиле пользователя
        await UsersDAO.update(
            current_user.id, skin_url=str(skin_path), avatar_url=str(avatar_path)
        )

        return {
            "message": "Скин успешно загружен",
            "skin_url": str(skin_path),
            "avatar_url": str(avatar_path),
        }

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Ошибка при загрузке скина: {str(e)}"
        )


@router.get("/get-skin")
@cache(expire=120)
async def get_skin(current_user: User = Depends(get_current_user)):
    """
    Возвращает URL скина текущего пользователя.
    """
    # Формируем путь к файлу скина
    skin_path = Path(f"app/static/skins/{current_user.login}.png")

    # Проверяем, существует ли файл
    if not skin_path.exists():
        # Если скин не загружен, возвращаем базовое изображение
        skin_path = Path(f"app/static/skins/{current_user.login}_base.png")
        if not skin_path.exists():
            raise HTTPException(status_code=404, detail="Скин не найден")

    return FileResponse(skin_path)


@router.get("/avatar")
@cache(expire=300)
async def get_avatar(current_user: User = Depends(get_current_user)):
    """
    Возвращает аватарку текущего пользователя.
    """
    avatar_path = Path(f"app/static/skins/{current_user.login}_face.png")

    if not avatar_path.exists():
        raise HTTPException(status_code=404, detail="Аватарка не найдена")

    # Устанавливаем заголовки для кеширования на стороне клиента
    headers = {
        "Cache-Control": "public, max-age=300",  # Кешировать на 5 минут
        "ETag": str(
            avatar_path.stat().st_mtime
        ),  # Используем время изменения файла как ETag
    }

    return FileResponse(avatar_path, headers=headers)
