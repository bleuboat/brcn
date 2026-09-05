from typing import Any

from regex import DOTALL, MULTILINE, Match, compile, finditer

from ._utils import Renderer


class Deflist(Renderer):
    regex = compile(r"\n((: ).*?\n)(?!(: |\n))", DOTALL)

    def process(self, matches: Match[str]) -> str:
        ret: list[str] = []
        ret.append(self.token(type="list_start"))
        for val in finditer(r"^(: )(.*?)?( : )(.*?)?$", matches[1], DOTALL | MULTILINE):
            ret.extend((
                self.token(type="term_start"),
                val[2].strip(),
                self.token(type="term_end"),
                self.token(type="narr_start"),
                val[4].strip(),
                self.token(type="narr_end"),
            ))
        ret.append(self.token(type="list_end"))
        return f"\n{"".join(ret)}\n\n"

    def render(self, options: dict[str, Any]) -> str:
        match options["type"]:
            case "list_start":
                return "<dl>\n"
            case "list_end":
                return "</dl>\n\n"
            case "term_start":
                return "    <dt>\n"
            case "term_end":
                return "</dt>\n\n"
            case "narr_start":
                return "        <dd>\n"
            case "narr_end":
                return "</dd>\n\n"
            case _:
                return ""
