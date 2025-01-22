from typing import Optional
from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, Response
from pathlib import Path

from fastapi.responses import FileResponse
from app.models import User
from app.posts.dao import PostsDAO
from app.posts.schemas import PostCreate, PostResponse
from app.users.dependencies import get_current_user
from datetime import datetime
from app.images.dependencies import FileService
from fastapi_cache.decorator import cache
import uuid
from app.database import async_session_maker

router = APIRouter(
    prefix="/posts",
    tags=["Posts"],
)


@router.get("/{post_id}", response_model=PostResponse)
async def get_post(post_id: int):
    """
    Возвращает информацию о посте по его ID.
    """
    post = await PostsDAO.find_one_or_none(id=post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Пост не найден")

    return {
        "id": post.id,
        "title": post.title,
        "content": post.content,
        "discord_url": post.discord_url,
        "author_login": post.author.login,
        "image_url": f"/static/posts/post_{post_id}.png",  # Возвращаем URL для получения изображения
        "created_at": post.created_at.strftime("%d.%m.%Y"),
    }


@router.get("/", response_model=list[PostResponse])
@cache(expire=300)
async def get_posts():
    """
    Возвращает список всех постов с URL для получения изображений.
    """
    posts = await PostsDAO.find_all()
    result = []

    for post in posts:
        # Формируем URL для получения изображения

        # Формируем данные поста
        post_data = {
            "id": post.id,
            "title": post.title,
            "content": post.content,
            "discord_url": post.discord_url,
            "author_login": post.author.login,
            "image_url": f"/static/posts/post_{post.id}.png",  # Возвращаем URL для получения изображения
            "created_at": post.created_at.strftime("%d.%m.%Y"),
        }
        result.append(post_data)

    return result


@router.post("/", response_model=PostResponse)
async def create_post(
    title: str = Form(...),
    content: str = Form(...),
    discord_url: str = Form(...),
    image: UploadFile = File(None),
    current_user: User = Depends(get_current_user),
):
    """
    Создает новый пост.
    """
    if current_user.role != "admin":
        raise HTTPException(
            status_code=403, detail="Только админ может добавлять новости"
        )

    # Сохраняем изображение (если есть)
    image_url = None
    if image:
        # Генерируем временное имя файла
        temp_entity_id = str(uuid.uuid4())
        image_url = await FileService.save_image(
            image, entity_type="post", entity_id=temp_entity_id
        )

    # Создаем пост
    post = await PostsDAO.add(
        title=title,
        content=content,
        author_id=current_user.id,
        discord_url=discord_url,
        image_url=image_url,
    )

    # Обновляем имя файла с учетом ID поста
    if image_url:
        # Переименовываем файл
        old_image_path = Path(f"app/static/posts/post_{temp_entity_id}.png")
        new_image_path = Path(f"app/static/posts/post_{post.id}.png")
        if old_image_path.exists():
            old_image_path.rename(new_image_path)

        # Обновляем URL изображения в базе данных
        new_image_url = f"/static/posts/post_{post.id}.png"
        await PostsDAO.update(post.id, image_url=new_image_url)

    return {
        "id": post.id,
        "title": post.title,
        "content": post.content,
        "discord_url": post.discord_url,
        "author_login": current_user.login,
        "image_url": f"/posts/{post.id}/image",  # Возвращаем URL для получения изображения
        "created_at": post.created_at.strftime("%d.%m.%Y"),
    }


@router.put("/{post_id}", response_model=PostResponse)
async def update_post(
    post_id: int,
    title: Optional[str] = Form(None),
    content: Optional[str] = Form(None),
    discord_url: Optional[str] = Form(None),
    image: Optional[UploadFile] = File(None),
    current_user: User = Depends(get_current_user),
):
    """
    Обновляет существующий пост.
    """
    if current_user.role != "admin":
        raise HTTPException(
            status_code=403, detail="Только админ может редактировать новости"
        )

    post = await PostsDAO.find_one_or_none(id=post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Пост не найден")

    # Обновляем изображение, если оно предоставлено
    image_url = post.image_url
    if image:
        # Удаляем старое изображение, если оно есть
        if post.image_url:
            FileService.delete_image(entity_type="post", entity_id=post_id)
        # Сохраняем новое изображение
        image_url = await FileService.save_image(
            image, entity_type="post", entity_id=post_id
        )

    # Обновляем пост
    updated_post = await PostsDAO.update(
        post_id=post_id,
        title=title,
        content=content,
        author_id=current_user.id,
        discord_url=discord_url,
        image_url=image_url,
    )

    if not updated_post:
        raise HTTPException(status_code=500, detail="Не удалось обновить пост")

    # Возвращаем обновленный пост
    return {
        "id": updated_post.id,
        "title": updated_post.title,
        "content": updated_post.content,
        "discord_url": updated_post.discord_url,
        "author_login": current_user.login,  # Используем current_user, так как автор обновлен
        "image_url": f"/posts/{post_id}/image",  # Возвращаем URL для получения изображения
        "created_at": updated_post.created_at.strftime("%d.%m.%Y"),
    }


@router.get("/{post_id}/image")
async def get_post_image(post_id: int):
    """
    Возвращает изображение поста по его ID.
    Используется FileResponse для оптимальной отдачи файлов.
    """
    # Формируем путь к файлу изображения
    image_path = Path(f"app/static/posts/post_{post_id}.png")

    # Проверяем, существует ли файл
    if not image_path.exists():
        raise HTTPException(status_code=404, detail="Изображение поста не найдено")

    # Отдаем файл с соответствующими заголовками
    return FileResponse(image_path)


@router.delete("/{post_id}")
async def delete_post(
    post_id: int,
    current_user: User = Depends(get_current_user),
):
    """
    Удаляет пост по его ID.
    """
    if current_user.role != "admin":
        raise HTTPException(
            status_code=403, detail="Только админ может удалять новости"
        )

    post = await PostsDAO.find_one_or_none(id=post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Пост не найден")

    # Удаляем изображение, если оно есть
    if post.image_url:
        FileService.delete_image(entity_type="post", entity_id=post_id)

    # Удаляем пост из базы данных
    deleted_post = await PostsDAO.delete(post_id)
    if not deleted_post:
        raise HTTPException(status_code=500, detail="Не удалось удалить пост")

    return {"message": "Пост успешно удален", "id": deleted_post.id}
