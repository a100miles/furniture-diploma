"""Footprint geometry and layout validation (FR-07).

Footprints are axis-aligned rectangles because rotations are multiples of 90°.
"""

from dataclasses import dataclass

from .models import Door, FurnitureItem, Placement, Room, Violation, Wall

EPS = 1e-6


@dataclass(frozen=True)
class Rect:
    x0: float
    z0: float
    x1: float
    z1: float

    def intersects(self, other: "Rect") -> bool:
        return self.x0 < other.x1 - EPS and other.x0 < self.x1 - EPS and self.z0 < other.z1 - EPS and other.z0 < self.z1 - EPS

    def inside(self, room: Room) -> bool:
        return self.x0 >= -EPS and self.z0 >= -EPS and self.x1 <= room.width + EPS and self.z1 <= room.length + EPS

    def expand(self, margin: float) -> "Rect":
        return Rect(self.x0 - margin, self.z0 - margin, self.x1 + margin, self.z1 + margin)


def footprint_size(item: FurnitureItem, rotation: int) -> tuple[float, float]:
    """Size of the footprint along (x, z) for the given rotation."""
    if rotation % 180 == 0:
        return item.width, item.depth
    return item.depth, item.width


def footprint(item: FurnitureItem, placement: Placement) -> Rect:
    sx, sz = footprint_size(item, placement.rotation)
    return Rect(placement.x - sx / 2, placement.z - sz / 2, placement.x + sx / 2, placement.z + sz / 2)


def door_zone(room: Room, door: Door) -> Rect:
    """Square in front of the door that must stay free for the door to swing."""
    half, d = door.width / 2, door.width
    if door.wall == Wall.back:
        return Rect(door.offset - half, 0, door.offset + half, d)
    if door.wall == Wall.front:
        return Rect(door.offset - half, room.length - d, door.offset + half, room.length)
    if door.wall == Wall.left:
        return Rect(0, door.offset - half, d, door.offset + half)
    return Rect(room.width - d, door.offset - half, room.width, door.offset + half)


def validate(room: Room, placements: list[Placement], items: dict[str, FurnitureItem]) -> list[Violation]:
    violations: list[Violation] = []
    rects: list[tuple[str, Rect]] = []
    for p in placements:
        item = items.get(p.item_id)
        if item is None:
            violations.append(Violation(kind="unknown_item", item_ids=[p.item_id], message=f"Unknown item {p.item_id}"))
            continue
        rect = footprint(item, p)
        rects.append((p.item_id, rect))
        if not rect.inside(room):
            violations.append(Violation(kind="out_of_bounds", item_ids=[p.item_id], message=f"{item.name} is outside the room"))
        for door in room.doors:
            if rect.intersects(door_zone(room, door)):
                violations.append(Violation(kind="door_blocked", item_ids=[p.item_id], message=f"{item.name} blocks a door"))
    for i, (id_a, a) in enumerate(rects):
        for id_b, b in rects[i + 1 :]:
            if a.intersects(b):
                violations.append(Violation(kind="overlap", item_ids=[id_a, id_b], message=f"{id_a} overlaps {id_b}"))
    return violations
