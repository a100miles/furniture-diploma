"""Rule-based automatic layout, version 1 (FR-06).

Interior design guidelines (Merrell et al. 2011; Yu et al. 2011) are written as
a score for each candidate position; hard constraints (inside the room, no
overlap, door swing zone free) are never violated. Items are placed greedily,
anchors first, so later items can relate to them (coffee table in front of the
sofa, nightstands beside the bed, ...).

Rotation convention (matches three.js rotation.y): at 0° an item's front faces
+z; 90° faces +x; 180° faces -z; 270° faces -x.
"""

import math
from dataclasses import dataclass

from . import catalog
from .geometry import Rect, door_zone, footprint, validate
from .models import FurnitureItem, LayoutRequest, LayoutResponse, Placement, Room

WALL_STEP = 0.05
FREE_STEP = 0.1
WALKWAY = 0.6  # free depth in front of an item, m

# Placement order: room-defining pieces first, then pieces that relate to them.
ORDER = ["bed", "sofa", "wardrobe", "desk", "tv_stand", "bookshelf", "nightstand", "coffee_table", "armchair", "office_chair"]

FRONT = {0: (0.0, 1.0), 90: (1.0, 0.0), 180: (0.0, -1.0), 270: (-1.0, 0.0)}


@dataclass
class Placed:
    item: FurnitureItem
    placement: Placement
    rect: Rect


def front_dir(rotation: int) -> tuple[float, float]:
    return FRONT[rotation % 360]


def wall_candidates(item: FurnitureItem, room: Room) -> list[Placement]:
    """Positions with the item's back against each wall."""
    out: list[Placement] = []
    w, d = item.width, item.depth
    for rotation, along, fixed in (
        (0, room.width, d / 2),  # back wall z = 0
        (180, room.width, room.length - d / 2),  # front wall
        (90, room.length, d / 2),  # left wall x = 0
        (270, room.length, room.width - d / 2),  # right wall
    ):
        steps = int((along - w) / WALL_STEP)
        for i in range(steps + 1):
            t = w / 2 + i * WALL_STEP
            if rotation in (0, 180):
                out.append(Placement(item_id=item.id, x=round(t, 3), z=round(fixed, 3), rotation=rotation))
            else:
                out.append(Placement(item_id=item.id, x=round(fixed, 3), z=round(t, 3), rotation=rotation))
    return out


def free_candidates(item: FurnitureItem, room: Room) -> list[Placement]:
    out: list[Placement] = []
    nx, nz = int(room.width / FREE_STEP), int(room.length / FREE_STEP)
    for rotation in (0, 90, 180, 270):
        for i in range(nx + 1):
            for j in range(nz + 1):
                out.append(Placement(item_id=item.id, x=round(i * FREE_STEP, 3), z=round(j * FREE_STEP, 3), rotation=rotation))
    return out


def is_valid(room: Room, rect: Rect, placed: list[Placed], doors: list[Rect]) -> bool:
    if not rect.inside(room):
        return False
    if any(rect.intersects(d) for d in doors):
        return False
    return not any(rect.intersects(p.rect) for p in placed)


def front_zone(rect: Rect, rotation: int, depth: float = WALKWAY) -> Rect:
    fx, fz = front_dir(rotation)
    if fz > 0:
        return Rect(rect.x0, rect.z1, rect.x1, rect.z1 + depth)
    if fz < 0:
        return Rect(rect.x0, rect.z0 - depth, rect.x1, rect.z0)
    if fx > 0:
        return Rect(rect.x1, rect.z0, rect.x1 + depth, rect.z1)
    return Rect(rect.x0 - depth, rect.z0, rect.x0, rect.z1)


def _dist(ax: float, az: float, bx: float, bz: float) -> float:
    return math.hypot(ax - bx, az - bz)


def _first(placed: list[Placed], category: str) -> Placed | None:
    return next((p for p in placed if p.item.category == category), None)


def _facing(p: Placement, tx: float, tz: float) -> float:
    """1 when the item faces the target point, -1 when it faces away."""
    fx, fz = front_dir(p.rotation)
    dx, dz = tx - p.x, tz - p.z
    n = math.hypot(dx, dz) or 1.0
    return (fx * dx + fz * dz) / n


def score(item: FurnitureItem, p: Placement, rect: Rect, room: Room, placed: list[Placed], doors: list[Rect]) -> float:
    s = 0.0
    cx, cz = room.width / 2, room.length / 2

    # Keep a walkway in front of the item (soft).
    zone = front_zone(rect, p.rotation)
    if not zone.inside(room) or any(zone.intersects(o.rect) for o in placed):
        s -= 2.0

    # Stay away from doors.
    for d in doors:
        s += min(_dist(p.x, p.z, (d.x0 + d.x1) / 2, (d.z0 + d.z1) / 2), 3.0) * 0.3

    cat = item.category
    if cat in ("bed", "sofa"):
        # Centre of a long wall, facing into the room.
        s += 2.0 * _facing(p, cx, cz)
        along = p.x if p.rotation in (0, 180) else p.z
        wall_len = room.width if p.rotation in (0, 180) else room.length
        s -= abs(along - wall_len / 2)
        s += 0.5 * wall_len
    elif cat == "tv_stand":
        sofa = _first(placed, "sofa")
        if sofa:
            # Both must face each other: the TV faces the sofa and the sofa faces the TV.
            s += 3.0 * _facing(p, sofa.placement.x, sofa.placement.z)
            s += 3.0 * _facing(sofa.placement, p.x, p.z)
            s -= abs(_dist(p.x, p.z, sofa.placement.x, sofa.placement.z) - 2.8)
    elif cat == "coffee_table":
        sofa = _first(placed, "sofa")
        if sofa:
            fx, fz = front_dir(sofa.placement.rotation)
            gap = sofa.item.depth / 2 + 0.45 + item.depth / 2
            tx, tz = sofa.placement.x + fx * gap, sofa.placement.z + fz * gap
            s -= 3.0 * _dist(p.x, p.z, tx, tz)
            s += 1.0 if p.rotation % 180 == sofa.placement.rotation % 180 else 0.0
        else:
            s -= _dist(p.x, p.z, cx, cz)
    elif cat == "armchair":
        target = _first(placed, "coffee_table") or _first(placed, "sofa")
        if target:
            dist = _dist(p.x, p.z, target.placement.x, target.placement.z)
            s -= 2.0 * abs(dist - 1.2)
            s += 2.0 * _facing(p, target.placement.x, target.placement.z)
    elif cat == "nightstand":
        bed = _first(placed, "bed")
        if bed:
            s -= 3.0 * min(_dist(p.x, p.z, tx, tz) for tx, tz in _bedside_points(bed, item))
            s += 1.0 if p.rotation == bed.placement.rotation else 0.0
    elif cat == "office_chair":
        desk = _first(placed, "desk")
        if desk:
            fx, fz = front_dir(desk.placement.rotation)
            gap = desk.item.depth / 2 + item.depth / 2 + 0.05
            s -= 3.0 * _dist(p.x, p.z, desk.placement.x + fx * gap, desk.placement.z + fz * gap)
            s += 2.0 * _facing(p, desk.placement.x, desk.placement.z)
    elif cat in ("wardrobe", "bookshelf"):
        # Near a corner keeps the middle of the room open.
        corner = min(_dist(p.x, p.z, x, z) for x in (0, room.width) for z in (0, room.length))
        s -= 0.5 * corner
    return s


def _bedside_points(bed: Placed, item: FurnitureItem) -> list[tuple[float, float]]:
    fx, fz = front_dir(bed.placement.rotation)
    # Along the head wall, i.e. perpendicular to the bed's facing direction.
    ax, az = -fz, fx
    side = bed.item.width / 2 + item.width / 2 + 0.05
    back = -(bed.item.depth / 2 - item.depth / 2)
    return [
        (bed.placement.x + ax * side * k + fx * back, bed.placement.z + az * side * k + fz * back)
        for k in (-1, 1)
    ]


def auto_layout(request: LayoutRequest) -> LayoutResponse:
    room = request.room
    items_by_id = catalog.load_catalog()
    doors = [door_zone(room, d) for d in room.doors]

    unknown = [i for i in request.item_ids if i not in items_by_id]
    known = [items_by_id[i] for i in request.item_ids if i in items_by_id]
    order = {c: n for n, c in enumerate(ORDER)}
    known.sort(key=lambda it: (order.get(it.category, len(ORDER)), -it.width * it.depth))

    placed: list[Placed] = []
    unplaced: list[str] = list(unknown)
    for item in known:
        candidates = wall_candidates(item, room) if item.against_wall else free_candidates(item, room)
        best: tuple[float, Placement, Rect] | None = None
        for cand in candidates:
            rect = footprint(item, cand)
            if not is_valid(room, rect, placed, doors):
                continue
            value = score(item, cand, rect, room, placed, doors)
            if best is None or value > best[0]:
                best = (value, cand, rect)
        if best is None:
            unplaced.append(item.id)
        else:
            placed.append(Placed(item=item, placement=best[1], rect=best[2]))

    placements = [p.placement for p in placed]
    return LayoutResponse(placements=placements, unplaced=unplaced, violations=validate(room, placements, items_by_id))
