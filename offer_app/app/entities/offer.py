from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import UUID, uuid4
from pydantic import BaseModel
from sqlalchemy import Column, Float, String, Boolean
from sqlmodel import SQLModel, Field
from sqlalchemy_utils import ChoiceType


class SizeEnum(str, Enum):
    LARGE = "LARGE"
    MEDIUM = "MEDIUM"
    SMALL = "SMALL"


class Offer(SQLModel, table=True):
    id: Optional[UUID] = Field(default=uuid4(), primary_key=True)
    userId: UUID
    postId: UUID
    description: str
    size: SizeEnum = Field(
        sa_column=Column(
            ChoiceType(SizeEnum, impl=String()),
            nullable=False
        )
    )
    fragile: bool
    offer: float
    createdAt: datetime = Field(default=datetime.utcnow())

class OfferCreateIn(BaseModel):
    postId: str
    description: str = Field(max_length=140, description="Descripción de no más de 140 caracteres sobre el paquete a llevar.")
    size: SizeEnum
    fragile: bool
    offer: float = Field(gt=0, description="El valor debe ser mayor a cero")
    

class OfferCreateOut(BaseModel):
    id: UUID
    userId: UUID
    createdAt: datetime

class OfferViewFilterOut(BaseModel):
    id: UUID
    postId: str
    description: str
    size: SizeEnum
    fragile : bool
    offer: float
    createdAt: datetime
    userId: UUID
