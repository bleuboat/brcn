from typing import Any

from regex import DOTALL, IGNORECASE, Match, compile

from ._utils import Renderer


class Button(Renderer):
    regex = compile(r"\[\[button\s+([a-z0-9\-_]+)(?:\s+(.+?))?\]\]", DOTALL | IGNORECASE)

    def process(self, matches: Match[str]) -> str:
        type = matches[1].replace("_", "-")
        attr = self.attrs(matches[2])
        options: dict[str, str] = {}
        for a in ("text", "class", "style"):
            if a in attr:
                options[a] = attr[a]
        return self.token(**options, type=type)

    def render(self, options: dict[str, Any]) -> str:
        type = options["type"]

        types2text = {
            "edit": "edit",
            "edit-append": "append",
            "edit-sections": "edit sections",
            "history": "history",
            "print": "print",
            "files": "files",
            "tags": "tags",
            "source": "view source",
            "talk": "talk",
            "backlinks": "backlinks",
        }

        if type not in types2text:
            return self.error("The button type is not recognized")
        
        text = options.get("text", types2text[type])
        class_ = options.get("class", "wiki-standalone-button")
        style = options.get("style", "")

        out = f'<a class="{class_}" '
        if style:
            out += f'style="{style}" '
        out += 'href="javascript:;">'
        out += text
        out += "</a>"
        return out
