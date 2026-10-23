from catalog_pipeline import robots

# Excerpt of https://mebel.kz/robots.txt (23 Oct 2026) plus a bot-specific group.
ROBOTS = """
User-Agent: *
Allow: *.png
Disallow: *order
Disallow: /other/
Disallow: */params
Crawl-delay: 1

User-Agent: OtherBot
Disallow: /
"""


def test_wildcard_rules():
    rules = robots.parse(ROBOTS, "ArcaCatalogBot/0.1")
    assert rules.allowed("https://mebel.kz/category/divany/page-2")
    assert not rules.allowed("https://mebel.kz/order")
    assert not rules.allowed("https://mebel.kz/cart/order/5")
    assert not rules.allowed("https://mebel.kz/other/x")
    assert not rules.allowed("https://mebel.kz/category/divany/params")
    assert rules.crawl_delay == 1.0


def test_longest_match_wins_and_allow_wins_ties():
    rules = robots.parse("User-agent: *\nDisallow: /shop\nAllow: /shop/catalog\nAllow: /x\nDisallow: /x\n", "ArcaCatalogBot")
    assert rules.allowed("https://x.kz/shop/catalog/1")
    assert not rules.allowed("https://x.kz/shop/cart")
    assert rules.allowed("https://x.kz/x")


def test_specific_group_overrides_star():
    assert not robots.parse(ROBOTS, "OtherBot/2.0").allowed("https://mebel.kz/category/divany")


def test_end_anchor():
    rules = robots.parse("User-agent: *\nDisallow: /*.pdf$\n", "ArcaCatalogBot")
    assert not rules.allowed("https://x.kz/files/a.pdf")
    assert rules.allowed("https://x.kz/files/a.pdf?view=1")


def test_empty_robots_allows_everything():
    assert robots.parse("", "ArcaCatalogBot").allowed("https://x.kz/anything")
