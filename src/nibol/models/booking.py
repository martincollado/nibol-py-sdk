from pydantic import BaseModel, Field, constr
from typing import List, Optional, Annotated
from datetime import datetime
from nibol.models.common import ReservationTimeSlot, Position, ActionHistory


class BookingQuery(BaseModel):
    page: Optional[int] = Field(default=0, ge=0, description="Page starting from 0")
    limit: Optional[int] = Field(default=20, ge=1, le=100, description="Elements per page")
    start: Optional[datetime]
    end: Optional[datetime]
    mode: Optional[Annotated[str, constr(regex="^(office|remote|not_working)$")]]
    building: Optional[Annotated[str, constr(regex="^[a-f\\d]{24}$")]]
    space: Optional[Annotated[str, constr(regex="^[a-f\\d]{24}$")]]
    category: Optional[str]
    type: Optional[str]
    visitor: Optional[bool]


class BookingData(BaseModel):
    id: str = Field(..., regex="^[a-f\\d]{24}$")
    start: datetime
    end: datetime
    mode: str
    timezone: str
    created_by: str
    user: str
    active: bool
    deleted: bool
    statuses: List[str]
    history: List[ActionHistory]
    created_at: datetime
    venue: Optional[str]
    seats: Optional[int]
    position: Optional[Position]
    type: Optional[str]
    visitor: Optional[bool]
    map_entity: Optional[str]
    map_entity_name: Optional[str]
    space: Optional[str]
    welcome: Optional[dict]
    building: Optional[str]
    email: Optional[str]
    name: Optional[str]
    note: Optional[str]


class BookingCalendarResponse(BaseModel):
    page: int
    limit: int
    total: int
    data: List[BookingData]


class BookingCreateRequest(BaseModel):
    mode: str
    days: List[ReservationTimeSlot]
    map_entity_id: Annotated[str, constr(regex="^[a-f\\d]{24}$")]
    conference_link: Optional[Annotated[str, constr(max_length=200)]]
    attendees: Optional[List[str]]
    description: Optional[Annotated[str, constr(max_length=250)]]
    title: Optional[Annotated[str, constr(max_length=50)]]


class BookingResponseItem(BaseModel):
    start: datetime
    end: datetime
    status: bool
    error: Optional[str]


class BookingResponse(BaseModel):
    __root__: List[BookingResponseItem]
