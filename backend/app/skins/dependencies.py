import os
from fastapi import UploadFile, HTTPException
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

UPLOAD_DIR = "app/static/skins"  # Папка для загрузки скинов
BASE_FONT = "arial.ttf"  # Шрифт для базового изображения


def extract_face(skin_path: Path, avatar_path: Path):
    """
    Извлекает аватарку (лицо) из скина и сохраняет её.
    :param skin_path: Путь к файлу скина.
    :param avatar_path: Путь для сохранения аватарки.
    """
    try:
        # Открываем скин
        skin = Image.open(skin_path)

        # Извлекаем область лица (пример для скинов Minecraft)
        face = skin.crop((8, 8, 16, 16))  # Координаты области лица
        face = face.resize((64, 64), Image.BICUBIC)  # Увеличиваем до 64x64

        # Сохраняем аватарку
        face.save(avatar_path)

        # Логируем успешное извлечение
        print(f"Аватарка сохранена: {avatar_path}")

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Ошибка при извлечении аватарки: {str(e)}"
        )


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

            # Путь к базовому скину (steve.png)
            base_skin_path = Path("app/static/skins/steve.png")

            # Если базовый скин существует, копируем его
            if base_skin_path.exists():
                base_skin = Image.open(base_skin_path)
                base_skin.save(skin_path)
            else:
                # Создаем базовый скин (белый квадрат)
                base_skin = Image.new("RGBA", (64, 64), (255, 255, 255, 255))
                base_skin.save(skin_path)

            # Создаем аватарку на основе скина
            extract_face(skin_path, avatar_path)

            # Возвращаем URL скина
            return f"/static/skins/{username}.png"

        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Ошибка при создании скина: {str(e)}"
            )

    @staticmethod
    async def upload_skin(username: str, skin: UploadFile) -> str:
        """
        Загружает скин для игрока и создает аватарку на его основе.
        """
        try:
            # Проверяем формат файла
            if not skin.filename.endswith(".png"):
                raise HTTPException(
                    status_code=400, detail="Скин должен быть в формате PNG"
                )

            # Проверяем размер файла (максимум 1 МБ)
            file_size = await skin.read()
            if len(file_size) > 1024 * 1024:
                raise HTTPException(
                    status_code=400, detail="Размер скина не должен превышать 1 МБ"
                )
            # Вернуть указатель в начало файла, иначе Image.open(skin.file) сломается
            # skin.file.seek(0)

            # Читаем изображение
            img = Image.open(skin.file)
            img.verify()
            # skin.file.seek(0)
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

            # Удаляем старый скин и аватарку (если есть)
            old_skin_path = os.path.join(UPLOAD_DIR, f"{username}.png")
            old_avatar_path = os.path.join(UPLOAD_DIR, f"{username}_face.png")
            if os.path.exists(old_skin_path):
                os.remove(old_skin_path)
            if os.path.exists(old_avatar_path):
                os.remove(old_avatar_path)

            # Сохраняем новый скин
            filename = f"{username}.png"
            file_path = os.path.join(UPLOAD_DIR, filename)
            img.save(file_path)

            # Создаем аватарку на основе нового скина
            extract_face(Path(file_path), Path(old_avatar_path))

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
            return f"/static/skins/steve.png"

    @staticmethod
    def get_avatar_url(username: str) -> str:
        """
        Возвращает URL аватарки игрока.
        Если аватарка не существует, создает её на основе скина.
        """
        avatar_path = os.path.join(UPLOAD_DIR, f"{username}_face.png")
        if os.path.exists(avatar_path):
            return f"/static/skins/{username}_face.png"
        else:
            # Если аватарка не существует, создаем её на основе скина
            skin_path = os.path.join(UPLOAD_DIR, f"{username}.png")
            if os.path.exists(skin_path):
                extract_face(Path(skin_path), Path(avatar_path))
                return f"/static/skins/{username}_face.png"
            else:
                # Если скин тоже не существует, возвращаем базовую аватарку
                base_avatar_path = os.path.join(UPLOAD_DIR, "steve_face.png")
                if os.path.exists(base_avatar_path):
                    return f"/static/skins/steve_face.png"
                else:
                    raise HTTPException(
                        status_code=404, detail="Базовая аватарка не найдена"
                    )
