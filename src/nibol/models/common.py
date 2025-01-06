from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class Coordinates(BaseModel):
    lat: float
    lng: float


class TimeSlot(BaseModel):
    start: str
    end: str


class Position(BaseModel):
    address: str
    coordinates: dict
    timezone: str
    country: Optional[str] = None
    additional: Optional[str] = None


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
