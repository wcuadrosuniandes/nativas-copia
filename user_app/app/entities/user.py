from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import UUID, uuid4
from pydantic import BaseModel, EmailStr, Field as PField
from sqlalchemy import Column, String
from sqlalchemy_utils import ChoiceType
from sqlmodel import SQLModel, Field


class StatusEnum(str, Enum):
    NO_VERIFICADO = "NO_VERIFICADO"
    POR_VERIFICAR = "POR_VERIFICAR"
    VERIFICADO = "VERIFICADO"


class User(SQLModel, table=True):
    id: Optional[UUID] = Field(default=uuid4(), primary_key=True)
    username: str = Field(unique=True)
    email: str = Field(unique=True)
    phoneNumber: Optional[str] = None
    dni: Optional[str] = None
    fullName: Optional[str] = None
    password: str
    salt: str
    token: Optional[UUID] = None
    status: StatusEnum = Field(
        sa_column=Column(
            ChoiceType(StatusEnum, impl=String()),
            nullable=False,
            default=StatusEnum.NO_VERIFICADO,
        )
    )
    expireAt: Optional[datetime] = None
    createdAt: datetime = Field(default=datetime.utcnow())
    updateAt: datetime = Field(default=datetime.utcnow())


class UserCreateIn(BaseModel):
    username: str = PField(pattern=r"^[a-zA-Z0-9]+$")
    email: EmailStr
    password: str
    phoneNumber: Optional[str] = None
    dni: Optional[str] = None
    fullName: Optional[str] = None


class UserCreateOut(BaseModel):
    id: UUID
    createdAt: datetime


class UserUpdateIn(BaseModel):
    status: Optional[StatusEnum] = None
    phoneNumber: Optional[str] = None
    dni: Optional[str] = None
    fullName: Optional[str] = None


class UserAuthIn(BaseModel):
    username: str
    password: str


class UserAuthOut(BaseModel):
    id: UUID
    token: UUID
    expireAt: datetime


class UserMeOut(BaseModel):
    id: UUID
    username: str
    email: EmailStr
    fullName: Optional[str] = None
    dni: Optional[str] = None
    phoneNumber: Optional[str] = None
    status: StatusEnum
