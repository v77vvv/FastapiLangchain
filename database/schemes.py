from enum import Enum
from pydantic import BaseModel, Field, EmailStr
from datetime import datetime

class StatusChoices(str, Enum):
    BASIC = 'Basic'
    PRO = 'Pro'

class UserRefreshScheme(BaseModel):
    refresh_token: str


class UserLoginScheme(BaseModel):
    username: str 
    password: str 


class UserCreateScheme(BaseModel):
    username: str = Field(min_length=3, max_length=30)
    email: EmailStr | None = None
    phone: str | None = None 
    password: str = Field(min_length=6, max_length=100)
    plan: StatusChoices = Field(default='Basic')

class UserResponseScheme(BaseModel):
    id: int 
    username: str
    email: EmailStr
    phone: str 
    password: str 
    plan: StatusChoices
    registered_date: datetime

class UserUpdateScheme(BaseModel):
    username: str | None = Field(default=None, min_length=3, max_length=30)
    email: EmailStr | None = None 
    phone: str | None = None
    password: str | None = Field(default=None, ge=6, le=100)


class ChatResponseScheme(BaseModel):
    title: str 
    created_at: datetime

class ChatCreateScheme(BaseModel):
    title: str | None = 'New dialogue'

class ChatUpdateScheme(BaseModel):
    title: str | None = None 


class ChatMessageResponseScheme(BaseModel):
    response: str 
    created_at: datetime

class ChatMessageCreateScheme(BaseModel):
    chat_id: int
    message: str = Field(max_length=10000)