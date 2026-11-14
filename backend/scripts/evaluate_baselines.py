"""Offline comparison of the prototype with the baselines of docs/evaluation-plan.md.

H1 (recommendation): rule-based ranker vs B1 (category + max price, cheapest
first) and B1s (B1 plus a style filter), scored with nDCG@5 and Precision@5
against rule-derived 0-2 proxy grades (see grade()).
H2 (layout): guideline solver vs B2 (random valid placement, same hard
constraints, 20 seeded runs per room), scored by an evaluator whose thresholds
are fixed here and are independent of the solver's continuous score.

Run from backend/ with the parsed store data:
  python -m scripts.evaluate_baselines --data ../pipeline/data/mebel_kz.json --out ../docs/assets/eval
"""

import argparse
import csv
import json
import math
import random
import statistics
import time
from pathlib import Path

from app import catalog, layout, recommender
from app.geometry import door_zone, footprint
from app.layout import WALKWAY, front_dir, front_zone, is_valid
from app.models import Door, LayoutRequest, Placement, RecommendationRequest, Room, RoomType, Style, Wall

SEED = 42
K = 5
N_REC = 60  # recommendation scenarios, 20 per room type
N_LAYOUT = 30  # layout rooms, 10 per room type
B2_RUNS = 20  # random-placement runs per room
B2_ATTEMPTS = 1000  # tries per item before it is left unplaced

ROOM_SIZE = {  # (width range, length range), m
    RoomType.living_room: ((3.5, 6.0), (3.0, 5.5)),
    RoomType.bedroom: ((3.0, 5.0), (2.8, 4.5)),
    RoomType.office: ((2.5, 4.5), (2.5, 4.0)),
}
BUDGET = {  # total budget range, KZT
    RoomType.living_room: (600_000, 2_500_000),
    RoomType.bedroom: (400_000, 1_500_000),
    RoomType.office: (250_000, 800_000),
}
# A second copy of one category makes the layout task closer to a real room.
EXTRA = {RoomType.living_room: "armchair", RoomType.bedroom: "nightstand", RoomType.office: None}
# Items whose front must stay accessible; partners intentionally placed in front are exempt.
NEEDS_WALKWAY = {"sofa", "bed", "wardrobe", "bookshelf", "desk", "tv_stand", "armchair"}
PARTNERS = {frozenset(p) for p in (("sofa", "coffee_table"), ("desk", "office_chair"), ("armchair", "coffee_table"))}


# ---------- scenarios ----------


def make_room(rng: random.Random, room_type: RoomType) -> Room:
    (w0, w1), (l0, l1) = ROOM_SIZE[room_type]
    width, length = round(rng.uniform(w0, w1), 1), round(rng.uniform(l0, l1), 1)
    wall = rng.choice(list(Wall))
    along = width if wall in (Wall.back, Wall.front) else length
    return Room(width=width, length=length, doors=[Door(wall=wall, offset=round(rng.uniform(0.6, along - 0.6), 2), width=0.9)])


def make_request(rng: random.Random, room_type: RoomType) -> RecommendationRequest:
    lo, hi = BUDGET[room_type]
    return RecommendationRequest(
        room=make_room(rng, room_type),
        room_type=room_type,
        style=rng.choice(list(Style)),
        budget=round(rng.uniform(lo, hi), -4),
        top_k=K,
    )


def scenarios(rng: random.Random, n: int) -> list[RecommendationRequest]:
    types = list(RoomType)
    return [make_request(rng, types[i % len(types)]) for i in range(n)]


# ---------- H1: recommendation ----------


def grade(item, request: RecommendationRequest, planned: float) -> int:
    """Proxy relevance: 0 = does not fit the room or exceeds the category's
    planned budget; 1 = fits and affordable; 2 = also tagged with the requested style."""
    if not recommender.fits_room(item, request.room) or item.price > planned:
        return 0
    return 2 if request.style in item.styles else 1


def dcg(grades: list[int]) -> float:
    return sum((2**g - 1) / math.log2(i + 2) for i, g in enumerate(grades))


def ndcg(ranked: list[int], pool: list[int], k: int = K) -> float | None:
    ideal = dcg(sorted(pool, reverse=True)[:k])
    return None if ideal == 0 else dcg(ranked[:k]) / ideal


def baseline_b1(category: str, planned: float, style: Style | None = None) -> list:
    items = catalog.search(category=category, style=style, max_price=int(planned))
    return sorted(items, key=lambda i: (i.price, i.id))[:K]


def evaluate_recommendations(requests: list[RecommendationRequest]) -> list[dict]:
    rows = []
    for n, req in enumerate(requests):
        categories = recommender.DEFAULT_CATEGORIES[req.room_type]
        plan = recommender.planned_budget(categories, req.budget)
        t0 = time.perf_counter()
        response = recommender.recommend(req)
        latency = time.perf_counter() - t0
        arca = {c.category: [r.item for r in c.options] for c in response.categories}
        per_system: dict[str, dict[str, list[float]]] = {s: {"ndcg": [], "p": [], "fit": []} for s in ("arca", "b1", "b1s")}
        for c in categories:
            pool = [grade(i, req, plan[c]) for i in catalog.search(category=c)]
            lists = {"arca": arca[c], "b1": baseline_b1(c, plan[c]), "b1s": baseline_b1(c, plan[c], req.style)}
            for system, items in lists.items():
                grades = [grade(i, req, plan[c]) for i in items]
                score = ndcg(grades, pool)
                if score is None:
                    continue
                per_system[system]["ndcg"].append(score)
                per_system[system]["p"].append(sum(g == 2 for g in grades) / K)
                per_system[system]["fit"].append(sum(recommender.fits_room(i, req.room) for i in items) / max(len(items), 1))
        row = {"scenario": n, "room_type": req.room_type.value, "style": req.style.value, "budget": req.budget,
               "width": req.room.width, "length": req.room.length, "latency_s": round(latency, 4),
               "bundle_within_budget": int(response.within_budget)}
        for system, m in per_system.items():
            for metric, values in m.items():
                row[f"{system}_{metric}"] = round(statistics.mean(values), 4) if values else None
        rows.append(row)
    return rows


# ---------- H2: layout ----------


def layout_items(req: RecommendationRequest) -> list[str]:
    response = recommender.recommend(req)
    ids = list(response.bundle)
    extra = EXTRA[req.room_type]
    if extra:
        options = next((c.options for c in response.categories if c.category == extra), [])
        if options:
            ids.append(options[1].item.id if len(options) > 1 else options[0].item.id)
    return ids


def random_layout(room: Room, item_ids: list[str], rng: random.Random) -> tuple[list[Placement], list[str]]:
    items = catalog.load_catalog()
    doors = [door_zone(room, d) for d in room.doors]
    placed: list[layout.Placed] = []
    unplaced = []
    for item_id in item_ids:
        item = items[item_id]
        for _ in range(B2_ATTEMPTS):
            rotation = rng.choice((0, 90, 180, 270))
            sx, sz = (item.width, item.depth) if rotation % 180 == 0 else (item.depth, item.width)
            if sx > room.width or sz > room.length:
                continue
            p = Placement(item_id=item_id, x=rng.uniform(sx / 2, room.width - sx / 2), z=rng.uniform(sz / 2, room.length - sz / 2), rotation=rotation)
            rect = footprint(item, p)
            if is_valid(room, rect, placed, doors):
                placed.append(layout.Placed(item=item, placement=p, rect=rect))
                break
        else:
            unplaced.append(item_id)
    return [p.placement for p in placed], unplaced


def facing(p: Placement, tx: float, tz: float) -> float:
    fx, fz = front_dir(p.rotation)
    dx, dz = tx - p.x, tz - p.z
    return (fx * dx + fz * dz) / (math.hypot(dx, dz) or 1.0)


def against_wall(rect, rotation: int, room: Room, tol: float = 0.05) -> bool:
    r = rotation % 360
    return {0: rect.z0 <= tol, 180: rect.z1 >= room.length - tol, 90: rect.x0 <= tol, 270: rect.x1 >= room.width - tol}[r]


def evaluate_layout(room: Room, item_ids: list[str], placements: list[Placement]) -> dict:
    items = catalog.load_catalog()
    placed = [(items[p.item_id], p, footprint(items[p.item_id], p)) for p in placements]
    by_cat: dict[str, list] = {}
    for entry in placed:
        by_cat.setdefault(entry[0].category, []).append(entry)

    walk_ok = walk_n = 0
    for item, p, rect in placed:
        if item.category not in NEEDS_WALKWAY:
            continue
        walk_n += 1
        zone = front_zone(rect, p.rotation, WALKWAY)
        blocked = any(zone.intersects(r) for other, _, r in placed if other is not item and frozenset((item.category, other.category)) not in PARTNERS)
        walk_ok += zone.inside(room) and not blocked

    wall_items = [(i, p, r) for i, p, r in placed if i.against_wall]
    wall_ok = sum(against_wall(r, p.rotation, room) for _, p, r in wall_items)

    rel_ok = rel_n = 0

    def first(cat):
        return by_cat.get(cat, [None])[0]

    sofa, tv, table, bed, desk = first("sofa"), first("tv_stand"), first("coffee_table"), first("bed"), first("desk")
    if sofa and tv:
        rel_n += 1
        d = math.hypot(sofa[1].x - tv[1].x, sofa[1].z - tv[1].z)
        rel_ok += facing(sofa[1], tv[1].x, tv[1].z) >= 0.7 and facing(tv[1], sofa[1].x, sofa[1].z) >= 0.7 and 1.5 <= d <= 4.0
    if sofa and table:
        rel_n += 1
        d = math.hypot(sofa[1].x - table[1].x, sofa[1].z - table[1].z)
        rel_ok += facing(sofa[1], table[1].x, table[1].z) >= 0.7 and d <= sofa[0].depth / 2 + table[0].depth / 2 + 0.8
    for chair in by_cat.get("armchair", []):
        target = table or sofa
        if target:
            rel_n += 1
            d = math.hypot(chair[1].x - target[1].x, chair[1].z - target[1].z)
            rel_ok += facing(chair[1], target[1].x, target[1].z) >= 0.5 and d <= 2.0
    for stand in by_cat.get("nightstand", []):
        if bed:
            rel_n += 1
            gap = min(abs(stand[2].x1 - bed[2].x0), abs(bed[2].x1 - stand[2].x0), abs(stand[2].z1 - bed[2].z0), abs(bed[2].z1 - stand[2].z0))
            rel_ok += gap <= 0.3 and math.hypot(stand[1].x - bed[1].x, stand[1].z - bed[1].z) <= bed[0].width / 2 + stand[0].width / 2 + 0.5
    for chair in by_cat.get("office_chair", []):
        if desk:
            rel_n += 1
            d = math.hypot(chair[1].x - desk[1].x, chair[1].z - desk[1].z)
            rel_ok += facing(chair[1], desk[1].x, desk[1].z) >= 0.7 and d <= desk[0].depth / 2 + chair[0].depth / 2 + 0.4

    parts = {
        "walkway": walk_ok / walk_n if walk_n else None,
        "wall": wall_ok / len(wall_items) if wall_items else None,
        "relations": rel_ok / rel_n if rel_n else None,
    }
    present = [v for v in parts.values() if v is not None]
    return {"completion": float(len(placements) == len(item_ids)), "placed_share": len(placements) / len(item_ids),
            **parts, "guideline": statistics.mean(present) if present else 0.0}


def evaluate_layouts(requests: list[RecommendationRequest], rng: random.Random) -> list[dict]:
    rows = []
    for n, req in enumerate(requests):
        ids = layout_items(req)
        t0 = time.perf_counter()
        result = layout.auto_layout(LayoutRequest(room=req.room, item_ids=ids))
        runtime = time.perf_counter() - t0
        arca = evaluate_layout(req.room, ids, result.placements)
        runs = [evaluate_layout(req.room, ids, random_layout(req.room, ids, rng)[0]) for _ in range(B2_RUNS)]
        b2 = {k: statistics.mean(r[k] for r in runs if r[k] is not None) if any(r[k] is not None for r in runs) else None for k in arca}
        row = {"room": n, "room_type": req.room_type.value, "width": req.room.width, "length": req.room.length,
               "items": len(ids), "runtime_s": round(runtime, 3), "arca_violations": len(result.violations)}
        row.update({f"arca_{k}": None if v is None else round(v, 4) for k, v in arca.items()})
        row.update({f"b2_{k}": None if v is None else round(v, 4) for k, v in b2.items()})
        rows.append(row)
    return rows


# ---------- statistics ----------


def paired(rows: list[dict], a: str, b: str, rng: random.Random) -> dict:
    from scipy.stats import wilcoxon

    pairs = [(r[a], r[b]) for r in rows if r[a] is not None and r[b] is not None]
    diffs = [x - y for x, y in pairs]
    nonzero = [d for d in diffs if d != 0]
    ranks = _ranks([abs(d) for d in nonzero])
    w_pos = sum(r for r, d in zip(ranks, nonzero) if d > 0)
    w_neg = sum(r for r, d in zip(ranks, nonzero) if d < 0)
    boot = sorted(statistics.mean(rng.choices(diffs, k=len(diffs))) for _ in range(5000))
    test = wilcoxon([x for x, _ in pairs], [y for _, y in pairs]) if nonzero else None
    return {
        "n": len(pairs),
        "mean_a": statistics.mean(x for x, _ in pairs),
        "mean_b": statistics.mean(y for _, y in pairs),
        "mean_diff": statistics.mean(diffs),
        "ci95": [boot[125], boot[4874]],
        "wilcoxon_W": None if test is None else float(test.statistic),
        "p": None if test is None else float(test.pvalue),
        "rank_biserial": (w_pos - w_neg) / (w_pos + w_neg) if nonzero else 0.0,
    }


def _ranks(values: list[float]) -> list[float]:
    order = sorted(range(len(values)), key=values.__getitem__)
    ranks = [0.0] * len(values)
    i = 0
    while i < len(order):
        j = i
        while j + 1 < len(order) and values[order[j + 1]] == values[order[i]]:
            j += 1
        for k in range(i, j + 1):
            ranks[order[k]] = (i + j) / 2 + 1
        i = j + 1
    return ranks


def write_csv(path: Path, rows: list[dict]) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", type=Path, required=True, help="Parsed store JSON, e.g. pipeline/data/mebel_kz.json")
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()

    catalog.STORE_DATA_DIR = args.data.resolve().parent
    import os

    os.environ["CATALOG"] = args.data.stem
    catalog.load_catalog.cache_clear()
    args.out.mkdir(parents=True, exist_ok=True)

    rng = random.Random(SEED)
    rec_rows = evaluate_recommendations(scenarios(rng, N_REC))
    lay_rows = evaluate_layouts(scenarios(rng, N_LAYOUT), rng)
    write_csv(args.out / "h1_recommendation.csv", rec_rows)
    write_csv(args.out / "h2_layout.csv", lay_rows)

    stats_rng = random.Random(SEED)
    summary = {
        "catalog_items": len(catalog.load_catalog()),
        "seed": SEED,
        "h1": {f"{m}_arca_vs_{b}": paired(rec_rows, f"arca_{m}", f"{b}_{m}", stats_rng) for m in ("ndcg", "p", "fit") for b in ("b1", "b1s")},
        "h1_latency_s": {"median": statistics.median(r["latency_s"] for r in rec_rows), "max": max(r["latency_s"] for r in rec_rows)},
        "h1_bundle_within_budget": statistics.mean(r["bundle_within_budget"] for r in rec_rows),
        "h2": {m: paired(lay_rows, f"arca_{m}", f"b2_{m}", stats_rng) for m in ("completion", "placed_share", "walkway", "wall", "relations", "guideline")},
        "h2_runtime_s": {"median": statistics.median(r["runtime_s"] for r in lay_rows), "max": max(r["runtime_s"] for r in lay_rows)},
        "h2_hard_violations": sum(r["arca_violations"] for r in lay_rows),
    }
    (args.out / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
