from json import dumps, loads
from pathlib import Path
from typing import cast

from playwright.sync_api import Locator, sync_playwright


def get_data(div: Locator, name: str) -> tuple[str, str]:
    value = div.locator(f".{name}").text_content()
    assert value is not None
    return name, value


def get() -> None:
    metadata_path = Path("metadata")
    metadata_path.mkdir(exist_ok=True)
    source_path = Path("source")
    source_path.mkdir(exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch(
            channel="chrome",
            # headless=False,
        )
        page = browser.new_page()
        page2 = browser.new_page()

        page.goto("https://backrooms-wiki-cn.wikidot.com/fragment:bleuboat")

        n = page.text_content("#page-content .pager > .target:nth-last-child(2) a")

        assert n is not None

        for p in range(int(n)):
            if p > 0:
                page.goto(f"https://backrooms-wiki-cn.wikidot.com/fragment:bleuboat/p/{p + 1}")
            for div in page.locator("#page-content .list-pages-item").all():
                data = dict((
                    get_data(div, "name"),
                    get_data(div, "category"),
                    get_data(div, "fullname"),
                    get_data(div, "title"),
                    get_data(div, "parent"),
                    get_data(div, "tags"),
                    get_data(div, "_tags"),
                    get_data(div, "revisions"),
                ))

                metadata_category = metadata_path / data["category"]
                metadata_category.mkdir(exist_ok=True)
                page_metadata_path = metadata_category / f"{data["name"]}.json"

                source_category = source_path / data["category"]
                source_category.mkdir(exist_ok=True)
                page_source_path = source_category / f"{data["name"]}.txt"

                if page_metadata_path.exists() and page_source_path.exists():
                    old_data = cast(dict[str, str], loads(page_metadata_path.read_text("utf-8")))

                    if old_data["revisions"] == data["revisions"]:
                        print(f"{data["title"]} 使用已下载的版本")
                        continue

                print(f"正在下载 {data["title"]}")

                page_metadata_path.write_text(dumps(data, ensure_ascii=False, indent=2), "utf-8")

                page2.goto(f"https://backrooms-wiki-cn.wikidot.com/{data["fullname"]}/norender/true")
                page2.locator("#more-options-button").click()
                page2.locator("#view-source-button").click()
                source = page2.locator("#action-area > .page-source").text_content()

                assert source is not None

                page_source_path.write_text(source[2:], "utf-8")

        browser.close()
