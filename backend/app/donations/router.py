from datetime import datetime
import os
from fastapi import APIRouter, Depends, Form, HTTPException, UploadFile, File
from app.donations.dao import DonationsDAO
from app.donations.schemas import DonationCreate, DonationResponse
from app.payments.dao import PaymentsDAO
from app.users.dao import UsersDAO
from app.users.dependencies import get_current_user
from app.models import User
from app.images.dependencies import FileService

router = APIRouter(prefix="/donations", tags=["Donations"])


@router.get("/", response_model=list[DonationResponse])
async def get_all_donations():
    donations = await DonationsDAO.find_all()
    return [
        {
            "id": donation.id,
            "name": donation.name,
            "price": donation.price,
            "category": donation.category,
            "description": donation.description,
        }
        for donation in donations
    ]


@router.get("/{category}", response_model=list[DonationResponse])
async def get_donations_by_category(category: str):
    donations = await DonationsDAO.get_by_category(category)
    return [
        {
            "id": donation.id,
            "name": donation.name,
            "price": donation.price,
            "category": donation.category,
            "description": donation.description,
            "image_url": donation.image_url,
        }
        for donation in donations
    ]


@router.post("/{donation_id}/buy")
async def buy_donation(
    donation_id: int,
    current_user: User = Depends(get_current_user),
):
    # Получаем донат
    donation = await DonationsDAO.find_one_or_none(id=donation_id)
    if not donation:
        raise HTTPException(status_code=404, detail="Донат не найден")

    # Проверяем баланс пользователя
    if current_user.balance < donation.price:
        raise HTTPException(status_code=400, detail="Недостаточно средств")

    # Создаем транзакцию
    transaction = await PaymentsDAO.add(
        user_id=current_user.id,
        amount=donation.price,
        status="pending",  # Статус "в ожидании"
    )

    # Обновляем баланс пользователя
    current_user.balance -= donation.price
    await UsersDAO.update(current_user.id, balance=current_user.balance)

    return {
        "message": "Покупка успешно завершена",
        "transaction_id": transaction.transaction_id,  # Возвращаем transaction_id
    }


@router.post("/", response_model=DonationResponse)
async def create_donation(
    name: str = Form(...),
    price: float = Form(...),
    category: str = Form(...),
    description: str = Form(None),
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
        image_url = await FileService.save_image(
            image, prefix="donation", entity_id=0
        )  # entity_id будет обновлен после создания доната

    # Создаем донат
    donation = await DonationsDAO.add(
        name=name,
        price=price,
        category=category,
        description=description,
        image_url=image_url,
    )

    # Обновляем имя файла с учетом ID доната
    if image_url:
        new_image_url = await FileService.save_image(
            image, prefix="donation", entity_id=donation.id
        )
        await DonationsDAO.update(donation.id, image_url=new_image_url)

    return {
        "id": donation.id,
        "name": donation.name,
        "price": donation.price,
        "category": donation.category,
        "description": donation.description,
        "image_url": new_image_url if image_url else None,
    }


@router.put("/{donation_id}", response_model=DonationResponse)
async def update_donation(
    donation_id: int,
    name: str = Form(None),
    price: float = Form(None),
    category: str = Form(None),
    description: str = Form(None),
    image: UploadFile = File(None),
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
        # Удаляем старое изображение
        FileService.delete_image(donation.image_url)
        # Сохраняем новое изображение
        image_url = await FileService.save_image(
            image, prefix="donation", entity_id=donation_id
        )

    # Обновляем донат
    updated_donation = await DonationsDAO.update(
        donation_id=donation_id,
        name=name,
        price=price,
        category=category,
        description=description,
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
        "image_url": updated_donation.image_url,
    }
