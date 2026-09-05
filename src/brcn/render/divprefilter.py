from regex import DOTALL, IGNORECASE, MULTILINE, Match, compile

from ._utils import Renderer


class Divprefilter(Renderer):
    regex = compile(r"\[\[/div\]\](\s*?)\[\[div", DOTALL | IGNORECASE | MULTILINE)

    def process(self, matches: Match[str]) -> str:
        return "[[/div]][[div"
