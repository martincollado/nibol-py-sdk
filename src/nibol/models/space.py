from pydantic import BaseModel
from typing import List, Optional


class Space(BaseModel):
    id: str
    type: str
    name: str
    pictures: List[str]
    order: int
    seats: int
    max_capacity: Optional[int]
    map_entities_total: int


class SpaceListResponse(BaseModel):
    __root__: List[Space]


class SpaceDetails(BaseModel):
    id: str
    type: str
    name: str
    pictures: List[str]
    description: Optional[str]
    map_entities: List[dict]
    building: str
    map: Optional[dict]
    seats: int
    max_capacity: Optional[int]
    map_entities_total: int
