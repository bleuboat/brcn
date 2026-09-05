from typing import Any

from regex import DOTALL, MULTILINE, Match, compile, findall

from ._utils import Renderer


class List(Renderer):
    regex = compile(r"^((\*|#) .*?\n)(?!\2 |(?: {1,}((?:\*|#) |\n)))", DOTALL | MULTILINE)

    def process(self, matches: Match[str]) -> str:
        lst: list[tuple[str, str, str]] = findall(r"^( {0,})(\*|#) (.*?)$", matches[1], DOTALL | MULTILINE)
        ret: list[str] = []
        stack: list[str] = []
        itemcount: list[int] = []
        for val in lst:
            print(val)
            level = len(val[0]) + 1
            type = {"*": "bullet", "#": "number"}[val[1]]
            if level > len(stack):
                stack.append(type)
                ret.append(self.token(type=f"{type}_list_start", level=level - 1))
            while len(stack) > level:
                tmp = len(stack) - 1
                ret.append(self.token(type=f"{stack.pop()}_list_end", level=tmp))
                type = stack[tmp - 1]
                if tmp + 1 < len(itemcount):
                    del itemcount[tmp + 1]
            while len(itemcount) <= level:
                itemcount.append(-1)
            itemcount[level] += 1
            start = self.token(type="item_start", level=level, count=itemcount[level])
            end = self.token(type="item_end", level=level)
            ret.extend((start, val[2], end))
        while stack:
            ret.append(self.token(type=f"{stack.pop()}_list_end", level=len(stack)))
        return f"\n\n{"".join(ret)}\n\n"
                
    def render(self, options: dict[str, Any]) -> str:
        type = options["type"]
        level = options["level"]
        pad = "    " * level
        match type:
            case "bullet_list_start":
                return "<ul>"
            case "bullet_list_end":
                return f"</li>{pad}</ul>{"\n\n" if level == 0 else ""}"
            case "number_list_start":
                return "<ol>"
            case "number_list_end":
                return f"</li>{pad}</ol>{"\n\n" if level == 0 else ""}"
            case "item_start":
                count = options["count"]
                return f"{"</li>" if count > 0 else ""}\n{pad}<li>"
            case _:
                return ""
