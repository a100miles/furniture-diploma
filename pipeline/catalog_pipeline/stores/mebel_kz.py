"""mebel.kz parser.

The site is a Next.js app. Category pages embed the full product cards
(name, price, category, colour, dimensions in cm) in the React Server
Components payload pushed through `self.__next_f.push([1, "..."])`, so a
listing page yields ~50 items. Some cards (mostly configurable beds) only
carry the sleeping-area size; for those the product page is fetched to read
the overall size.
"""

import json
import re
from collections.abc import Iterator
from datetime import datetime, timezone

from ..normalize import Item, Rejected, check, to_cm

STORE = "mebel_kz"
BASE_URL = "https://mebel.kz"

# Our category -> mebel.kz category slugs. An item listed in several slugs is
# kept under the first one, so more specific slugs come first.
CATEGORIES: dict[str, list[str]] = {
    "sofa": ["divany"],
    "armchair": ["kresla"],
    "office_chair": ["kompyuternye-kresla"],
    "bed": ["krovati"],
    # Before nightstand: the bedside-table listing also shows coffee tables.
    "coffee_table": ["zurnalnye-stoliki"],
    "nightstand": ["prikrovatnye-tumby"],
    "wardrobe": ["shkafy"],
    "bookshelf": ["stellazhi", "knizhnye-shkafy"],
    "desk": ["stoly-pismennye-i-kompyuternye"],
    "tv_stand": ["tv-tumby"],
}

# Size groups are titled "Размеры (ДxШxВ)" or "Габариты (ДxШxВ)": length, width, height.
SIZE_GROUP = re.compile(r"^(Размеры|Габариты)\b")
FLIGHT_CHUNK = re.compile(r'self\.__next_f\.push\(\[1,(".*?")\]\)</script>', re.S)
FLIGHT_ROW = re.compile(r"^[0-9a-f]+:")


def category_url(slug: str, page: int = 1) -> str:
    return f"{BASE_URL}/category/{slug}" + (f"/page-{page}" if page > 1 else "")


def last_page(html: str, slug: str) -> int:
    pages = [int(n) for n in re.findall(rf"/category/{re.escape(slug)}/page-(\d+)", html)]
    return max(pages, default=1)


def _flight_objects(html: str) -> Iterator[dict]:
    """Every JSON object in the page's React Server Components payload."""
    flight = "".join(json.loads(chunk) for chunk in FLIGHT_CHUNK.findall(html))

    def walk(node):
        if isinstance(node, dict):
            yield node
            for value in node.values():
                yield from walk(value)
        elif isinstance(node, list):
            for value in node:
                yield from walk(value)

    for row in flight.split("\n"):
        match = FLIGHT_ROW.match(row)
        if not match:
            continue
        try:
            data = json.loads(row[match.end():])
        except json.JSONDecodeError:
            continue  # module references and text chunks, not data
        yield from walk(data)


def product_cards(html: str) -> list[dict]:
    """All product cards embedded in a page, in page order, without duplicates."""
    cards: dict[int, dict] = {}
    for node in _flight_objects(html):
        if {"id", "link", "price", "parameterValues"} <= node.keys():
            cards.setdefault(node["id"], node)
    return list(cards.values())


def has_size(card: dict) -> bool:
    try:
        _size(card)
    except Rejected:
        return False
    return True


def product_page_size(html: str) -> tuple[int, int, int]:
    """Overall (length, width, height) from a product page.

    The size block may lack a height; configurable beds then give it as the
    selected headboard height ("Высота изголовья").
    """
    size: dict[str, int] = {}
    headboard = None
    for node in _flight_objects(html):
        if node.get("theme") == "dimension" and SIZE_GROUP.match(node.get("name", "")) and not size:
            for value in node.get("values", []):
                number, _, unit = value.get("value", "").partition(" ")
                size[value.get("name")] = to_cm(number, unit)
        elif node.get("name") == "Высота изголовья" and headboard is None:
            selected = [v for v in node.get("variants", []) if v.get("selected")]
            if selected:
                number, _, unit = selected[0]["name"].partition(" ")
                headboard = to_cm(number, unit)
    length = size.get("Длина")
    width = size.get("Ширина") or size.get("Глубина")
    height = size.get("Высота") or headboard
    if not (length and width and height):
        raise Rejected("missing_dimensions")
    return length, width, height


def to_item(card: dict, category: str, scraped_at: str, size: tuple[int, int, int] | None = None) -> Item:
    length, width, height = size or _size(card)
    # Beds are listed as length (head to foot) x width; the headboard is against
    # the wall, so the bed's width runs along the wall.
    along_wall, depth = (width, length) if category == "bed" else (length, width)
    return check(
        Item(
            store=STORE,
            external_id=str(card["id"]),
            category=category,
            name=" ".join(filter(None, [card.get("type"), card.get("name")])).strip(),
            width_cm=along_wall,
            depth_cm=depth,
            height_cm=height,
            price_kzt=int((card.get("price") or {}).get("actual") or 0),
            url=product_url(card),
            scraped_at=scraped_at,
            color=card.get("color") or None,
            material=_parameter(card, "Материал"),
            source_category=card.get("category"),
            image_urls=[img["src"] for img in card.get("images", []) if img.get("src")][:3],
        )
    )


def _size(card: dict) -> tuple[int, int, int]:
    groups = [g["id"] for g in card.get("parameterGroups", []) if SIZE_GROUP.match(g.get("title", ""))]
    if not groups:
        raise Rejected("missing_dimensions")
    units = {u["id"]: u["title"] for u in card.get("units", [])}
    values = {v["parameterId"]: v for v in card["parameterValues"]}
    sizes = []
    for param in card.get("parameters", []):
        value = values.get(param["id"])
        if param.get("groupId") == groups[0] and value and value.get("value"):
            sizes.append(to_cm(value["value"][0], units.get(value.get("unitId"))))
    if len(sizes) != 3:
        raise Rejected("missing_dimensions")
    return sizes[0], sizes[1], sizes[2]


def _parameter(card: dict, title_prefix: str) -> str | None:
    values = {v["parameterId"]: v for v in card["parameterValues"]}
    for param in card.get("parameters", []):
        value = values.get(param["id"])
        if param.get("title", "").startswith(title_prefix) and value and value.get("value"):
            return ", ".join(str(v) for v in value["value"])
    return None


def product_url(card: dict) -> str:
    return BASE_URL + card["link"]


def crawl(fetch, categories: list[str], max_pages: int | None = None) -> Iterator[tuple[str, dict]]:
    """Yield (category, card) for every product card in the given categories."""
    for category in categories:
        for slug in CATEGORIES[category]:
            html = fetch(category_url(slug))
            pages = last_page(html, slug)
            if max_pages:
                pages = min(pages, max_pages)
            for page in range(1, pages + 1):
                if page > 1:
                    html = fetch(category_url(slug, page))
                for card in product_cards(html):
                    yield category, card


def now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")
