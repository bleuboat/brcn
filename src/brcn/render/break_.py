from re import Match, compile
from typing import Any

from ._utils import Renderer


class Break(Renderer):
    regex = compile(r" _\n")

    def process(self, matches: Match[str]) -> str:
        return self.token()

    def render(self, options: dict[str, Any]) -> str:
        return "<br>"
