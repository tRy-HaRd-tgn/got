import os
from datetime import datetime
from fastapi import UploadFile, HTTPException
from pathlib import Path

UPLOAD_DIR = "app/static/images"  # Папка для загрузки изображений


class FileService:
    @staticmethod
    async def save_image(file: UploadFile, prefix: str, entity_id: int) -> str:
        """
        Сохраняет изображение с уникальным именем, связанным с сущностью (пост, донат и т.д.).
        Если старое изображение существует, оно будет удалено.

        :param file: Файл изображения.
        :param prefix: Префикс для имени файла (например, "post" или "donation").
        :param entity_id: ID сущности (поста, доната и т.д.).
        :return: Путь к сохраненному изображению.
        """
        try:
            # Генерируем уникальное имя файла
            file_extension = file.filename.split(".")[-1]
            filename = f"{prefix}_{entity_id}.{file_extension}"
            file_path = os.path.join(UPLOAD_DIR, filename)

            # Удаляем старое изображение (если оно существует)
            if os.path.exists(file_path):
                os.remove(file_path)

            # Сохраняем новое изображение
            with open(file_path, "wb") as buffer:
                buffer.write(await file.read())

            return f"/static/images/{filename}"

        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Ошибка при сохранении изображения: {str(e)}"
            )

    @staticmethod
    def delete_image(image_url: str) -> None:
        """
        Удаляет изображение по его URL.

        :param image_url: URL изображения.
        """
        try:
            if image_url:
                # Извлекаем имя файла из URL
                filename = image_url.replace("/static/images/", "")
                file_path = os.path.join(UPLOAD_DIR, filename)

                # Удаляем файл, если он существует
                if os.path.exists(file_path):
                    os.remove(file_path)
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Ошибка при удалении изображения: {str(e)}"
            )
