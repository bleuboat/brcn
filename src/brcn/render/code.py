from typing import Any

from regex import DOTALL, IGNORECASE, MULTILINE, Match, compile

from ._utils import Renderer


class Code(Renderer):
    regex = compile(r"^\[\[code(\s[^\]]*)?\]\]((?:(?R)|.)*?)\[\[/code\]\](\s|$)", DOTALL | IGNORECASE | MULTILINE)

    def process(self, matches: Match[str]) -> str:
        return f"\n\n{self.token(text=matches[2])}{matches[3]}"

    def render(self, options: dict[str, Any]) -> str:
        text = options["text"]
        return f'\n<div class="code"><pre><code>{text}</code></pre></div>'
