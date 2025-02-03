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
        avatar_url = skin_url.replace(".png", "_face.png")
        # Обновляем URL скина и аватарки в профиле пользователя
        await UsersDAO.update(current_user.id, skin_url=skin_url, avatar_url=avatar_url)

        return {
            "message": "Скин успешно загружен",
            "skin_url": skin_url,
        }

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Ошибка при загрузке скина: {str(e)}"
        )


@router.get("/get-skin")
async def get_skin(current_user: "User" = Depends(get_current_user)):
    """
    Отдаёт актуальный скин пользователя.
    Если файл скина не найден, возвращается базовый скин.
    URL возвращается относительно корня приложения (без "app/").
    """
    upload_dir = Path("app/static/skins")
    # Ищем файлы вида username_<timestamp>.png (без подстроки "face")
    skin_files = [
        f
        for f in upload_dir.glob(f"{current_user.login}_*.png")
        if "face" not in f.name
    ]

    if not skin_files:
        base_skin_path = Path("app/static/skins/steve.png")
        if not base_skin_path.exists():
            raise HTTPException(status_code=404, detail="Базовый скин не найден")
        return str(base_skin_path.relative_to("app"))

    # Выбираем последний (актуальный) файл
    skin_file = sorted(skin_files)[-1]
    return str(skin_file.relative_to("app"))


@router.get("/get-avatar")
async def get_avatar(current_user: "User" = Depends(get_current_user)):
    """
    Отдаёт актуальную аватарку (лицо) пользователя.
    Если аватарка не найдена, пытается создать её из скина.
    Если и скин отсутствует, возвращает базовую аватарку.
    URL возвращается относительно корня приложения (без "app/").
    """
    upload_dir = Path("app/static/skins")
    # Ищем файлы аватарки: username_<timestamp>_face.png
    avatar_files = list(upload_dir.glob(f"{current_user.login}_*_face.png"))
    if avatar_files:
        avatar_file = sorted(avatar_files)[-1]
        return str(avatar_file.relative_to("app"))

    # Если аватарка не найдена, попробуем извлечь её из скина
    skin_files = [
        f
        for f in upload_dir.glob(f"{current_user.login}_*.png")
        if "face" not in f.name
    ]
    if skin_files:
        skin_path = sorted(skin_files)[-1]
        # Определяем путь для нового файла аватарки
        avatar_path = upload_dir / f"{skin_path.stem}_face.png"
        extract_face(skin_path, avatar_path)
        return str(avatar_path.relative_to("app"))

    # Если ни скин, ни аватарка не найдены, отдаем базовую аватарку
    base_avatar_path = Path("app/static/skins/steve_face.png")
    if base_avatar_path.exists():
        return str(base_avatar_path.relative_to("app"))

    raise HTTPException(status_code=404, detail="Аватарка не найдена")
