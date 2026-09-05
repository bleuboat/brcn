from typing import Any

from regex import MULTILINE, Match, compile

from ._utils import Renderer


class Newline(Renderer):
    regex = compile(r"([^\n])\n(?!\n)", MULTILINE)

    def process(self, matches: Match[str]) -> str:
        return f"{matches[1]}{self.token()}"
    
    def render(self, options: dict[str, Any]) -> str:
        return "<br>"
