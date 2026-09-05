from typing import Any

from regex import Match, compile

from ._utils import Renderer


class Break(Renderer):
    regex = compile(r" _\n")

    def process(self, matches: Match[str]) -> str:
        return self.token()

    def render(self, options: dict[str, Any]) -> str:
        return "<br>"
