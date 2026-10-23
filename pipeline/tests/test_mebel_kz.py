import json

import pytest

from catalog_pipeline.normalize import Rejected
from catalog_pipeline.stores import mebel_kz


def page(*objects) -> str:
    """A minimal Next.js page whose RSC payload holds the given objects, one per row."""
    flight = "".join(f"{i:x}:{json.dumps(obj, ensure_ascii=False)}\n" for i, obj in enumerate(objects))
    flight = '0:I["chunk.js"]\n' + flight  # module reference row, not JSON data
    return f"<html><body><script>self.__next_f.push([1,{json.dumps(flight)}])</script></body></html>"


def card(id=1, size=(220, 110, 95), group="Габариты (ДxШxВ)", **extra) -> dict:
    groups = [{"id": 3, "title": "Спальное место (ДхШхВ)"}]
    params = [{"id": 3, "groupId": 3, "title": "Спальное место (ДxШxВ)"}]
    values = [{"value": [200], "parameterId": 3, "unitId": 1}]
    if size:
        groups.insert(0, {"id": 2, "title": group})
        for param_id, value in zip((1, 41, 9), size):
            params.append({"id": param_id, "groupId": 2, "title": group})
            values.append({"value": [value], "parameterId": param_id, "unitId": 1})
    return {
        "id": id,
        "type": "Диван прямой",
        "name": "Слипсон Велюр Молочный",
        "category": "Прямые диваны",
        "color": "Бежевый",
        "link": f"/product/item-{id}",
        "price": {"actual": 558820},
        "images": [{"src": "https://cdn.example/1.jpg"}],
        "parameterGroups": groups,
        "parameters": params,
        "parameterValues": values,
        "units": [{"id": 1, "title": " см"}],
        **extra,
    }


def test_product_cards_are_found_anywhere_in_the_payload_without_duplicates():
    html = page({"products": [card(1), card(2)]}, ["$", "div", None, {"children": card(1)}])
    assert [c["id"] for c in mebel_kz.product_cards(html)] == [1, 2]


def test_to_item_maps_length_width_height_to_cm_fields():
    item = mebel_kz.to_item(card(size=(220, 110, 95)), "sofa", "2026-10-23T00:00:00+00:00")
    assert (item.width_cm, item.depth_cm, item.height_cm) == (220, 110, 95)
    assert item.name == "Диван прямой Слипсон Велюр Молочный"
    assert item.price_kzt == 558820
    assert item.url == "https://mebel.kz/product/item-1"
    assert item.external_id == "1"


def test_bed_width_runs_along_the_wall():
    item = mebel_kz.to_item(card(size=(207, 188, 89)), "bed", "t")
    assert (item.width_cm, item.depth_cm) == (188, 207)


def test_sleeping_area_is_not_used_as_the_footprint():
    assert not mebel_kz.has_size(card(size=None))
    with pytest.raises(Rejected, match="missing_dimensions"):
        mebel_kz.to_item(card(size=None), "bed", "t")


def test_items_without_price_are_rejected():
    with pytest.raises(Rejected, match="missing_price"):
        mebel_kz.to_item(card(price={"actual": 0}), "sofa", "t")


def test_product_page_size_falls_back_to_headboard_height():
    html = page(
        {"theme": "dimension", "name": "Спальное место", "values": [{"name": "Высота", "value": "33 см"}]},
        {"theme": "dimension", "name": "Размеры", "values": [{"name": "Длина", "value": "217 см"}, {"name": "Ширина", "value": "181 см"}]},
        {"name": "Высота изголовья", "variants": [{"name": "130 см"}, {"name": "95 см", "selected": True}]},
    )
    assert mebel_kz.product_page_size(html) == (217, 181, 95)


def test_last_page_reads_pagination_links():
    html = '<a href="/category/divany/page-2"></a><a href="/category/divany/page-23"></a><a href="/category/krovati/page-40"></a>'
    assert mebel_kz.last_page(html, "divany") == 23
    assert mebel_kz.last_page("", "divany") == 1


def test_crawl_visits_every_page_and_respects_max_pages():
    fetched = []

    def fetch(url):
        fetched.append(url)
        return page({"products": [card(len(fetched))]}) + '<a href="/category/divany/page-3"></a>'

    cards = list(mebel_kz.crawl(fetch, ["sofa"], max_pages=2))
    assert fetched == ["https://mebel.kz/category/divany", "https://mebel.kz/category/divany/page-2"]
    assert [(category, c["id"]) for category, c in cards] == [("sofa", 1), ("sofa", 2)]
