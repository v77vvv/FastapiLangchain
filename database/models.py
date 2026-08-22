from .connection import Base
from sqlalchemy import String, ForeignKey, Enum, Date
from enum import Enum as PyEnum
from sqlalchemy.orm import mapped_column, Mapped, relationship
from datetime import date

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
    status: Mapped[StatusChoices] = mapped_column(Enum(StatusChoices), default=StatusChoices.BASIC)
    registered_date: Mapped[date] = mapped_column(Date, default=date.today)

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