from .connection import Base
from sqlalchemy import String, ForeignKey, Enum, Text
from enum import Enum as PyEnum
from sqlalchemy.orm import mapped_column, Mapped, relationship
from datetime import date
from typing import List
from datetime import datetime

class StatusChoices(str, PyEnum):
    BASIC = 'Basic'
    PRO = 'Pro'

class UserProfile(Base):
    __tablename__ = 'user_profile'

    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)
    username: Mapped[str] = mapped_column(String(30), nullable=False)
    email: Mapped[str | None] = mapped_column(nullable=True)
    phone: Mapped[str | None] = mapped_column(nullable=True)
    password: Mapped[str] = mapped_column(String(100), nullable=False)
    plan: Mapped[StatusChoices] = mapped_column(Enum(StatusChoices), 
                                                default=StatusChoices.BASIC,
                                                server_default='Basic')
    registered_date: Mapped[date] = mapped_column(default=date.today)

    user_refresh: Mapped['UserRefresh'] = relationship(back_populates='refresh_user',
                                                       cascade='all, delete-orphan')

    def __repr__(self):
        return super().__repr__()

class UserRefresh(Base):
    __tablename__ = 'user_refresh'

    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)
    user: Mapped[int] = mapped_column(ForeignKey('user_profile.id', ondelete='CASCADE'), nullable=False)
    token: Mapped[str] = mapped_column(nullable=False)

    refresh_user: Mapped[UserProfile] = relationship(back_populates='user_refresh')

    def __repr__(self):
        return super().__repr__()

class Chat(Base):
    __tablename__ = 'chat'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user_profile.id", ondelete="CASCADE"), nullable=False, index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=True, default="Новый диалог")
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)

    messages: Mapped[List["ChatMessage"]] = relationship("ChatMessage", back_populates="chat", cascade="all, delete-orphan")

class ChatMessage(Base):
    __tablename__ = 'chat_message'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    chat_id: Mapped[int] = mapped_column(ForeignKey("chat.id", ondelete="CASCADE"), nullable=False, index=True)
    message: Mapped[str] = mapped_column(Text, nullable=False)
    response: Mapped[str] = mapped_column()
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)

    chat: Mapped["Chat"] = relationship("Chat", back_populates="messages")