from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4
from pydantic import BaseModel
from sqlmodel import SQLModel, Field


class Post(SQLModel, table=True):
    id: Optional[UUID] = Field(default=uuid4(), primary_key=True)
    routeId: UUID
    userId: UUID
    expireAt: datetime
    createdAt: datetime = Field(default=datetime.utcnow())

class PostCreateIn(BaseModel):
    routeId: UUID
    expireAt: datetime

class PostCreateOut(BaseModel):
    id: UUID
    userId: UUID
    createdAt: datetime

class PostGetOut(BaseModel):
    id:Optional[UUID]
    userId: UUID
    routeId: UUID
    expireAt: datetime
    createdAt: datetime
