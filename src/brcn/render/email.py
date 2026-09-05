from typing import Any

from regex import IGNORECASE, Match, compile, sub

from ._utils import Renderer


class Email(Renderer):
    regex = compile(r"[_a-z0-9\-]+(?:\.[_a-z0-9\-]+)*@[a-z0-9\-]+(?:\.[a-z0-9\-]+)+")

    def _parse(self, source: str) -> str:
        regex = r"\[([_a-z0-9\-]+(?:\.[_a-z0-9\-]+)*@[a-z0-9\-]+(?:\.[a-z0-9\-]+)+) (.+?)\]"
        source = sub(regex, self.process_descr, source, IGNORECASE)
        return sub(self.regex, self.process, source, IGNORECASE)

    def process(self, matches: Match[str]) -> str:
        return self.token(email=matches[0], text=matches[0])

    def process_descr(self, matches: Match[str]) -> str:
        return self.token(email=matches[1], text=matches[2])

    def render(self, options: dict[str, Any]) -> str:
        email = options["email"]
        text = options["text"]
        return f'<span class="wiki-email" style="visibility: visible;"><a href="mailto:{email}">{text}</a></span>'
