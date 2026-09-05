from regex import sub

from ._utils import Renderer

REPLACEMENTS = {
    "``": "&#8220;",
    "''": "&#8221;",
    ",,": "&#8222;",
    "`": "&#8216;",
    "'": "&#8217;",
    "<<": "&#171;",
    ">>": "&#187;",
    " ": "&#160;",
    "...": "&#8230;",
    "--": "&#8212;",
    "---": "&#8212;",
}


class Typography(Renderer):
    def _parse(self, source: str) -> str:
        source = sub(
            r"``(.*?)''",
            REPLACEMENTS["``"] + r"\1" + REPLACEMENTS["''"],
            source,
        )
        source = sub(
            r",,(.*?)''",
            REPLACEMENTS[",,"] + r"\1" + REPLACEMENTS["''"],
            source,
        )
        source = sub(
            r"`(.*?)'",
            REPLACEMENTS["`"] + r"\1" + REPLACEMENTS["'"],
            source,
        )
        source = sub(
            r"<<",
            REPLACEMENTS["<<"],
            source,
        )
        source = sub(
            r">>",
            REPLACEMENTS[">>"],
            source,
        )
        source = sub(
            r"(?<=[0-9]) (?=[0-9])",
            REPLACEMENTS[" "],
            source,
        )
        source = sub(
            r"\.\.\.|\. \. \.",
            REPLACEMENTS["..."],
            source,
        )
        source = sub(
            r"--",
            REPLACEMENTS["--"],
            source,
        )
        source = sub(
            r"---",
            REPLACEMENTS["---"],
            source,
        )
        return source
