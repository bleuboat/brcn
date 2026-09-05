from typing import Any

from regex import DOTALL, IGNORECASE, MULTILINE, Match, compile

from ._utils import Renderer


class Div(Renderer):
    regex = compile(r"(\n)?\[\[div(\s.*?)?\]\] *\n((?:(?R)|.)*?)\[\[\/div\]\] *", DOTALL | IGNORECASE | MULTILINE)

    def process(self, matches: Match[str]) -> str:
        content = matches[3]
        attr = self.attrs(matches[2])
        args: dict[str, str] = {}
        if "class" in attr:
            args["class"] = attr["class"]
        if "style" in attr:
            args["style"] = attr["style"]
        start = self.token(type="start", args=args)
        end = self.token(type="end")
        return matches[1] + matches[1] + start + "\n\n" + content + "\n\n" + end

    def render(self, options: dict[str, Any]) -> str:
        type = options["type"]
        if type == "start":
            args = options["args"]
            argstr = " ".join(f'{k}="{v}"' for k, v in args.items())
            return f"<div {argstr}>"
        return "</div>"
