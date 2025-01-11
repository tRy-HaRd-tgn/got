import os
from fastapi import UploadFile, HTTPException
from PIL import Image
from pathlib import Path


class FileService:
    @staticmethod
    async def save_image(file: UploadFile, entity_type: str, entity_id: int) -> str:
        """
        Сохраняет изображение для поста или доната.
        :param file: Файл изображения.
        :param entity_type: Тип сущности ("post" или "donation").
        :param entity_id: ID сущности (поста или доната).
        :return: Путь к сохраненному изображению.
        """
        try:
            # Проверяем формат файла
            if not file.filename.endswith(".png"):
                raise HTTPException(
                    status_code=400, detail="Изображение должно быть в формате PNG"
                )

            # Проверяем размер файла (максимум 1 МБ)
            if file.size > 1024 * 1024:
                raise HTTPException(
                    status_code=400,
                    detail="Размер изображения не должен превышать 1 МБ",
                )

            # Читаем изображение
            img = Image.open(file.file)

            # Проверяем размер изображения
            if entity_type == "skin" and img.size not in [
                (64, 64),
                (128, 128),
                (256, 256),
            ]:
                raise HTTPException(
                    status_code=400,
                    detail="Размер изображения должен быть 64x64, 128x128 или 256x256 пикселей",
                )

            # Определяем папку для сохранения
            upload_dir = Path(f"app/static/{entity_type}s")
            upload_dir.mkdir(parents=True, exist_ok=True)

            # Формируем имя файла
            filename = f"{entity_id}.png"
            file_path = upload_dir / filename

            # Удаляем старое изображение (если есть)
            if file_path.exists():
                file_path.unlink()

            # Сохраняем новое изображение
            img.save(file_path)

            return f"/static/{entity_type}s/{filename}"

        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Ошибка при сохранении изображения: {str(e)}"
            )

    @staticmethod
    def delete_image(entity_type: str, entity_id: int) -> None:
        """
        Удаляет изображение для поста или доната.
        :param entity_type: Тип сущности ("post" или "donation").
        :param entity_id: ID сущности (поста или доната).
        """
        try:
            file_path = Path(f"app/static/{entity_type}s/{entity_id}.png")
            if file_path.exists():
                file_path.unlink()
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Ошибка при удалении изображения: {str(e)}"
            )
