from re import Match, compile
from typing import Any

from ._utils import Renderer


class XXX(Renderer):  # Rename It!
    regex = compile(r"")

    def process(self, matches: Match[str]) -> str:
        return ""

    def render(self, options: dict[str, Any]) -> str:
        return ""
