from pathlib import Path
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from app.users.dependencies import get_current_user
from app.models import User
from app.skins.dependencies import SkinService
from app.users.dao import UsersDAO
from fastapi.responses import FileResponse

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
        skin_url = await SkinService.upload_skin(current_user.login, skin)

        # Обновляем URL скина в профиле пользователя
        await UsersDAO.update(current_user.id)

        return {"message": "Скин успешно загружен", "skin_url": skin_url}

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Ошибка при загрузке скина: {str(e)}"
        )


@router.get("/get-skin")
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
