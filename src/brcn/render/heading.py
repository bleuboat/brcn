from re import MULTILINE, Match, compile
from typing import Any

from ._utils import Renderer


class Heading(Renderer):
    regex = compile(r"^(\+{1,6}) (.*)", MULTILINE)

    def process(self, matches: Match[str]) -> str:
        if "headline_id" not in self.wiki.vars:
            self.wiki.vars["headline_id"] = 0
        headline_id = self.wiki.vars["headline_id"]
        start = self.token(type="start", level=len(matches[1]), text=matches[2], id=f"toc{headline_id}")
        end = self.token(type="end", level=len(matches[1]))
        self.wiki.vars["headline_id"] += 1
        return f"\n{start}{matches[2]}{end}\n\n"

    def render(self, options: dict[str, Any]) -> str:
        type = options["type"]
        level = options["level"]
        if type == "start":
            id = options["id"]
            return f'<h{level} id="{id}"><span>'
        return f"</span></h{level}>"
