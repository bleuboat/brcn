from typing import Any

from regex import DOTALL, IGNORECASE, MULTILINE, Match, compile

from ._utils import Renderer

ALIGNS = {
    "=": "center",
    "<": "left",
    ">": "right",
    "==": "justify",
}


class Divalign(Renderer):
    regex = compile(r"^\[\[(=|<|>|==)\]\]\n((?:(?R)|.)*?)\[\[/\1\]\]$", DOTALL | IGNORECASE | MULTILINE)

    def process(self, matches: Match[str]) -> str:
        align = ALIGNS[matches[1]]
        content = matches[2]
        start = self.token(type="start", align=align)
        end = self.token(type="end")
        return f"{start}\n\n{content}\n\n{end}"

    def render(self, options: dict[str, Any]) -> str:
        type = options["type"]
        if type == "start":
            align = options["align"]
            return f'<div style="text-align: {align};">'
        return "</div>"
