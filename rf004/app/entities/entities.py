from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, EmailStr, Field


class SizeEnum(str, Enum):
    LARGE = "LARGE"
    MEDIUM = "MEDIUM"
    SMALL = "SMALL"


class StatusEnum(str, Enum):
    NO_VERIFICADO = "NO_VERIFICADO"
    POR_VERIFICAR = "POR_VERIFICAR"
    VERIFICADO = "VERIFICADO"


class Rf004In(BaseModel):
    description: str = Field(
        max_length=140,
        description="Descripción de no más de 140 caracteres sobre el paquete a llevar.",
    )
    size: SizeEnum
    fragile: bool
    offer: float = Field(gt=0, description="El valor debe ser mayor a cero")


class CreateOfferIn(Rf004In):
    postId: str


class CreateOfferOut(BaseModel):
    id: UUID
    userId: UUID
    createdAt: datetime


class OfferData(BaseModel):
    id: UUID
    userId: UUID
    postId: UUID
    createdAt: datetime


class Rf004Out(BaseModel):
    data: OfferData
    msg: str


class PostGetOut(BaseModel):
    id: UUID
    userId: UUID
    routeId: UUID
    expireAt: datetime
    createdAt: datetime


class UserMeOut(BaseModel):
    id: UUID
    username: str
    email: EmailStr
    fullName: Optional[str] = None
    dni: Optional[str] = None
    phoneNumber: Optional[str] = None
    status: StatusEnum


class ScoreCreateIn(BaseModel):
    id: str
    offer: float
    postId: str
    size: SizeEnum
    bagCost: float


class RouteOut(BaseModel):
    id: Optional[UUID]
    flightId: str
    sourceAirportCode: str
    sourceCountry: str
    destinyAirportCode: str
    destinyCountry: str
    bagCost: int
    plannedStartDate: datetime
    plannedEndDate: datetime
    createdAt: datetime
