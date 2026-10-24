from datetime import datetime, timezone

import pytest
import requests

from catalog_pipeline import http


NOW = datetime(2015, 10, 21, 7, 27, 0, tzinfo=timezone.utc).timestamp()


def response(status=200, retry_after=None):
    result = requests.Response()
    result.status_code = status
    result._content = b"ok"
    if retry_after is not None:
        result.headers["Retry-After"] = retry_after
    return result


@pytest.mark.parametrize(
    ("header", "expected"),
    [
        ("120", 120.0),
        ("0", 0.0),
        ("Wed, 21 Oct 2015 07:28:00 GMT", 60.0),
        ("Wednesday, 21-Oct-15 07:28:00 GMT", 60.0),
        ("Wed Oct 21 07:28:00 2015", 60.0),
        ("Wed, 21 Oct 2015 07:26:00 GMT", 0.0),
        (None, None),
        ("invalid", None),
        ("", None),
        ("-1", None),
        ("nan", None),
        ("inf", None),
    ],
)
def test_retry_after(header, expected, monkeypatch):
    monkeypatch.setattr(http.time, "time", lambda: NOW)
    assert http._retry_after(response(retry_after=header)) == expected


@pytest.mark.parametrize(
    ("header", "expected_delay"),
    [
        ("Wed, 21 Oct 2015 07:28:00 GMT", 60.0),
        ("Wed, 21 Oct 2015 07:26:00 GMT", 0.0),
        ("0", 0.0),
        ("invalid", 10.0),
    ],
)
def test_fetcher_honours_retry_after(header, expected_delay, monkeypatch):
    responses = iter([response(), response(429, header), response()])
    monkeypatch.setattr(requests.Session, "get", lambda *args, **kwargs: next(responses))
    monkeypatch.setattr(http.time, "time", lambda: NOW)
    sleeps = []
    monkeypatch.setattr(http.time, "sleep", sleeps.append)

    fetcher = http.PoliteFetcher("https://example.test", delay=0)
    assert fetcher.get("https://example.test/items") == "ok"
    assert sleeps == [expected_delay]
    assert fetcher.requests_made == 3
