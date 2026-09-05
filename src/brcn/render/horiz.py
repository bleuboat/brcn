from typing import Any

from regex import MULTILINE, Match, compile

from ._utils import Renderer


class Horiz(Renderer):
    regex = compile(r"^([-]{4,})$", MULTILINE)

    def process(self, matches: Match[str]) -> str:
        return f"\n{self.token()}\n\n"
    
    def render(self, options: dict[str, Any]) -> str:
        return "<hr>"
