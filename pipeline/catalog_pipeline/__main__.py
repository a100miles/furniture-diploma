"""Run a store parser and write normalised items plus an import report.

    python -m catalog_pipeline mebel_kz --out data/mebel_kz.json
"""

import argparse
import json
import logging
from collections import Counter
from dataclasses import asdict
from pathlib import Path

import requests

from .http import Disallowed, PoliteFetcher
from .normalize import Rejected
from .stores import mebel_kz

STORES = {mebel_kz.STORE: mebel_kz}


def main() -> None:
    parser = argparse.ArgumentParser(prog="catalog_pipeline")
    parser.add_argument("store", choices=STORES)
    parser.add_argument("--categories", help="comma-separated, default: all")
    parser.add_argument("--max-pages", type=int, help="per category slug")
    parser.add_argument("--delay", type=float, default=2.0, help="seconds between requests (default 2)")
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

    store = STORES[args.store]
    categories = args.categories.split(",") if args.categories else list(store.CATEGORIES)
    fetcher = PoliteFetcher(store.BASE_URL, delay=args.delay)

    def fetch(url: str) -> str:
        logging.info("GET %s", url)
        return fetcher.get(url)

    started_at = store.now()
    items, seen = [], set()
    detail_pages = 0
    rejected: Counter[str] = Counter()
    try:
        for category, card in store.crawl(fetch, categories, args.max_pages):
            if card["id"] in seen:
                continue
            seen.add(card["id"])
            try:
                size = None
                if not store.has_size(card):
                    size = store.product_page_size(fetch(store.product_url(card)))
                    detail_pages += 1
                items.append(store.to_item(card, category, started_at, size))
            except Rejected as reason:
                rejected[str(reason)] += 1
            except requests.RequestException as error:
                logging.warning("skipped %s: %s", card.get("link"), error)
                rejected["fetch_failed"] += 1
    except Disallowed as url:
        logging.error("blocked by robots.txt: %s", url)

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps([asdict(i) for i in items], ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    report = {
        "store": args.store,
        "started_at": started_at,
        "finished_at": store.now(),
        "requests": fetcher.requests_made,
        "product_pages_fetched": detail_pages,
        "delay_s": fetcher.delay,
        "rows_seen": len(seen),
        "items": len(items),
        "rows_rejected": sum(rejected.values()),
        "rejected_by_reason": dict(rejected),
        "items_by_category": dict(Counter(i.category for i in items)),
    }
    args.out.with_suffix(".report.json").write_text(json.dumps(report, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    logging.info("%d items, %d rejected -> %s", len(items), report["rows_rejected"], args.out)


if __name__ == "__main__":
    main()
