from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, EmailStr, Field

class Location(BaseModel):
    airportCode: str
    country: str

class RouteA(BaseModel):
    id: str
    createdAt: str

class Route(BaseModel):
    id: Optional[UUID]
    flightId: str
    sourceAirportCode: str
    sourceCountry: str
    destinyAirportCode: str
    destinyCountry: str
    bagCost: int
    plannedStartDate: datetime
    plannedEndDate: datetime
    expireAt: datetime

class CreateRouteIn(BaseModel):
    flightId: str
    sourceAirportCode: str
    sourceCountry: str
    destinyAirportCode: str
    destinyCountry: str
    bagCost: int
    plannedStartDate: str
    plannedEndDate: str

class Rf003In(BaseModel):
    flightId: str
    expireAt: datetime
    plannedStartDate: datetime
    plannedEndDate: datetime
    origin: Location
    destiny: Location
    bagCost: int

class CreatePostIn(BaseModel):
    routeId: str
    expireAt: str

class PostCreateOut(BaseModel):
    id: UUID
    userId: UUID
    createdAt: datetime

class CreateRouteOut(BaseModel):
    id: str

class PostData(BaseModel):
    id:Optional[UUID]
    userId: UUID
    createdAt: datetime
    expireAt: datetime
    route: RouteA

class Rf003Out(BaseModel):
    data: PostData
    msg: str



