from re import Match, compile
from typing import Any

from ._utils import Renderer


class Strong(Renderer):
    regex = compile(r"\*\*([^\s\n](?:.*?[^\s\n])?)\*\*")

    def process(self, matches: Match[str]) -> str:
        start = self.token(type="start")
        end = self.token(type="end")
        return start + matches[1] + end

    def render(self, options: dict[str, Any]) -> str:
        type = options["type"]
        if type == "start":
            return "<strong>"
        return "</strong>\n\n"
