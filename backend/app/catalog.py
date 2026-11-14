"""Furniture catalog.

`CATALOG=mebel_kz` (default) reads items parsed from mebel.kz by the catalogue
pipeline (pipeline/data/mebel_kz.json); `CATALOG=demo` reads the 25-item demo
catalog in data/catalog.json, which the tests use.

Replaced by a PostgreSQL repository in DIP-17; callers only use these functions.
"""

import json
import os
from functools import lru_cache
from pathlib import Path

from .models import FurnitureItem, Style
from .store_catalog import to_furniture_item

CATALOG_PATH = Path(__file__).resolve().parent.parent / "data" / "catalog.json"
STORE_DATA_DIR = Path(__file__).resolve().parents[2] / "pipeline" / "data"


@lru_cache
def load_catalog() -> dict[str, FurnitureItem]:
    source = os.getenv("CATALOG", "mebel_kz")
    if source == "demo":
        raw = json.loads(CATALOG_PATH.read_text(encoding="utf-8"))
        items = [FurnitureItem(**entry) for entry in raw]
    else:
        raw = json.loads((STORE_DATA_DIR / f"{source}.json").read_text(encoding="utf-8"))
        items = [to_furniture_item(row) for row in raw]
    return {item.id: item for item in items}


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
