from enum import Enum
from pydantic import BaseModel, Field, EmailStr
from datetime import date 

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
    password: str = Field(ge=6, le=100)
    status: StatusChoices = Field(default='Basic')

class UserResponseScheme(BaseModel):
    id: int 
    username: str
    email: EmailStr
    phone: str 
    password: str 
    status: StatusChoices
    registered_date: date

class UserUpdateScheme(BaseModel):
    username: str | None = Field(default=None, min_length=3, max_length=30)
    email: EmailStr | None = None 
    phone: str | None = None
    password: str | None = Field(default=None, ge=6, le=100)