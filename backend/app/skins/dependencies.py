import os
from fastapi import UploadFile, HTTPException
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

UPLOAD_DIR = "app/static/skins"  # Папка для загрузки скинов
BASE_FONT = "arial.ttf"  # Шрифт для базового изображения


class SkinService:
    @staticmethod
    async def create_base_skin(username: str) -> str:
        """
        Создает базовый скин и аватарку для пользователя.
        :param username: Логин пользователя.
        :return: URL скина.
        """
        try:
            # Путь для сохранения скина и аватарки
            skin_path = Path(f"app/static/skins/{username}.png")
            avatar_path = Path(f"app/static/skins/{username}_face.png")

            # Создаем базовый скин (например, загружаем шаблон)
            base_skin = Image.new(
                "RGBA", (64, 64), (255, 255, 255, 255)
            )  # Белый квадрат как пример
            base_skin.save(skin_path)

            # Создаем аватарку на основе скина
            face = base_skin.crop((8, 8, 16, 16))  # Извлекаем область лица
            face = face.resize((64, 64), Image.NEAREST)  # Увеличиваем до 64x64
            face.save(avatar_path)

            # Возвращаем URL скина
            return f"/static/skins/{username}.png"

        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Ошибка при создании скина: {str(e)}"
            )

    @staticmethod
    async def upload_skin(username: str, skin: UploadFile) -> str:
        """
        Загружает скин для игрока.
        """
        try:
            # Проверяем формат файла
            if not skin.filename.endswith(".png"):
                raise HTTPException(
                    status_code=400, detail="Скин должен быть в формате PNG"
                )

            # Проверяем размер файла (максимум 1 МБ)
            if skin.size > 1024 * 1024:
                raise HTTPException(
                    status_code=400, detail="Размер скина не должен превышать 1 МБ"
                )

            # Читаем изображение
            img = Image.open(skin.file)

            # Проверяем размер изображения
            if (
                img.size != (64, 64)
                and img.size != (128, 128)
                and img.size != (256, 256)
            ):
                raise HTTPException(
                    status_code=400,
                    detail="Размер скина должен быть 64x64, 128x128 или 256x256 пикселей",
                )

            # Удаляем старый скин (если есть)
            old_skin_path = os.path.join(UPLOAD_DIR, f"{username}.png")
            if os.path.exists(old_skin_path):
                os.remove(old_skin_path)

            # Сохраняем новый скин
            filename = f"{username}.png"
            file_path = os.path.join(UPLOAD_DIR, filename)
            img.save(file_path)

            return f"/static/skins/{filename}"

        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Ошибка при загрузке скина: {str(e)}"
            )

    @staticmethod
    def get_skin_url(username: str) -> str:
        """
        Возвращает URL скина игрока.
        Если скин не загружен, возвращает URL базового изображения.
        """
        skin_path = os.path.join(UPLOAD_DIR, f"{username}.png")
        if os.path.exists(skin_path):
            return f"/static/skins/{username}.png"
        else:
            return f"/static/skins/{username}_base.png"


def extract_face(skin_path: str, output_path: str) -> str:
    """
    Извлекает лицо скина и сохраняет его как отдельное изображение.
    :param skin_path: Путь к файлу скина (64x64).
    :param output_path: Путь для сохранения аватарки.
    """
    # Открываем изображение скина
    skin = Image.open(skin_path)

    # Извлекаем область лица (8x8 пикселей)
    face = skin.crop((8, 8, 16, 16))

    # Увеличиваем лицо до 64x64 пикселей
    # face = face.resize((64, 64), Image.NEAREST)

    # Сохраняем аватарку
    face.save(output_path)
