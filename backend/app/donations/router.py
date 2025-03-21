from datetime import datetime
import os
from pathlib import Path
from typing import Literal, Optional
from fastapi import APIRouter, Depends, Form, HTTPException, Response, UploadFile, File
from fastapi.responses import FileResponse
from app.donations.dao import DonationsDAO
from app.donations.schemas import DonationCreate, DonationResponse
from app.payments.dao import PaymentsDAO
from app.users.dao import UsersDAO
from app.users.dependencies import get_current_user
from app.models import User
from app.images.dependencies import FileService
import uuid
from fastapi_cache.decorator import cache

from app.donations.purchased_donations.dao import PurchasedDonationsDAO

router = APIRouter(prefix="/donations", tags=["Donations"])


@router.get("/", response_model=list[DonationResponse])
async def get_all_donations():
    donations = await DonationsDAO.find_all()
    result = []

    for donation in donations:
        # Формируем данные доната
        donation_data = {
            "id": donation.id,
            "name": donation.name,
            "price": donation.price,
            "category": donation.category,
            "description": donation.description,
            "background_color": donation.background_color,
            "image_url": f"/static/donations/donation_{donation.id}.png",  # Возвращаем URL для получения изображения
        }
        result.append(donation_data)

    return result


@router.get("/{category}", response_model=list[DonationResponse])
async def get_donations_by_category(
    category: Literal["privileges", "pets", "mounts", "other"]
):
    donations = await DonationsDAO.get_by_category(category)
    result = []

    for donation in donations:

        # Формируем данные доната
        donation_data = {
            "id": donation.id,
            "name": donation.name,
            "price": donation.price,
            "category": donation.category,
            "description": donation.description,
            "background_color": donation.background_color,
            "image_url": f"/static/donations/donation_{donation.id}.png",  # Возвращаем URL для получения изображения
        }
        result.append(donation_data)

    return result


@router.post("/{donation_id}/buy")
async def buy_donation(
    donation_id: int,
    current_user: User = Depends(get_current_user),
):
    # Получаем донат
    donation = await DonationsDAO.find_one_or_none(id=donation_id)
    if not donation:
        raise HTTPException(status_code=404, detail="Донат не найден")

    # Проверяем, достаточно ли средств на балансе
    if current_user.balance < donation.price:
        raise HTTPException(status_code=400, detail="Недостаточно средств")

    # Списываем сумму с баланса пользователя
    current_user.balance -= donation.price
    await UsersDAO.update(current_user.id, balance=current_user.balance)

    # Создаем запись о покупке доната
    purchased_donation = await PurchasedDonationsDAO.add(
        user_id=current_user.id,
        donation_id=donation_id,
    )

    return {
        "message": "Покупка успешно завершена",
        "purchased_donation_id": purchased_donation.id,
    }


@router.post("/", response_model=DonationResponse)
async def create_donation(
    name: str = Form(...),
    price: float = Form(...),
    category: Literal["privileges", "pets", "mounts", "other"] = Form(...),
    description: str = Form(None),
    background_color: str = Form(None),
    image: UploadFile = File(None),
    current_user: User = Depends(get_current_user),
):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=403, detail="Только админ может добавлять донаты"
        )

    # Сохраняем изображение (если есть)
    image_url = None
    if image:
        # Генерируем временное имя файла
        temp_entity_id = str(uuid.uuid4())
        image_url = await FileService.save_image(
            file=image, entity_type="donation", entity_id=temp_entity_id
        )

    # Создаем донат
    donation = await DonationsDAO.add(
        name=name,
        price=price,
        category=category,
        description=description,
        background_color=background_color,
        image_url=image_url,
    )

    if image_url:
        # Переименовываем файл
        old_image_path = Path(f"app/static/donations/donation_{temp_entity_id}.png")
        new_image_path = Path(f"app/static/donations/donation_{donation.id}.png")
        if old_image_path.exists():
            old_image_path.rename(new_image_path)

        # Обновляем URL изображения в базе данных
        new_image_url = f"/static/donations/donation_{donation.id}.png"
        await DonationsDAO.update(donation.id, image_url=new_image_url)

    return {
        "id": donation.id,
        "name": donation.name,
        "price": donation.price,
        "category": donation.category,
        "description": donation.description,
        "background_color": donation.background_color,
        "image_url": f"static/donations/donation_{donation.id}.png",  # Возвращаем URL для получения изображения
    }


@router.get("/{donation_id}/image")
async def get_donation_image(donation_id: int):
    """
    Возвращает изображение доната по его ID.
    Используется FileResponse для оптимальной отдачи файлов.
    """
    # Формируем путь к файлу изображения
    image_path = Path(f"app/static/donations/donation_{donation_id}.png")

    # Проверяем, существует ли файл
    if not image_path.exists():
        raise HTTPException(status_code=404, detail="Изображение доната не найдено")

    # Отдаем файл с соответствующими заголовками
    return FileResponse(image_path, media_type="image/png")


@router.put("/{donation_id}", response_model=DonationResponse)
async def update_donation(
    donation_id: int,
    name: Optional[str] = Form(None),
    price: Optional[float] = Form(None),
    category: Optional[Literal["privileges", "pets", "mounts", "other"]] = Form(None),
    description: Optional[str] = Form(None),
    background_color: Optional[str] = Form(None),
    image: Optional[UploadFile] = File(None),
    current_user: User = Depends(get_current_user),
):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=403, detail="Только админ может редактировать донаты"
        )

    donation = await DonationsDAO.find_one_or_none(id=donation_id)
    if not donation:
        raise HTTPException(status_code=404, detail="Донат не найден")

    # Обновляем изображение, если оно предоставлено
    image_url = donation.image_url
    if image:
        # Удаляем старое изображение, если оно есть
        if donation.image_url:
            FileService.delete_image(entity_type="donation", entity_id=donation_id)
        # Сохраняем новое изображение
        image_url = await FileService.save_image(
            file=image, entity_type="donation", entity_id=donation_id
        )

    # Обновляем донат
    updated_donation = await DonationsDAO.update(
        donation_id=donation_id,
        name=name,
        price=price,
        category=category,
        description=description,
        background_color=background_color,
        image_url=image_url,
    )

    if not updated_donation:
        raise HTTPException(status_code=500, detail="Не удалось обновить донат")

    return {
        "id": updated_donation.id,
        "name": updated_donation.name,
        "price": updated_donation.price,
        "category": updated_donation.category,
        "description": updated_donation.description,
        "background_color": updated_donation.background_color,
        "image_url": updated_donation.image_url,
    }


@router.delete("/{donation_id}")
async def delete_donation(
    donation_id: int,
    current_user: User = Depends(get_current_user),
):
    # Проверка прав доступа
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Только админ может удалять донаты")

    # Удаление доната
    deleted_donation = await DonationsDAO.delete(donation_id)
    if not deleted_donation:
        raise HTTPException(status_code=404, detail="Донат не найден")

    # Удаление изображения, если оно есть
    if deleted_donation.image_url:
        FileService.delete_image(entity_type="donation", entity_id=donation_id)

    return {"message": "Донат успешно удален", "id": deleted_donation.id}
