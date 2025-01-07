from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from app.models import User
from app.posts.dao import PostsDAO
from app.posts.schemas import PostCreate, PostResponse
from app.users.dependecies import get_current_user
from datetime import datetime
import os

from app.images.dependencies import FileService

router = APIRouter(
    prefix="/posts",
    tags=["Posts"],
)

UPLOAD_DIR = "app/static/images"


@router.get("/posts/{post_id}", response_model=PostResponse)
async def get_post(
    post_id: int,
):
    post = await PostsDAO.find_one_or_none(id=post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Пост не найден")

    return {
        "id": post.id,
        "title": post.title,
        "content": post.content,
        "discord_url": post.discord_url,
        "author_login": post.author.login,  # Теперь author загружен
        "image_url": post.image_url,
        "created_at": post.created_at.strftime("%d.%m.%Y"),
    }


@router.get("/posts", response_model=list[PostResponse])
async def get_posts():
    posts = await PostsDAO.find_all()
    return [
        {
            "id": post.id,
            "title": post.title,
            "content": post.content,
            "discord_url": post.discord_url,
            "author_login": post.author.login,
            "image_url": post.image_url,
            "created_at": post.created_at.strftime("%d.%m.%Y"),
        }
        for post in posts
    ]


@router.post("/", response_model=PostResponse)
async def create_post(
    title: str = Form(...),
    content: str = Form(...),
    discord_url: str = Form(...),
    image: UploadFile = File(None),
    current_user: User = Depends(get_current_user),
):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=403, detail="Только админ может добавлять новости"
        )

    # Сохраняем изображение (если есть)
    image_url = None
    if image:
        image_url = await FileService.save_image(
            image, prefix="post", entity_id=0
        )  # entity_id будет обновлен после создания поста

    # Создаем пост
    post = await PostsDAO.add(
        title=title,
        content=content,
        author_id=current_user.id,
        image_url=image_url,
        discord_url=discord_url,
    )

    # Обновляем имя файла с учетом ID поста
    if image_url:
        new_image_url = await FileService.save_image(
            image, prefix="post", entity_id=post.id
        )
        await PostsDAO.update(post.id, image_url=new_image_url)

    return {
        "id": post.id,
        "title": post.title,
        "content": post.content,
        "discord_url": post.discord_url,
        "author_login": current_user.login,
        "image_url": new_image_url if image_url else None,
        "created_at": post.created_at.strftime("%d.%m.%Y"),
    }


@router.put("/posts/{post_id}", response_model=PostResponse)
async def update_post(
    post_id: int,
    title: str = Form(None),
    content: str = Form(None),
    discord_url: str = Form(None),
    image: UploadFile = File(None),
    current_user: User = Depends(get_current_user),
):
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
        # Удаляем старое изображение
        FileService.delete_image(post.image_url)
        # Сохраняем новое изображение
        image_url = await FileService.save_image(
            image, prefix="post", entity_id=post_id
        )

    # Обновляем пост
    updated_post = await PostsDAO.update(
        post_id=post_id,
        title=title,
        content=content,
        discord_url=discord_url,
        image_url=image_url,
    )

    if not updated_post:
        raise HTTPException(status_code=500, detail="Не удалось обновить пост")

    return {
        "id": updated_post.id,
        "title": updated_post.title,
        "content": updated_post.content,
        "discord_url": updated_post.discord_url,
        "author_login": updated_post.author.login,
        "image_url": updated_post.image_url,
        "created_at": updated_post.created_at.strftime("%d.%m.%Y"),
    }
