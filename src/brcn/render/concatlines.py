from regex import Match, compile

from ._utils import Renderer


class Concatlines(Renderer):
    regex = compile(r"\\\n")

    def process(self, matches: Match[str]) -> str:
        return ""
