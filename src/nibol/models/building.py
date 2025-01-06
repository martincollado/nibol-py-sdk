from pydantic import BaseModel
from typing import List
from nibol.models.common import Position


class BuildingFeatures(BaseModel):
    rooms: bool
    visitors: bool
    deliveries: bool


class BuildingSettings(BaseModel):
    availability_opening_time: dict
    availability_weekdays: List[int]
    closings: List[dict]
    wifi: dict


class Building(BaseModel):
    id: str
    name: str
    position: Position
    features: BuildingFeatures
    settings: BuildingSettings


class BuildingListResponse(BaseModel):
    __root__: List[Building]
