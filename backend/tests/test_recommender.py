from app.models import RecommendationRequest, Room, RoomType, Style
from app.recommender import fits_room, recommend
from app.catalog import load_catalog


def make_request(**kw):
    base = dict(room=Room(width=4.0, length=3.5), room_type=RoomType.living_room, style=Style.scandinavian, budget=600_000)
    base.update(kw)
    return RecommendationRequest(**base)


def test_all_recommendations_satisfy_hard_constraints():
    req = make_request()
    res = recommend(req)
    for cat in res.categories:
        for rec in cat.options:
            assert rec.item.category == cat.category
            assert rec.item.price <= req.budget
            assert fits_room(rec.item, req.room)


def test_style_match_ranks_first():
    res = recommend(make_request())
    sofas = next(c for c in res.categories if c.category == "sofa")
    assert Style.scandinavian in sofas.options[0].item.styles
    assert sofas.options[0].reasons[0] == "Matches your scandinavian style"


def test_every_recommendation_is_explained():
    res = recommend(make_request())
    for cat in res.categories:
        for rec in cat.options:
            assert len(rec.reasons) == 3 and all(rec.reasons)
            assert 0 <= rec.score <= 1


def test_bundle_respects_budget_when_possible():
    # Cheapest complete living-room set in the demo catalog costs 465 000.
    res = recommend(make_request(budget=500_000))
    assert res.within_budget
    assert res.bundle_price <= 500_000
    assert len(res.bundle) == 5


def test_bundle_reports_impossible_budget():
    res = recommend(make_request(budget=300_000))
    assert not res.within_budget
    assert res.bundle_price > 300_000


def test_large_items_excluded_from_small_room():
    small = Room(width=2.2, length=2.5)
    corner_sofa = load_catalog()["sofa-brick-corner"]
    assert not fits_room(corner_sofa, small)


def test_custom_categories():
    res = recommend(make_request(room_type=RoomType.bedroom, categories=["bed", "wardrobe"], top_k=2))
    assert [c.category for c in res.categories] == ["bed", "wardrobe"]
    assert all(len(c.options) <= 2 for c in res.categories)
