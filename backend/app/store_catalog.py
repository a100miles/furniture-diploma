"""Converts catalogue pipeline output (pipeline/data/<store>.json) to prototype items.

Store data has no style tags or hex colours, so both are derived here with
keyword rules on the product name and colour. The style rules are a stand-in
until CLIP-based style tagging (DIP-28) and are not validated.
"""

from .models import FurnitureItem, Style

AGAINST_WALL = {"sofa", "bed", "wardrobe", "tv_stand", "bookshelf", "desk", "nightstand"}

# Store colour name (lower case) -> swatch / 3D box colour.
COLORS = {
    "бежевый": "#d8c3a5",
    "серый": "#9a9a9a",
    "зеленый": "#6b8f5e",
    "белый": "#f2f2f0",
    "коричневый": "#7a5236",
    "оранжевый": "#d9823b",
    "черный": "#2b2b2b",
    "синий": "#34508a",
    "молочный": "#efe8dc",
    "оливковый": "#7d7f45",
    "красный": "#a8322d",
    "светлое дерево": "#c9a77c",
    "терракотовый": "#b5583c",
    "желтый": "#e0b93f",
    "розовый": "#d9a0a8",
    "голубой": "#8fb8d8",
    "графитовый": "#474a4f",
    "темное дерево": "#5a3d2b",
    "бордовый": "#6d1f2c",
    "мятный": "#a8d5c2",
    "кремовый": "#f1e6c8",
    "горчичный": "#c49a2c",
    "фиолетовый": "#6c4f8a",
}
DEFAULT_COLOR = "#cccccc"

# Name keyword (lower case) -> styles it suggests. Materials and finishes carry
# most of the signal: wood -> scandinavian, black frames and leather -> loft, ...
STYLE_KEYWORDS: dict[str, list[Style]] = {
    "лофт": [Style.loft],
    "черный": [Style.loft],
    "экокожа": [Style.loft],
    "темное дерево": [Style.loft, Style.classic],
    "дуб": [Style.scandinavian],
    "орех": [Style.scandinavian, Style.classic],
    "дерево": [Style.scandinavian],
    "древесный": [Style.scandinavian],
    "натуральный": [Style.scandinavian],
    "букле": [Style.scandinavian, Style.minimalist],
    "рогожка": [Style.scandinavian],
    "шенилл": [Style.modern],
    "велюр": [Style.modern],
    "вельвет": [Style.modern],
    "белый": [Style.minimalist],
    "молочный": [Style.minimalist, Style.scandinavian],
    "светло-серый": [Style.minimalist],
    "графитовый": [Style.minimalist, Style.modern],
    "бордовый": [Style.classic],
    "коричневый": [Style.classic],
    "золотистый": [Style.classic],
    "кремовый": [Style.classic],
    "терракотовый": [Style.modern],
    "оливковый": [Style.modern],
    "латте": [Style.scandinavian],
}


def guess_styles(name: str) -> list[Style]:
    text = name.lower()
    styles = {style for keyword, tags in STYLE_KEYWORDS.items() if keyword in text for style in tags}
    return sorted(styles, key=list(Style).index) or [Style.modern]


def to_furniture_item(row: dict) -> FurnitureItem:
    return FurnitureItem(
        id=f"{row['store']}-{row['external_id']}",
        name=row["name"],
        category=row["category"],
        styles=guess_styles(row["name"]),
        width=row["width_cm"] / 100,
        depth=row["depth_cm"] / 100,
        height=row["height_cm"] / 100,
        price=row["price_kzt"],
        color=COLORS.get((row.get("color") or "").lower(), DEFAULT_COLOR),
        against_wall=row["category"] in AGAINST_WALL,
        url=row.get("url"),
    )
