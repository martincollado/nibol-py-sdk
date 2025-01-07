from pydantic import BaseModel, Field, model_validator
from typing import List, Optional, Dict

from nibol.models.common import TimeSlot


class SpaceListRequest(BaseModel):
    building: str = Field(..., alias="building")

    @model_validator(mode="after")
    def validate_building(cls, values):
        if not values.building:
            raise ValueError("The 'building' field is required to filter spaces.")
        return values


class SpaceDetailsRequest(BaseModel):
    space_id: str = Field(..., description="The ID of the space.")

    @model_validator(mode="after")
    def validate_space_id(cls, values):
        if not values.space_id:
            raise ValueError("The 'space_id' field is required to fetch space details.")
        return values


class Space(BaseModel):
    id: str
    type: str
    name: str
    pictures: List[str]
    order: int
    seats: int
    max_capacity: Optional[int]
    map_entities_total: int = Field(..., alias="mapEntitiesTotal")


class SpaceDetails(BaseModel):
    id: str
    type: str
    name: str
    pictures: List[str]
    description: Optional[str]
    map_entities: List[Dict] = Field(..., alias="mapEntities")  # Usar alias para mapear nombres
    building: str
    map: Optional[Dict]
    seats: int
    max_capacity: Optional[int]
    map_entities_total: int = Field(..., alias="mapEntitiesTotal")  # Usar alias para mapear nombres


class SpaceAvailability(BaseModel):
    id: str
    type: str
    mapEntityCategory: str
    name: str
    space: str
    building: str
    coordinates: List[Dict]
    space_name: str
    building_name: str
    status: str
    reservation_slots: List[Dict]
    time_slots: List[TimeSlot]
    seats: Optional[int] = 0
    max_capacity: Optional[int] = 0


class SpaceAvailabilityRequest(BaseModel):
    space_id: str = Field(..., description="The ID of the space.")
    date: str = Field(..., description="The date to check availability (YYYY-MM-DD).")

    @classmethod
    def validate_request(cls, space_id: str, date: str) -> "SpaceAvailabilityRequest":
        if not space_id:
            raise ValueError("The 'space_id' field is required to fetch space availability.")
        if not date:
            raise ValueError("The 'date' field is required to fetch space availability.")
        return cls(space_id=space_id, date=date)
