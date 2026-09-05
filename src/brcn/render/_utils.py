from abc import ABC, abstractmethod
from re import (
    Match,
    Pattern,
    sub,
)
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from ..wiki import Wiki

DELIM = "\xFF"
RENDERERS: dict[str, type[Renderer]] = {}


class Renderer(ABC):
    regex: Pattern[str]

    def __init__(self, wiki: Wiki) -> None:
        self.wiki = wiki

    def token(self, **options: Any) -> str:
        self.wiki.tokens.append((type(self).__name__, options))
        return DELIM + str(len(self.wiki.tokens) - 1) + DELIM

    def parse(self, source: str) -> str:
        return sub(self.regex, self.process, source)

    def error(self, message: str) -> str:
        return f'<div class="error-block">{message}</div>'

    def attrs(self, text: str) -> dict[str, str]:
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

    @abstractmethod
    def process(self, matches: Match[str]) -> str:
        raise NotImplementedError

    @abstractmethod
    def render(self, options: dict[str, Any]) -> str:
        raise NotImplementedError

    def __init_subclass__(cls) -> None:
        name = cls.__name__
        assert name != "XXX", f"the renderer of module {cls.__module__} has not been renamed"
        assert name not in RENDERERS, f"{name} renderer redefined"
        RENDERERS[name] = cls
