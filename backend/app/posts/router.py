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


@router.put("/posts/{post_id}", response_model=PostResponse)
async def update_post(
    post_id: int,  # ID поста для редактирования
    title: str = Form(None),  # Новый заголовок (опционально)
    content: str = Form(None),  # Новое содержание (опционально)
    discord_url: str = Form(None),  # Новая ссылка на Discord (опционально)
    image: UploadFile = File(
        None, max_size=1024 * 1024
    ),  # Новое изображение (опционально)
    current_user: User = Depends(get_current_user),  # Текущий пользователь
):
    """
    Редактирование существующего поста.
    Доступно только для пользователей с ролью "admin".
    """
    # Проверяем, что текущий пользователь — админ
    if current_user.role != "admin":
        raise HTTPException(
            status_code=403, detail="Только админ может редактировать новости"
        )

    # Проверяем, существует ли пост
    post = await PostsDAO.find_one_or_none(id=post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Пост не найден")

    # Обновляем изображение, если оно предоставлено
    image_url = post.image_url
    if image:
        try:
            # Генерируем уникальное имя файла
            file_extension = image.filename.split(".")[-1]
            filename = f"{datetime.now().strftime('%Y%m%d%H%M%S')}.{file_extension}"
            file_path = os.path.join(UPLOAD_DIR, filename)

            # Сохраняем файл
            with open(file_path, "wb") as buffer:
                buffer.write(await image.read())

            image_url = f"/static/images/{filename}"
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Ошибка при загрузке изображения: {str(e)}"
            )

    try:
        # Обновляем пост через DAO
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
            "author_login": updated_post.author.login,  # Теперь author загружен
            "image_url": updated_post.image_url,
            "created_at": updated_post.created_at.strftime("%d.%m.%Y"),
        }

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Ошибка при обновлении поста: {str(e)}"
        )
