from typing import Any

from regex import Match, compile

from ._utils import DELIM, Renderer


class Delimiter(Renderer):
    regex = compile(DELIM)

    def process(self, matches: Match[str]) -> str:
        return self.token()

    def render(self, options: dict[str, Any]) -> str:
        return DELIM
