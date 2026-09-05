from typing import Any

from .render import DELIM, RENDERERS, Renderer

RULES = [
    "Include",
    "Prefilter",
    "Delimiter",
    "Code",
    "Form",
    "Raw",
    "Rawold",
    "Modulepre",
    "Module",
    "Module654",
    "Iftags",
    "Comment",
    "Iframe",
    "Date",
    "Math",
    "Concatlines",
    "Freelink",
    "Equationreference",
    "Footnote",
    "Footnoteitem",
    "Footnoteblock",
    "Bibitem",
    "Bibliography",
    "Bibcite",
    "Divprefilter",
    "Anchor",
    "User",
    "Blockquote",
    "Heading",
    "Toc",
    "Horiz",
    "Separator",
    "Clearfloat",
    "Break",
    "Span",
    "Size",
    "Div",
    "Divalign",
    "Collapsible",
    "Tabview",
    "Note",
    "Gallery",
    "List",
    "Deflist",
    "Table",
    "Tableadv",
    "Button",
    "Image",
    "Embed",
    "Social",
    "File",
    "Center",
    "Newline",
    "Paragraph" ,
    "Url",
    "Email",
    "Mathinline",
    "Interwiki",
    "Colortext",
    "Strong",
    "Emphasis",
    "Underline",
    "Strikethrough",
    "Tt",
    "Superscript",
    "Subscript",
    "Typography",
    "Tighten",
]


class Wiki:
    def __init__(self) -> None:
        self.tokens: list[tuple[str, dict[str, Any]]] = []
        self.vars: dict[str, Any] = {}
        self.renderers: dict[str, Renderer] = {}

    def parse(self, source: str) -> str:
        if not self.renderers:
            for rule in RULES:
                renderer = RENDERERS.get(rule)
                if not renderer:
                    continue
                self.renderers[renderer.__name__] = renderer(self)
        for renderer in self.renderers.values():
            source = renderer.parse(source)
        return source

    def render(self, source: str) -> str:
        output: list[str] = []
        key: list[str] = []
        in_delim = False
        for char in self.parse(source):
            if in_delim:
                if char == DELIM:
                    int_key = int("".join(key))
                    rule = self.tokens[int_key][0]
                    opts = self.tokens[int_key][1]
                    output.append(self.renderers[rule].render(opts))
                    in_delim = False
                else:
                    key.append(char)
            else:
                if char == DELIM:
                    key = []
                    in_delim = True
                else:
                    output.append(char)
        return "".join(output)


if __name__ == "__main__":
    source = """
~~~~
~~~~<
~~~~>
~~~~=
"""
    output = Wiki().render(source)
    print(output)
