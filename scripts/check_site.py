"""Check rendered internal links, fragment targets, downloads and image alt text."""

from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
import json

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "_site"


class Page(HTMLParser):
    def __init__(self, source):
        super().__init__()
        self.ids = set()
        self.links = []
        self.images = []
        self.feed(source)

    def handle_starttag(self, tag, attributes):
        attrs = dict(attributes)
        if "id" in attrs:
            self.ids.add(attrs["id"])
        if tag in {"a", "link", "script", "img"}:
            target = attrs.get("href") if tag in {"a", "link"} else attrs.get("src")
            if target:
                self.links.append(target)
        if tag == "img":
            self.images.append(attrs)


def main():
    pages = {path.resolve(): Page(path.read_text()) for path in SITE.rglob("*.html")}
    assert (SITE / "index.html").resolve() in pages, "No landing page."
    failures = []
    for path, page in pages.items():
        for image in page.images:
            if not image.get("alt", "").strip() and image.get("role") != "presentation":
                failures.append(f"{path.relative_to(SITE)}: missing image alt text")
        for href in page.links:
            parts = urlsplit(href)
            if parts.scheme or parts.netloc or href == "#":
                continue
            url_path = unquote(parts.path)
            if url_path.startswith("/Python-for-Beginners/"):
                target = SITE / url_path.removeprefix("/Python-for-Beginners/")
            elif url_path.startswith("/"):
                target = SITE / url_path.lstrip("/")
            else:
                target = path.parent / url_path if url_path else path
            if target.is_dir():
                target /= "index.html"
            target = target.resolve()
            if not target.exists():
                failures.append(f"{path.relative_to(SITE)}: broken target {href}")
            elif parts.fragment and target in pages and unquote(parts.fragment) not in pages[target].ids:
                failures.append(f"{path.relative_to(SITE)}: missing fragment {href}")
    for source in (ROOT / "lessons").rglob("*.ipynb"):
        download = SITE / "downloads" / source.relative_to(ROOT / "lessons")
        if not download.exists() or download.read_bytes() != source.read_bytes():
            failures.append(f"Missing or stale notebook download: {source.name}")
    assert json.loads((SITE / "search.json").read_text()), "Search index is empty."
    assert not failures, "\n".join(failures)
    print(f"PASS: {len(pages)} rendered pages; local links/fragments, assets, notebook downloads, image alt text and search index.")


if __name__ == "__main__":
    main()
