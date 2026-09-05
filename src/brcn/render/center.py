from typing import Any

from regex import Match, compile

from ._utils import Renderer


class Center(Renderer):
    regex = compile(r"\n\= (.*?)\n")

    def process(self, matches: Match[str]) -> str:
        start = self.token(type="start")
        end = self.token(type="end")
        return f"\n\n{start}{matches[1]}{end}\n\n"

    def render(self, options: dict[str, Any]) -> str:
        type = options["type"]
        if type == "start":
            return '<p style="text-align: center;">'
        return "</p>"
