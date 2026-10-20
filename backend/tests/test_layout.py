import pytest

from app.catalog import load_catalog
from app.geometry import footprint
from app.layout import auto_layout
from app.models import Door, LayoutRequest, Room, Wall

LIVING = ["sofa-oslo-3", "coffee-birch", "tv-ash", "armchair-lund", "shelf-ladder"]
BEDROOM = ["bed-nord-160", "night-pine", "night-pine", "wardrobe-2door"]
OFFICE = ["desk-oak-120", "chair-ergo", "shelf-cube"]

ROOMS = [
    Room(width=4.0, length=3.5, doors=[Door(wall=Wall.front, offset=0.6)]),
    Room(width=5.0, length=4.0, doors=[Door(wall=Wall.left, offset=3.2)]),
    Room(width=3.2, length=3.0, doors=[Door(wall=Wall.back, offset=2.6)]),
]


@pytest.mark.parametrize("room", ROOMS)
@pytest.mark.parametrize("items", [LIVING, BEDROOM, OFFICE])
def test_layout_is_valid(room, items):
    res = auto_layout(LayoutRequest(room=room, item_ids=items))
    assert res.violations == []
    assert len(res.placements) + len(res.unplaced) == len(items)


def test_living_room_relations():
    room = ROOMS[1]
    res = auto_layout(LayoutRequest(room=room, item_ids=LIVING))
    assert res.unplaced == []
    by_id = {p.item_id: p for p in res.placements}
    sofa, table, tv = by_id["sofa-oslo-3"], by_id["coffee-birch"], by_id["tv-ash"]
    # Coffee table is in front of the sofa, within 1.2 m.
    assert ((sofa.x - table.x) ** 2 + (sofa.z - table.z) ** 2) ** 0.5 < 1.2
    # TV stand is on the opposite wall, facing the sofa.
    assert abs(sofa.rotation - tv.rotation) == 180


def test_nightstands_next_to_bed():
    room = ROOMS[1]
    items = load_catalog()
    res = auto_layout(LayoutRequest(room=room, item_ids=BEDROOM))
    bed = next(p for p in res.placements if p.item_id == "bed-nord-160")
    bed_rect = footprint(items["bed-nord-160"], bed).expand(0.15)
    stands = [p for p in res.placements if p.item_id == "night-pine"]
    assert len(stands) == 2
    assert all(footprint(items["night-pine"], s).intersects(bed_rect) for s in stands)


def test_too_many_items_are_reported_unplaced():
    room = Room(width=2.5, length=2.5)
    res = auto_layout(LayoutRequest(room=room, item_ids=["bed-nord-160", "wardrobe-sliding", "sofa-chester-3"]))
    assert res.violations == []
    assert res.unplaced


def test_unknown_item_unplaced():
    res = auto_layout(LayoutRequest(room=ROOMS[0], item_ids=["does-not-exist"]))
    assert res.unplaced == ["does-not-exist"]
