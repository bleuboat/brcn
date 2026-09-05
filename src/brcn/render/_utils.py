from logging import getLogger
from traceback import format_exc
from typing import TYPE_CHECKING, Any

from regex import (
    Match,
    Pattern,
    sub,
)

if TYPE_CHECKING:
    from ..wiki import Wiki

logger = getLogger(__name__)

DELIM = "\xFF"
RENDERERS: dict[str, type[Renderer]] = {}
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


class Renderer:
    regex: Pattern[str]

    def __init__(self, wiki: Wiki) -> None:
        self.wiki = wiki

    def token(self, **options: Any) -> str:
        self.wiki.tokens.append((type(self).__name__, options))
        return DELIM + str(len(self.wiki.tokens) - 1) + DELIM

    def _parse(self, source: str) -> str:
        return sub(self.regex, self.process, source)

    def parse(self, source: str) -> str:
        try:
            source = self._parse(source)
        except Exception:  # noqa: BLE001
            logger.error(format_exc())
        return source

    def error(self, message: str) -> str:
        return f'<div class="error-block">{message}</div>'

    def attrs(self, text: str | None) -> dict[str, str]:
        if text is None:
            return {}
        tmp = text.strip().split('="')
        attrs: dict[str, str] = {}
        key = None
        for i, val in enumerate(tmp):
            if i == 0:
                key = val.strip()
                continue
            assert key is not None
            pos = val.index('"')
            attrs[key] = val[:pos]
            key = val[pos + 1:].strip()
        return attrs

    def process(self, matches: Match[str]) -> str:
        raise NotImplementedError

    def render(self, options: dict[str, Any]) -> str:
        raise NotImplementedError

    def __init_subclass__(cls) -> None:
        name = cls.__name__
        assert name != "XXX", f"the renderer of module {cls.__module__} has not been renamed"
        assert name in RULES, f"{name} renderer unused"
        assert name not in RENDERERS, f"{name} renderer redefined"
        RENDERERS[name] = cls
