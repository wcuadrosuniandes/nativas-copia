from enum import Enum
from uuid import UUID
from pydantic import BaseModel
from sqlalchemy import Column, String
from sqlmodel import SQLModel, Field
from sqlalchemy_utils import ChoiceType
from typing import ClassVar


class SizeEnum(str, Enum):
    LARGE = "LARGE"
    MEDIUM = "MEDIUM"
    SMALL = "SMALL"


class Score(SQLModel, table=True):
    id: UUID = Field(primary_key=True)
    userId: UUID
    postId: UUID
    offer: float = Field(nullable=False, default=0.0)
    size: SizeEnum = Field(
        sa_column=Column(ChoiceType(SizeEnum, impl=String()), nullable=False)
    )
    bagCost: float = Field(nullable=False, default=0.0)
    profit: float

    OCCUPATION_BAG_MAPPING: ClassVar[dict[SizeEnum, float]] = {
        SizeEnum.LARGE: 1.0,
        SizeEnum.MEDIUM: 0.5,
        SizeEnum.SMALL: 0.25,
    }

    def calculate_profit(_self):
        occupationPercentage = _self.OCCUPATION_BAG_MAPPING.get(_self.size, 0)
        _self.profit = _self.offer - (occupationPercentage * _self.bagCost)


class ScoreCreateIn(BaseModel):
    id: UUID
    offer: float
    postId: UUID
    size: SizeEnum
    bagCost: float

class ScoreOut(ScoreCreateIn):
    profit: float