from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from app.models import User
from app.posts.dao import PostsDAO
from app.posts.schemas import PostCreate, PostResponse
from app.users.dependecies import get_current_user
from datetime import datetime
import os

router = APIRouter(
    prefix="/posts",
    tags=["Posts"],
)

UPLOAD_DIR = "app/static/images"


@router.post("/", response_model=PostResponse)
async def create_post(
    title: str = Form(...),
    content: str = Form(...),
    discord_url: str = Form(...),  # Discord URL
    image: UploadFile = File(..., max_size=1024 * 1024),
    current_user: User = Depends(get_current_user),
):
    # Проверяем, что текущий пользователь — админ
    if current_user.role != "admin":
        raise HTTPException(
            status_code=403, detail="Только админ может добавлять новости"
        )

    # Генерируем уникальное имя файла
    file_extension = image.filename.split(".")[-1]
    filename = f"{datetime.now().strftime('%Y%m%d%H%M%S')}.{file_extension}"
    file_path = os.path.join(UPLOAD_DIR, filename)

    # Сохраняем файл
    with open(file_path, "wb") as buffer:
        buffer.write(await image.read())

    # Создаем пост
    post = await PostsDAO.add(
        title=title,
        content=content,
        author_id=current_user.id,
        image_url=f"/static/images/{filename}",  # Сохраняем путь к изображению
        discord_url=discord_url,
    )

    return {
        "id": post.id,
        "title": post.title,
        "content": post.content,
        "discord_url": post.discord_url,
        "author_login": current_user.login,
        "image_url": post.image_url,
        "created_at": post.created_at.strftime("%d.%m.%Y"),
    }


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


# @router.post("/posts/{post_id}/upload-image")
# async def upload_image(
#     post_id: int,
#     file: UploadFile = File(..., max_size=1024 * 1024),
#     current_user: User = Depends(get_current_user),
# ):
#     if current_user.role != "admin":
#         raise HTTPException(
#             status_code=403, detail="Только админ может добавлять изображение к новости"
#         )
#     # Проверяем, существует ли пост
#     post = await PostsDAO.find_one_or_none(id=post_id)
#     if not post:
#         raise HTTPException(status_code=404, detail="Пост не найден")

#     # Генерируем уникальное имя файла
#     file_extension = file.filename.split(".")[-1]
#     filename = f"{datetime.now().strftime('%Y%m%d%H%M%S')}.{file_extension}"
#     file_path = os.path.join(UPLOAD_DIR, filename)

#     # Сохраняем файл
#     with open(file_path, "wb") as buffer:
#         buffer.write(await file.read())

#     # Обновляем пост с ссылкой на изображение
#     image_url = f"/static/images/{filename}"
#     await PostsDAO.update(post_id, image_url=image_url)

#     return {"message": "Изображение успешно загружено", "image_url": image_url}
