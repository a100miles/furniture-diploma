"""Constraint-based furniture recommender with weighted scoring (FR-05).

Approach (see docs/literature-review.md, Felfernig & Burke 2008):
1. Hard constraints remove items that cannot work: does not fit the room, or
   costs more than the whole budget.
2. Soft criteria are scored in [0, 1] and combined with fixed weights:
   style match, size suitability for the room, price vs. the planned share of
   the budget for that category.
3. Every score comes with human-readable reasons, so the user can see why an
   item is recommended.
4. A bundle (one item per category) is chosen greedily to fit the total budget.
"""

from . import catalog
from .models import (
    CategoryRecommendations,
    FurnitureItem,
    Recommendation,
    RecommendationRequest,
    RecommendationResponse,
    Room,
    RoomType,
    Style,
)

WEIGHTS = {"style": 0.5, "size": 0.3, "price": 0.2}

DEFAULT_CATEGORIES = {
    RoomType.living_room: ["sofa", "coffee_table", "tv_stand", "armchair", "bookshelf"],
    RoomType.bedroom: ["bed", "nightstand", "wardrobe"],
    RoomType.office: ["desk", "office_chair", "bookshelf"],
}

# Relative share of the budget a category typically takes; normalised over the requested categories.
BUDGET_SHARE = {
    "sofa": 0.35,
    "bed": 0.40,
    "wardrobe": 0.25,
    "desk": 0.30,
    "office_chair": 0.20,
    "armchair": 0.12,
    "tv_stand": 0.12,
    "coffee_table": 0.08,
    "bookshelf": 0.08,
    "nightstand": 0.05,
}

# How well a style goes with the requested one (1.0 = same style).
STYLE_COMPAT: dict[Style, dict[Style, float]] = {
    Style.scandinavian: {Style.minimalist: 0.7, Style.modern: 0.5, Style.loft: 0.3, Style.classic: 0.1},
    Style.modern: {Style.minimalist: 0.7, Style.loft: 0.5, Style.scandinavian: 0.5, Style.classic: 0.3},
    Style.classic: {Style.modern: 0.3, Style.scandinavian: 0.1, Style.loft: 0.1, Style.minimalist: 0.1},
    Style.loft: {Style.modern: 0.5, Style.minimalist: 0.4, Style.scandinavian: 0.3, Style.classic: 0.1},
    Style.minimalist: {Style.scandinavian: 0.7, Style.modern: 0.7, Style.loft: 0.4, Style.classic: 0.1},
}

# Ideal item width as a fraction of the longest wall, for large pieces that define the room.
IDEAL_WIDTH_RATIO = {"sofa": 0.5, "bed": 0.45, "wardrobe": 0.35, "tv_stand": 0.4, "desk": 0.35}
# Largest acceptable share of the floor area for one item.
MAX_AREA_SHARE = 0.25


def fits_room(item: FurnitureItem, room: Room) -> bool:
    long_wall, short_wall = max(room.width, room.length), min(room.width, room.length)
    big, small = max(item.width, item.depth), min(item.width, item.depth)
    return big <= long_wall and small <= short_wall and item.width * item.depth <= MAX_AREA_SHARE * room.width * room.length


def style_score(item: FurnitureItem, style: Style) -> tuple[float, str]:
    if style in item.styles:
        return 1.0, f"Matches your {style.value} style"
    best = max(item.styles, key=lambda s: STYLE_COMPAT[style].get(s, 0.0))
    value = STYLE_COMPAT[style].get(best, 0.0)
    return value, f"{best.value.capitalize()} style, {'goes well' if value >= 0.5 else 'contrasts'} with {style.value}"


def size_score(item: FurnitureItem, room: Room) -> tuple[float, str]:
    long_wall = max(room.width, room.length)
    ideal = IDEAL_WIDTH_RATIO.get(item.category)
    if ideal is None:
        share = item.width * item.depth / (room.width * room.length)
        return 1.0 - min(1.0, share / MAX_AREA_SHARE) * 0.5, f"Takes {share:.0%} of the floor area"
    ratio = item.width / long_wall
    value = max(0.0, 1.0 - abs(ratio - ideal) / ideal)
    return value, f"Width {item.width:.2f} m suits a {long_wall:.1f} m wall" if value >= 0.6 else f"Width {item.width:.2f} m is {'large' if ratio > ideal else 'small'} for a {long_wall:.1f} m wall"


def price_score(item: FurnitureItem, planned: float) -> tuple[float, str]:
    if item.price <= planned:
        return 1.0, f"{_kzt(item.price)} is within the planned {_kzt(planned)} for this item"
    over = (item.price - planned) / planned
    return max(0.0, 1.0 - over), f"{_kzt(item.price)} is {over:.0%} above the planned {_kzt(planned)}"


def planned_budget(categories: list[str], budget: int) -> dict[str, float]:
    shares = {c: BUDGET_SHARE.get(c, 0.1) for c in categories}
    total = sum(shares.values())
    return {c: budget * s / total for c, s in shares.items()}


def score_item(item: FurnitureItem, request: RecommendationRequest, planned: float) -> Recommendation:
    s_style, r_style = style_score(item, request.style)
    s_size, r_size = size_score(item, request.room)
    s_price, r_price = price_score(item, planned)
    score = WEIGHTS["style"] * s_style + WEIGHTS["size"] * s_size + WEIGHTS["price"] * s_price
    return Recommendation(item=item, score=round(score, 3), reasons=[r_style, r_size, r_price])


def recommend(request: RecommendationRequest) -> RecommendationResponse:
    categories = request.categories or DEFAULT_CATEGORIES[request.room_type]
    plan = planned_budget(categories, request.budget)

    ranked: dict[str, list[Recommendation]] = {}
    for category in categories:
        candidates = [
            item
            for item in catalog.search(category=category)
            if fits_room(item, request.room) and item.price <= request.budget
        ]
        scored = sorted((score_item(i, request, plan[category]) for i in candidates), key=lambda r: (-r.score, r.item.price))
        ranked[category] = scored

    bundle = choose_bundle(ranked, request.budget)
    bundle_price = sum(r.item.price for r in bundle.values())
    return RecommendationResponse(
        categories=[CategoryRecommendations(category=c, options=ranked[c][: request.top_k]) for c in categories],
        bundle=[r.item.id for r in bundle.values()],
        bundle_price=bundle_price,
        within_budget=bundle_price <= request.budget,
    )


def choose_bundle(ranked: dict[str, list[Recommendation]], budget: int) -> dict[str, Recommendation]:
    """Start from the best item per category; while over budget, make the swap
    to a cheaper option that loses the least score per tenge saved."""
    chosen = {c: opts[0] for c, opts in ranked.items() if opts}
    while sum(r.item.price for r in chosen.values()) > budget:
        best_swap: tuple[float, str, Recommendation] | None = None
        for category, current in chosen.items():
            for option in ranked[category]:
                saved = current.item.price - option.item.price
                if saved <= 0:
                    continue
                loss_per_tenge = (current.score - option.score) / saved
                if best_swap is None or loss_per_tenge < best_swap[0]:
                    best_swap = (loss_per_tenge, category, option)
        if best_swap is None:
            break
        chosen[best_swap[1]] = best_swap[2]
    return chosen


def _kzt(amount: float) -> str:
    return f"{round(amount):,}".replace(",", " ") + " ₸"
