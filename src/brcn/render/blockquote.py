from re import DOTALL, MULTILINE, Match, compile, findall
from typing import Any

from ._utils import Renderer


class Blockquote(Renderer):
    regex = compile(r"\n((\>).*?\n)(?!\>)", DOTALL)

    def process(self, matches: Match[str]) -> str:
        ret = ""
        lst: list[tuple[str, str]] = findall(r"^(\>+) (.*\n)", matches[1], MULTILINE)
        count = 0
        for val in lst:
            level = len(val[0])
            text = val[1]
            while level > count:
                count += 1
                ret += "\n"
                ret += self.token(type="start", level=level - 1)
                ret += "\n\n"
            while count > level:
                count -= 1
                ret += "\n\n"
                ret += self.token(type="end", level=count)
                ret += "\n"
            ret += text
        ret += "\n"
        while count > 0:
            count -= 1
            ret += self.token(type="end", level=count)
        return f"\n{ret}\n\n"

    def render(self, options: dict[str, Any]) -> str:
        type = options["type"]
        level = options["level"]
        pad = "    " * level
        if type == "start":
            return f"{pad}<blockquote>"
        return f"{pad}</blockquote>\n"