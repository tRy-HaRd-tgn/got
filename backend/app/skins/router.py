from pathlib import Path
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from app.users.dependencies import get_current_user
from app.models import User
from app.skins.dependencies import SkinService
from app.users.dao import UsersDAO
from fastapi.responses import FileResponse
from app.skins.dependencies import extract_face
from fastapi_cache.decorator import cache

from app.images.dependencies import FileService

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
        # Проверяем формат файла
        if not skin.filename.endswith(".png"):
            raise HTTPException(
                status_code=400, detail="Изображение должно быть в формате PNG"
            )

        # Проверяем размер файла (максимум 1 МБ)
        if skin.size > 1024 * 1024:
            raise HTTPException(
                status_code=400,
                detail="Размер изображения не должен превышать 1 МБ",
            )

        # Сохраняем скин на сервере
        skin_url = await FileService.save_image(
            file=skin, entity_type="skin", login=current_user.login
        )

        # Извлекаем аватарку
        avatar_path = Path(f"app/static/skins/{current_user.login}_face.png")
        extract_face(Path(f"app/static/skins/{current_user.login}.png"), avatar_path)

        # Обновляем URL скина в профиле пользователя
        await UsersDAO.update(
            current_user.id, skin_url=skin_url, avatar_url=str(avatar_path)
        )

        return {
            "message": "Скин успешно загружен",
            "skin_url": skin_url,
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
    Возвращает скин текущего пользователя.
    Если скин не загружен, возвращает базовый скин (steve.png).
    """
    # Путь к скину пользователя
    skin_path = Path(f"app/static/skins/{current_user.login}.png")

    # Если скин пользователя не существует, возвращаем базовый скин
    if not skin_path.exists():
        base_skin_path = Path("app/static/skins/steve.png")
        if not base_skin_path.exists():
            raise HTTPException(status_code=404, detail="Базовый скин не найден")
        return FileResponse(base_skin_path)

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
