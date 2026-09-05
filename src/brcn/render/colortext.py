from typing import Any

from regex import Match, compile

from ._utils import Renderer

COLORS = [
    "aqua",
    "black",
    "blue",
    "fuchsia",
    "gray",
    "green",
    "lime",
    "maroon",
    "navy",
    "olive",
    "purple",
    "red",
    "silver",
    "teal",
    "white",
    "yellow",
]


class Colortext(Renderer):
    regex = compile(r"\#\#(.+?)\|(.+?)\#\#")

    def process(self, matches: Match[str]) -> str:
        start = self.token(type="start", color=matches[1])
        end = self.token(type="end", color=matches[1])
        return start + matches[2] + end

    def render(self, options: dict[str, Any]) -> str:
        type = options["type"]
        color = options["color"]
        if color not in COLORS and color[0] != "#":
            color = "#" + color
        if type == "start":
            return f'<span style="color: {color};">'
        return "</span>"
