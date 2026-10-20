"""Pydantic schemas shared by the API, the recommender and the layout solver.

Coordinate system: the room floor is the rectangle [0, width] x [0, length]
(metres), x to the right, z towards the viewer. A placed item is described by
the centre of its footprint and a rotation in degrees (0/90/180/270). At
rotation 0 the item's front faces +z, i.e. its back is towards the z = 0 wall.
"""

from enum import Enum

from pydantic import BaseModel, Field


class Style(str, Enum):
    scandinavian = "scandinavian"
    modern = "modern"
    classic = "classic"
    loft = "loft"
    minimalist = "minimalist"


class RoomType(str, Enum):
    living_room = "living_room"
    bedroom = "bedroom"
    office = "office"


class Wall(str, Enum):
    back = "back"  # z = 0
    front = "front"  # z = length
    left = "left"  # x = 0
    right = "right"  # x = width


class Door(BaseModel):
    wall: Wall
    offset: float = Field(..., ge=0, description="Distance from the wall start (x or z = 0) to the door centre, m")
    width: float = Field(0.9, gt=0.4, le=2.0)


class Room(BaseModel):
    width: float = Field(..., ge=2.0, le=10.0, description="Size along x, m")
    length: float = Field(..., ge=2.0, le=10.0, description="Size along z, m")
    height: float = Field(2.7, ge=2.2, le=4.0)
    doors: list[Door] = Field(default_factory=list)


class FurnitureItem(BaseModel):
    id: str
    name: str
    category: str
    styles: list[Style]
    width: float = Field(..., gt=0)
    depth: float = Field(..., gt=0)
    height: float = Field(..., gt=0)
    price: int = Field(..., ge=0, description="Price in KZT (demo data)")
    color: str = "#cccccc"
    against_wall: bool = False


class Placement(BaseModel):
    item_id: str
    x: float
    z: float
    rotation: int = Field(0, description="Degrees, one of 0, 90, 180, 270")


class Violation(BaseModel):
    kind: str  # "overlap" | "out_of_bounds" | "door_blocked" | "unknown_item"
    item_ids: list[str]
    message: str


class RecommendationRequest(BaseModel):
    room: Room
    room_type: RoomType = RoomType.living_room
    style: Style
    budget: int = Field(..., gt=0, description="Total budget, KZT")
    categories: list[str] | None = Field(None, description="Defaults to the typical set for room_type")
    top_k: int = Field(3, ge=1, le=10)


class Recommendation(BaseModel):
    item: FurnitureItem
    score: float
    reasons: list[str]


class CategoryRecommendations(BaseModel):
    category: str
    options: list[Recommendation]


class RecommendationResponse(BaseModel):
    categories: list[CategoryRecommendations]
    bundle: list[str] = Field(description="One item id per category, chosen to fit the total budget")
    bundle_price: int
    within_budget: bool


class LayoutRequest(BaseModel):
    room: Room
    item_ids: list[str]


class LayoutResponse(BaseModel):
    placements: list[Placement]
    unplaced: list[str]
    violations: list[Violation]


class ValidateRequest(BaseModel):
    room: Room
    placements: list[Placement]


class Project(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    room: Room
    placements: list[Placement] = Field(default_factory=list)
    style: Style | None = None
    budget: int | None = None


class StoredProject(Project):
    id: str
