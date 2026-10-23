# Catalogue pipeline

**Task:** DIP-25 · **Requirement:** FR-31

Python parsers that collect furniture from Kazakhstan online stores and normalise it into one schema (`furniture_items` in [database-schema.md](../docs/database-schema.md)). Until PostgreSQL persistence lands (DIP-17), the output is a JSON file per store plus an import report.

## Run

```bash
cd pipeline
python -m venv .venv && source .venv/bin/activate
pip install -r requirements-dev.txt

python -m catalog_pipeline mebel_kz --out data/mebel_kz.json                       # all categories
python -m catalog_pipeline mebel_kz --categories sofa,bed --max-pages 2 --out /tmp/sample.json
pytest -q
```

Each run writes `<out>.json` (items) and `<out>.report.json` (requests made, rows seen, items kept, rejected rows by reason, items per category).

## Politeness

- `robots.txt` is fetched first and every URL is checked against it, with `*` and `$` wildcards (`urllib.robotparser` ignores wildcards, and mebel.kz uses them).
- One request at a time, at least 2 s apart (`--delay`), never faster than the site's `Crawl-delay`.
- 429 and 5xx responses are retried with back-off, honouring `Retry-After`.
- The user agent names the project and links to this repository.

## Stores

### mebel.kz

Category pages embed complete product cards in the Next.js (React Server Components) payload, so one listing page gives ~50 items with name, price, colour, category, images and size in cm. Cards that only carry the sleeping-area size (mostly configurable beds) are completed from the product page: overall length and width from "Размеры", height from "Высота" or, if absent, the selected headboard height.

| Our category | mebel.kz slugs |
|--------------|----------------|
| sofa | `divany` |
| armchair | `kresla` |
| office_chair | `kompyuternye-kresla` |
| bed | `krovati` |
| coffee_table | `zurnalnye-stoliki` |
| nightstand | `prikrovatnye-tumby` |
| wardrobe | `shkafy` |
| bookshelf | `stellazhi`, `knizhnye-shkafy` |
| desk | `stoly-pismennye-i-kompyuternye` |
| tv_stand | `tv-tumby` |

An item listed in several categories is kept once, under the first category in this table that lists it (for example, the bedside-table listing also shows coffee tables, so `coffee_table` comes first).

## Normalisation

| Field | Rule |
|-------|------|
| `width_cm`, `depth_cm`, `height_cm` | Integer cm. The store lists length × width × height; length becomes `width_cm` (along the wall), except for beds, whose width runs along the wall. Sleeping-area size is never used as the footprint. |
| `price_kzt` | Integer KZT, current price shown on the listing (Almaty region by default). |
| `external_id` | Store product id; with `store` it is the upsert key. |
| `scraped_at` | Start of the run (UTC), so prices are dated. |

Rows are rejected and counted in the report when dimensions are missing, any dimension is outside 10-500 cm, the price is missing, or the product page cannot be fetched.

## Known limitations

- One store so far; FR-31 needs at least two stores and 5 000 items by pre-defense 2.
- No style tags yet; they come from CLIP (DIP-28) or rules on name and category.
- Colour is the store's own colour name, not a hex value; material is filled only when the card lists it.
- Categories follow the store's listings, which mix in some related items (e.g. wall consoles and office pedestals under desks, single modules under sofas). `source_category` keeps the store's own category for later filtering.
