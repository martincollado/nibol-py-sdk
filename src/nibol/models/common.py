from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class Coordinates(BaseModel):
    lat: float
    lng: float


class Position(BaseModel):
    address: Optional[str]
    country: Optional[str]
    additional: Optional[str]
    coordinates: Optional[Coordinates]
    timezone: Optional[str]


class ReservationTimeSlot(BaseModel):
    start: datetime
    end: datetime


class ActionHistory(BaseModel):
    date: datetime
    action: str
    note: Optional[str]


class Status(BaseModel):
    name: str
    description: Optional[str]
