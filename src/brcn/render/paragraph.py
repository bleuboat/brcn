from typing import Any

from regex import DOTALL, MULTILINE, Match, compile

from ._utils import DELIM, Renderer


class Paragraph(Renderer):
    regex = compile(r"^(.*?)\n\s*?\n", DOTALL | MULTILINE)

    def process(self, matches: Match[str]) -> str:
        match = matches[0].strip()
        if not match:
            return ""
        if match[0] != DELIM:
            start = self.token(type="start")
            end = self.token(type="end")
            return f"{start}{matches[0]}{end}\n\n"
        return matches[0]

    def render(self, options: dict[str, Any]) -> str:
        type = options["type"]
        if type == "start":
            return "<p>"
        return "</p>\n\n"
