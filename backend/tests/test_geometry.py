from app.catalog import load_catalog
from app.geometry import Rect, footprint, footprint_size, validate
from app.models import Door, Placement, Room, Wall

ITEMS = load_catalog()
ROOM = Room(width=4.0, length=3.5)


def test_rotation_swaps_footprint():
    sofa = ITEMS["sofa-oslo-3"]
    assert footprint_size(sofa, 0) == (sofa.width, sofa.depth)
    assert footprint_size(sofa, 90) == (sofa.depth, sofa.width)


def test_touching_rects_do_not_overlap():
    assert not Rect(0, 0, 1, 1).intersects(Rect(1, 0, 2, 1))
    assert Rect(0, 0, 1, 1).intersects(Rect(0.9, 0.9, 2, 2))


def test_valid_layout_has_no_violations():
    placements = [Placement(item_id="sofa-oslo-3", x=2.0, z=0.45, rotation=0)]
    assert validate(ROOM, placements, ITEMS) == []


def test_detects_out_of_bounds():
    placements = [Placement(item_id="sofa-oslo-3", x=0.5, z=0.45, rotation=0)]
    kinds = [v.kind for v in validate(ROOM, placements, ITEMS)]
    assert kinds == ["out_of_bounds"]


def test_detects_overlap():
    placements = [
        Placement(item_id="sofa-oslo-3", x=2.0, z=0.45, rotation=0),
        Placement(item_id="coffee-birch", x=2.0, z=0.8, rotation=0),
    ]
    kinds = [v.kind for v in validate(ROOM, placements, ITEMS)]
    assert kinds == ["overlap"]


def test_detects_blocked_door():
    room = Room(width=4.0, length=3.5, doors=[Door(wall=Wall.back, offset=2.0, width=0.9)])
    placements = [Placement(item_id="sofa-oslo-3", x=2.0, z=0.45, rotation=0)]
    assert [v.kind for v in validate(room, placements, ITEMS)] == ["door_blocked"]


def test_unknown_item_reported():
    placements = [Placement(item_id="nope", x=1, z=1)]
    assert validate(ROOM, placements, ITEMS)[0].kind == "unknown_item"


def test_footprint_centre():
    rect = footprint(ITEMS["coffee-birch"], Placement(item_id="coffee-birch", x=2, z=2, rotation=90))
    assert (round(rect.x0, 3), round(rect.x1, 3)) == (1.7, 2.3)
