import os
from fastapi import UploadFile, HTTPException
from PIL import Image
from pathlib import Path


class FileService:
    @staticmethod
    async def save_image(
        file: UploadFile, entity_type: str, entity_id: int = None, login: str = None
    ) -> str:
        """
        Сохраняет изображение для поста, доната или скина.
        :param file: Файл изображения.
        :param entity_type: Тип сущности ("post", "donation" или "skin").
        :param entity_id: ID сущности (поста или доната). Не используется для скинов.
        :param login: Логин пользователя (используется только для скинов).
        :return: Путь к сохраненному изображению.
        """
        try:
            # Проверяем формат файла
            allowed_extensions = {".png", ".jpg", ".jpeg"}
            file_extension = os.path.splitext(file.filename)[1].lower()
            if file_extension not in allowed_extensions:
                raise HTTPException(
                    status_code=400,
                    detail="Изображение должно быть в формате PNG, JPG или JPEG",
                )

            # Проверяем размер файла (максимум 1 МБ)
            if file.size > 1024 * 1024:
                raise HTTPException(
                    status_code=400,
                    detail="Размер изображения не должен превышать 1 МБ",
                )

            # Читаем изображение
            img = Image.open(file.file)

            # Определяем папку для сохранения
            upload_dir = Path(f"app/static/{entity_type}s")
            upload_dir.mkdir(parents=True, exist_ok=True)

            # Формируем имя файла
            if entity_type == "skin":
                if not login:
                    raise HTTPException(
                        status_code=400,
                        detail="Для скина необходимо указать логин пользователя",
                    )
                filename = (
                    f"{login}{file_extension}"  # Скин сохраняется как login.{extension}
                )
            else:
                if not entity_id:
                    raise HTTPException(
                        status_code=400,
                        detail="Для поста или доната необходимо указать entity_id",
                    )
                filename = f"{entity_type}_{entity_id}{file_extension}"  # Пост или донат сохраняется как entity_type_entity_id.{extension}

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
            file_path = Path(f"app/static/{entity_type}s/{entity_type}_{entity_id}.png")
            if file_path.exists():
                file_path.unlink()
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Ошибка при удалении изображения: {str(e)}"
            )
