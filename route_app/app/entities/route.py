from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4
from pydantic import BaseModel, Field as PField 
from sqlalchemy import Column, String
from sqlmodel import SQLModel, Field


class Route(SQLModel, table=True ):
    id: Optional[UUID] = Field(default=uuid4(), primary_key=True)
    flightId: str 
    sourceAirportCode: str
    sourceCountry: str
    destinyAirportCode: str
    destinyCountry: str
    bagCost: int
    plannedStartDate: datetime
    plannedEndDate: datetime
    createdAt: datetime = Field(default=datetime.utcnow())
    updateAt: datetime = Field(default=datetime.utcnow())


class RouteCreateIn(BaseModel):
    flightId: str 
    sourceAirportCode: str
    sourceCountry: str
    destinyAirportCode: str
    destinyCountry: str
    bagCost: int
    plannedStartDate: datetime
    plannedEndDate: datetime


class RouteCreateOut(BaseModel):
    id: UUID
    createdAt: datetime

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

