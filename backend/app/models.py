from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    Boolean,
    ForeignKey,
    DateTime,
    Text,
)
from sqlalchemy.orm import relationship
from app.database import Base
import datetime
from sqlalchemy.sql import func


class Donation(Base):
    __tablename__ = "donations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)  # Название доната
    description = Column(String, nullable=True)  # Описание
    price = Column(Float, nullable=False)  # Цена
    image_url = Column(String, nullable=True)
    category = Column(
        String, nullable=False
    )  # Категория (Привилегии, Питомцы, Маунты, Разное)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)  # Дата создания
    background_color = Column(String, nullable=True)

    def __str__(self) -> str:
        return f"Донат {self.name}: {self.price} руб."


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    login = Column(String, unique=True, nullable=False, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    hashed_password = Column(String, nullable=False)
    skin_url = Column(String, nullable=True)
    avatar_url = Column(String, nullable=True)
    is_verified = Column(Boolean, default=False)  # Статус подтверждения
    balance = Column(Float, default=0.0)  # Баланс пользователя
    role = Column(String, default="user")  # "user" или "admin"
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    # Связь с другими таблицами
    posts = relationship("Post", back_populates="author")
    payment_history = relationship("PaymentHistory", back_populates="user")
    purchased_donations = relationship("PurchasedDonation", back_populates="user")

    def __str__(self) -> str:
        return f"Пользователь {self.login}, баланс: {self.balance:.2f} золота."


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)  # ID автора
    image_url = Column(String, nullable=True)
    discord_url = Column(String, nullable=True)  # URL Discord новости
    created_at = Column(DateTime(timezone=True))

    author = relationship("User", back_populates="posts")

    def __str__(self) -> str:
        return f"Новость: {self.title} от {self.created_at}"


class PaymentHistory(Base):
    __tablename__ = "payment_history"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(
        Integer, ForeignKey("users.id"), nullable=False
    )  # Связь с пользователем
    amount = Column(Float, nullable=False)  # Сумма пополнения
    transaction_id = Column(String, nullable=True)  # ID транзакции в платежной системе
    status = Column(
        String, default="pending"
    )  # Статус платежа (pending, success, failed)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)  # Дата пополнения

    # Связь с пользователем
    user = relationship("User", back_populates="payment_history")

    def __str__(self) -> str:
        return (
            f"Пополнение {self.amount} руб. от {self.user.login}, статус: {self.status}"
        )


class PurchasedDonation(Base):
    __tablename__ = "purchased_donations"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    donation_id = Column(Integer, ForeignKey("donations.id"), nullable=False)
    purchase_date = Column(DateTime, default=datetime.datetime.utcnow)  # Дата покупки
    is_active = Column(Boolean, default=True)

    user = relationship("User", back_populates="purchased_donations")
    donation = relationship("Donation")

    def __str__(self) -> str:
        return f"Купленный донат {self.donation.name} пользователем {self.user.login}"
