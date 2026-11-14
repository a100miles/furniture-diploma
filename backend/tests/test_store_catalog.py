import json

from app.catalog import STORE_DATA_DIR
from app.models import Style
from app.store_catalog import guess_styles, to_furniture_item

ROW = {
    "store": "mebel_kz",
    "external_id": "368356",
    "category": "sofa",
    "name": "Диван прямой Слипсон Букле Молочный",
    "width_cm": 220,
    "depth_cm": 110,
    "height_cm": 95,
    "price_kzt": 558820,
    "url": "https://mebel.kz/product/x",
    "color": "Бежевый",
}


def test_store_row_becomes_item_in_metres():
    item = to_furniture_item(ROW)
    assert item.id == "mebel_kz-368356"
    assert (item.width, item.depth, item.height) == (2.2, 1.1, 0.95)
    assert item.price == 558820
    assert item.color == "#d8c3a5"
    assert item.against_wall
    assert item.url == "https://mebel.kz/product/x"


def test_unknown_colour_falls_back_to_grey():
    assert to_furniture_item({**ROW, "color": None}).color == "#cccccc"


def test_styles_from_name_keywords():
    assert guess_styles("Диван Слипсон Букле Молочный") == [Style.scandinavian, Style.minimalist]
    assert guess_styles("Стеллаж Кимбол Дуб Барбера/Черный") == [Style.scandinavian, Style.loft]
    assert guess_styles("Кресло Нолан") == [Style.modern]


def test_parsed_mebel_kz_catalog_loads():
    rows = json.loads((STORE_DATA_DIR / "mebel_kz.json").read_text(encoding="utf-8"))
    items = [to_furniture_item(row) for row in rows]
    assert len(items) > 1000
    assert len({i.id for i in items}) == len(items)
    assert {i.category for i in items} >= {"sofa", "bed", "wardrobe", "desk"}
