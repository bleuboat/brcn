from re import DOTALL, IGNORECASE, Match, compile
from typing import Any

from ._utils import Renderer


class Comment(Renderer):
    regex = compile(r"(\n)?\[!\-\-(.*?)\-\-\]", DOTALL | IGNORECASE)

    def process(self, matches: Match[str]) -> str:
        return ""
    
    def render(self, options: dict[str, Any]) -> str:
        return ""
