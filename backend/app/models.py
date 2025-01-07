from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, DateTime
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
    category = Column(
        String, nullable=False
    )  # Категория (Привилегии, Питомцы, Маунты, Разное)
    image_url = Column(String, nullable=True)  # Ссылка на изображение
    created_at = Column(DateTime, default=datetime.datetime.utcnow)  # Дата создания

    def __str__(self) -> str:
        return f"Донат {self.name}: {self.price} руб."


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    login = Column(String, unique=True, nullable=False, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    hashed_password = Column(String, nullable=False)
    is_verified = Column(Boolean, default=False)  # Статус подтверждения
    balance = Column(Float, default=0.0)  # Баланс пользователя
    role = Column(String, default="user")  # "user" или "admin"
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    # Связь с другими таблицами
    posts = relationship("Post", back_populates="author")
    payment_history = relationship("PaymentHistory", back_populates="user")
    skins = relationship("Skin", back_populates="user")

    def __str__(self) -> str:
        return f"Пользователь {self.login}, баланс: {self.balance:.2f} золота."


class Skin(Base):
    __tablename__ = "skins"

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    file_path = Column(String, nullable=False)  # Путь к файлу скина
    uploaded_at = Column(DateTime, default=datetime.datetime.utcnow)

    # Связь с пользователем
    user = relationship("User", back_populates="skins")

    def __str__(self) -> str:
        return f"Скин пользователя {self.user_id}: {self.file_path}"


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)  # ID автора
    image_url = Column(String, nullable=True)  # URL изображения
    discord_url = Column(String, nullable=True)  # URL Discord новости
    created_at = Column(DateTime(timezone=True))

    author = relationship("User", back_populates="posts")

    def __str__(self) -> str:
        return f"Новость: {self.title} от {self.created_at}"


class PaymentHistory(Base):
    __tablename__ = "payment_history"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    transaction_id = Column(String, unique=True, nullable=False)  # Обязательное поле
    amount = Column(Float, nullable=False)
    status = Column(
        String, nullable=False, default="pending"
    )  # "pending", "paid", "failed"
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    # Связь с пользователем
    user = relationship("User", back_populates="payment_history")

    def __str__(self) -> str:
        return f"Платеж {self.transaction_id}: {self.status}"
