from datetime import datetime
from enum import Enum
from typing import Optional, List
from uuid import UUID
from pydantic import BaseModel, EmailStr

class SizeEnum(str, Enum):
    LARGE = "LARGE"
    MEDIUM = "MEDIUM"
    SMALL = "SMALL"

class StatusEnum(str, Enum):
    NO_VERIFICADO = "NO_VERIFICADO"
    POR_VERIFICAR = "POR_VERIFICAR"
    VERIFICADO = "VERIFICADO"



class Point(BaseModel):
    airportCode: str
    country: str

class Route(BaseModel):
    id: Optional[UUID]
    flightId: str 
    origin: Point
    destiny: Point
    bagCost: int

class Offer(BaseModel):
    id: UUID
    userId: UUID
    description: str
    size: SizeEnum
    fragile : bool
    offer: float
    score: float
    createdAt: datetime
    

class Rf005(BaseModel):
    id:Optional[UUID]
    expireAt: datetime
    route: Route
    plannedStartDate: datetime
    plannedEndDate: datetime
    createdAt: datetime
    offers: List[Offer]


class DataOut(BaseModel):
    data: Rf005


class UserMeOut(BaseModel):
    id: UUID
    username: str
    email: EmailStr
    fullName: Optional[str] = None
    dni: Optional[str] = None
    phoneNumber: Optional[str] = None
    status: StatusEnum




