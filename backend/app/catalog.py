"""Furniture catalog. Reads the demo catalog from data/catalog.json.

Replaced by a PostgreSQL repository in DIP-17; callers only use these functions.
"""

import json
from functools import lru_cache
from pathlib import Path

from .models import FurnitureItem, Style

CATALOG_PATH = Path(__file__).resolve().parent.parent / "data" / "catalog.json"


@lru_cache
def load_catalog() -> dict[str, FurnitureItem]:
    raw = json.loads(CATALOG_PATH.read_text(encoding="utf-8"))
    return {entry["id"]: FurnitureItem(**entry) for entry in raw}


def get_item(item_id: str) -> FurnitureItem | None:
    return load_catalog().get(item_id)


def search(category: str | None = None, style: Style | None = None, max_price: int | None = None) -> list[FurnitureItem]:
    items = load_catalog().values()
    return [
        item
        for item in items
        if (category is None or item.category == category)
        and (style is None or style in item.styles)
        and (max_price is None or item.price <= max_price)
    ]


def categories() -> list[str]:
    return sorted({item.category for item in load_catalog().values()})
