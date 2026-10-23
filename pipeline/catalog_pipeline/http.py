"""HTTP fetcher that obeys robots.txt and a fixed request rate."""

import logging
import time
from urllib.parse import urlsplit

import requests

from . import robots

log = logging.getLogger(__name__)

USER_AGENT = "ArcaCatalogBot/0.1 (+https://github.com/a100miles/furniture-diploma; university project)"


class Disallowed(Exception):
    """The URL is blocked by the site's robots.txt."""


class PoliteFetcher:
    def __init__(self, base_url: str, delay: float = 2.0, retries: int = 3, timeout: float = 30.0):
        self.base_url = base_url.rstrip("/")
        self.retries = retries
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers["User-Agent"] = USER_AGENT
        self.requests_made = 0
        self.delay = delay
        self._last_request = 0.0

        self.rules = robots.parse(self._get(f"{self.base_url}/robots.txt", check_robots=False), USER_AGENT)
        # Never go faster than the site asks for.
        self.delay = max(delay, self.rules.crawl_delay or 0.0)

    def get(self, url: str) -> str:
        return self._get(url, check_robots=True)

    def _get(self, url: str, check_robots: bool) -> str:
        if urlsplit(url).netloc != urlsplit(self.base_url).netloc:
            raise ValueError(f"{url} is outside {self.base_url}")
        if check_robots and not self.rules.allowed(url):
            raise Disallowed(url)

        for attempt in range(self.retries + 1):
            self._wait()
            response = self.session.get(url, timeout=self.timeout)
            self.requests_made += 1
            if response.status_code in (429, 500, 502, 503, 504) and attempt < self.retries:
                pause = _retry_after(response) or 10.0 * (attempt + 1)
                log.warning("%s returned %s, retrying in %.0f s", url, response.status_code, pause)
                time.sleep(pause)
                continue
            response.raise_for_status()
            return response.text
        raise AssertionError("unreachable")

    def _wait(self) -> None:
        elapsed = time.monotonic() - self._last_request
        if elapsed < self.delay:
            time.sleep(self.delay - elapsed)
        self._last_request = time.monotonic()


def _retry_after(response: requests.Response) -> float | None:
    try:
        return float(response.headers["Retry-After"])
    except (KeyError, ValueError):
        return None
