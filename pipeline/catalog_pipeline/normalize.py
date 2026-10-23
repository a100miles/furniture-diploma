"""One schema for items from every store (matches `furniture_items` in docs/database-schema.md)."""

from dataclasses import dataclass, field

# Plausible footprint and height for room furniture, cm. Values outside this
# range are almost always data errors (mm entered as cm, missing digits).
MIN_CM, MAX_CM = 10, 500

UNIT_TO_CM = {"мм": 0.1, "mm": 0.1, "см": 1.0, "cm": 1.0, "м": 100.0, "m": 100.0}


class Rejected(Exception):
    """A source row that cannot become a catalogue item; the message is the reason code."""


@dataclass
class Item:
    store: str
    external_id: str
    category: str
    name: str
    width_cm: int
    depth_cm: int
    height_cm: int
    price_kzt: int
    url: str
    scraped_at: str
    color: str | None = None
    material: str | None = None
    source_category: str | None = None
    image_urls: list[str] = field(default_factory=list)


def to_cm(value: float | int | str, unit: str | None) -> int:
    factor = UNIT_TO_CM.get((unit or "см").strip().lower().rstrip("."))
    if factor is None:
        raise Rejected("unknown_unit")
    try:
        number = float(str(value).replace(",", ".").replace(" ", ""))
    except ValueError:
        raise Rejected("bad_dimension") from None
    return round(number * factor)


def check(item: Item) -> Item:
    if not item.name.strip():
        raise Rejected("missing_name")
    if item.price_kzt <= 0:
        raise Rejected("missing_price")
    for size in (item.width_cm, item.depth_cm, item.height_cm):
        if not MIN_CM <= size <= MAX_CM:
            raise Rejected("implausible_dimensions")
    return item
