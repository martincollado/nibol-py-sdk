from pydantic import BaseModel, Field, model_validator
from pydantic_core import PydanticCustomError
from typing import List, Optional
from nibol.models.common import Position, Coordinates, TimeSlot


class BuildingFeatures(BaseModel):
    rooms: bool
    visitors: bool
    deliveries: bool


class BuildingSettings(BaseModel):
    availability_opening_time: dict
    availability_weekdays: List[int]
    closings: List[dict]
    wifi: dict


class BuildingRequest(BaseModel):
    building_id: str = Field(..., description="The ID of the building.")

    @model_validator(mode="after")
    def check_building_id(cls, values):
        if not values.building_id:
            raise PydanticCustomError(
                "missing_building_id",
                "The 'building_id' field is required to fetch building details.",
            )
        return values


class Building(BaseModel):
    id: str
    name: str
    position: Position
    features: BuildingFeatures
    settings: BuildingSettings


class BuildingAvailability(BaseModel):
    type: str
    mapEntityCategory: str
    id: str
    name: str
    space: str
    building: str
    coordinates: List[Coordinates]
    space_name: str
    building_name: str
    status: str
    reservation_slots: List[dict]
    time_slots: List[TimeSlot]
    seats: int


class BuildingAvailabilityRequest(BaseModel):
    building_id: Optional[str] = Field(None, description="The ID of the building.")
    date: Optional[str] = Field(None, description="The date to check availability (YYYY-MM-DD).")
    category: Optional[str] = Field(None, description="The category to check availability for (e.g., 'rooms').")

    @model_validator(mode="after")
    def check_required_fields(cls, values):
        if not values.building_id or not values.date or not values.category:
            raise PydanticCustomError(
                "missing_fields",
                "The fields 'building_id', 'date', and 'category' are required to fetch building availability.",
            )
        return values
