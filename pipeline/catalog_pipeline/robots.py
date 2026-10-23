"""robots.txt rules with `*` and `$` wildcards (RFC 9309).

The standard library's urllib.robotparser treats patterns as plain prefixes,
so rules such as `Disallow: *order` used by mebel.kz would never match.
"""

import re
from dataclasses import dataclass, field
from urllib.parse import urlsplit


@dataclass
class Rules:
    allow: list[str] = field(default_factory=list)
    disallow: list[str] = field(default_factory=list)
    crawl_delay: float | None = None

    def allowed(self, url: str) -> bool:
        parts = urlsplit(url)
        path = (parts.path or "/") + (f"?{parts.query}" if parts.query else "")
        best_allow = max((len(p) for p in self.allow if _matches(p, path)), default=-1)
        best_disallow = max((len(p) for p in self.disallow if _matches(p, path)), default=-1)
        # The longest matching rule wins; on a tie, Allow wins.
        return best_allow >= best_disallow


def _matches(pattern: str, path: str) -> bool:
    if not pattern:
        return False
    regex = re.escape(pattern).replace(r"\*", ".*")
    if regex.endswith(r"\$"):
        regex = regex[:-2] + "$"
    if not regex.startswith(".*") and not pattern.startswith("/"):
        regex = ".*" + regex
    return re.match(regex, path) is not None


def parse(text: str, user_agent: str) -> Rules:
    """Return the rules of the group for `user_agent`, falling back to `*`."""
    groups: list[tuple[list[str], Rules]] = []
    agents: list[str] = []
    rules: Rules | None = None
    for raw in text.splitlines():
        line = raw.split("#", 1)[0].strip()
        if ":" not in line:
            continue
        key, value = (s.strip() for s in line.split(":", 1))
        key = key.lower()
        if key == "user-agent":
            if rules is not None:
                agents, rules = [], None
            agents.append(value.lower())
        elif key in ("allow", "disallow", "crawl-delay") and agents:
            if rules is None:
                rules = Rules()
                groups.append((agents, rules))
            if key == "allow":
                rules.allow.append(value)
            elif key == "disallow":
                rules.disallow.append(value)
            else:
                try:
                    rules.crawl_delay = float(value)
                except ValueError:
                    pass

    token = user_agent.split("/", 1)[0].lower()
    for names, group in groups:
        if token in names:
            return group
    for names, group in groups:
        if "*" in names:
            return group
    return Rules()
