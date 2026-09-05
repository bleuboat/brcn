from re import IGNORECASE, Match, compile
from typing import Any

from ._utils import Renderer


class Anchor(Renderer):
    regex = compile(r"\[\[# ([-_A-Za-z0-9.%]+?)\]\]", IGNORECASE)

    def process(self, matches: Match[str]) -> str:
        return self.token(name=matches[1])

    def render(self, options: dict[str, Any]) -> str:
        name = options["name"]
        return f"<a name={name}></a>"
