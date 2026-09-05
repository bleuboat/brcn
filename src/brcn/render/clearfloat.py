from typing import Any

from regex import MULTILINE, Match, compile

from ._utils import Renderer


class Clearfloat(Renderer):
    regex = compile(r"^([~]{4,})(>|<)?$", MULTILINE)

    def process(self, matches: Match[str]) -> str:
        return f"\n\n{self.token(side=matches[2])}\n\n"
    
    def render(self, options: dict[str, Any]) -> str:
        match options["side"]:
            case ">":
                side = "right"
            case "<":
                side = "left"
            case _:
                side = "both"
        return f'<div style="clear:{side}; height: 0px; font-size: 1px"></div>\n'
