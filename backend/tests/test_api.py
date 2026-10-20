from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)
ROOM = {"width": 4.0, "length": 3.5, "doors": [{"wall": "front", "offset": 0.6}]}


def test_health():
    assert client.get("/api/health").json() == {"status": "ok"}


def test_catalog_filters():
    res = client.get("/api/catalog", params={"category": "sofa", "style": "modern", "max_price": 300000})
    assert res.status_code == 200
    items = res.json()
    assert items and all(i["category"] == "sofa" and "modern" in i["styles"] and i["price"] <= 300000 for i in items)


def test_catalog_item_404():
    assert client.get("/api/catalog/unknown").status_code == 404


def test_invalid_room_rejected():
    res = client.post("/api/recommendations", json={"room": {"width": 50, "length": 3}, "style": "modern", "budget": 1000})
    assert res.status_code == 422


def test_recommendations_endpoint():
    res = client.post("/api/recommendations", json={"room": ROOM, "style": "loft", "budget": 500000})
    body = res.json()
    assert res.status_code == 200
    assert {c["category"] for c in body["categories"]} == {"sofa", "coffee_table", "tv_stand", "armchair", "bookshelf"}


def test_layout_and_validate_roundtrip():
    res = client.post("/api/layout", json={"room": ROOM, "item_ids": ["sofa-oslo-3", "coffee-birch", "tv-ash"]})
    body = res.json()
    assert res.status_code == 200 and body["violations"] == []
    check = client.post("/api/validate", json={"room": ROOM, "placements": body["placements"]})
    assert check.json() == []


def test_project_save_and_load():
    project = {"name": "My living room", "room": ROOM, "placements": [{"item_id": "tv-ash", "x": 2, "z": 0.2, "rotation": 0}]}
    created = client.post("/api/projects", json=project)
    assert created.status_code == 201
    pid = created.json()["id"]
    loaded = client.get(f"/api/projects/{pid}").json()
    assert loaded["name"] == project["name"] and loaded["placements"][0]["item_id"] == "tv-ash"
    assert client.get("/api/projects/missing").status_code == 404
