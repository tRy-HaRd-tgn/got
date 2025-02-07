import io
import os
import time
from fastapi import UploadFile, HTTPException
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

UPLOAD_DIR = "app/static/skins"  # Папка для загрузки скинов
BASE_FONT = "arial.ttf"  # Шрифт для базового изображения


def extract_face(skin_path: Path, avatar_path: Path, side: str = "front"):
    """
    Извлекает лицо из скина с учётом его разрешения.

    По умолчанию извлекается передняя часть головы, то есть берётся квадрат с координатами:
      - левый верхний угол: (skin.width/8, skin.width/8)
      - правый нижний угол: (skin.width/4, skin.width/4)

    Для задней части (side="back") берётся квадрат с координатами:
      - левый верхний угол: (3*skin.width/8, skin.width/8)
      - правый нижний угол: (skin.width/2, skin.width/4)

    :param skin_path: Путь к файлу скина.
    :param avatar_path: Путь для сохранения аватарки.
    :param side: "front" для передней части (по умолчанию) или "back" для задней.
    """
    try:
        skin = Image.open(skin_path)
        # Определяем «блок» как 1/8 от ширины скина (при стандартном скине 64 пикселя → 8 пикселей)
        block = int(skin.width / 8)

        if side == "front":
            # Переднее лицо: область (block, block, 2*block, 2*block)
            coords = (block, block, block * 2, block * 2)
        elif side == "back":
            # Заднее лицо: область (3*block, block, 4*block, 2*block)
            coords = (block * 3, block, block * 4, block * 2)
        else:
            raise ValueError("Параметр side должен быть 'front' или 'back'")

        face = skin.crop(coords)
        face.save(avatar_path)
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
        Загружает скин для игрока и создаёт аватарку (лицо) на его основе.
        Теперь имя файла включает таймштамп, чтобы URL менялся при каждом обновлении.
        """
        try:
            # Проверяем расширение файла
            if not skin.filename.endswith(".png"):
                raise HTTPException(
                    status_code=400, detail="Скин должен быть в формате PNG"
                )

            # Читаем файл в память
            file_content = await skin.read()
            if len(file_content) > 1024 * 1024:
                raise HTTPException(
                    status_code=400, detail="Размер скина не должен превышать 1 МБ"
                )

            # Открываем изображение
            img = Image.open(io.BytesIO(file_content))

            # Проверяем размер изображения
            # if img.size not in [(64, 64), (128, 128), (256, 256)]:
            #     raise HTTPException(
            #         status_code=400,
            #         detail="Размер скина должен быть 64x64, 128x128 или 256x256 пикселей",
            #     )

            # Папка для сохранения
            upload_dir = Path("app/static/skins")
            upload_dir.mkdir(parents=True, exist_ok=True)

            # Генерируем новое имя файла с таймштампом
            ts = int(time.time())
            new_filename = f"{username}_{ts}.png"
            skin_path = upload_dir / new_filename

            # Также сформируем имя для аватарки (лицо)
            avatar_filename = f"{username}_{ts}_face.png"
            avatar_path = upload_dir / avatar_filename

            # Если старые файлы существуют — можно их удалить.
            # Например, можно реализовать логику удаления всех файлов с именем username_*.png
            for file in upload_dir.glob(f"{username}_*.png"):
                file.unlink()

            # Сохраняем скин
            img.save(skin_path)

            # Создаём аватарку (лицо) без масштабирования – фронтенд сам масштабирует
            extract_face(skin_path, avatar_path)

            # Возвращаем URL для доступа (при условии, что /static/skins/ публично доступен)
            return f"/static/skins/{new_filename}"

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
