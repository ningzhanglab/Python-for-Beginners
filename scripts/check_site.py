"""Check rendered internal links, fragment targets, downloads and image alt text."""

from html.parser import HTMLParser
import argparse
from pathlib import Path
from urllib.parse import unquote, urlsplit
import json

import nbformat

from check_course import check_exports, notebook_sources, notebook_download

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "_site"


class Page(HTMLParser):
    def __init__(self, source):
        super().__init__()
        self.ids = set()
        self.links = []
        self.images = []
        self.empty_table_headers = 0
        self._table_is_dataframe = False
        self._header = None
        self.feed(source)

    def handle_starttag(self, tag, attributes):
        attrs = dict(attributes)
        if tag == 'table':
            self._table_is_dataframe = 'dataframe' in attrs.get('class', '').split()
        if tag == 'th' and self._table_is_dataframe:
            self._header = []
        if "id" in attrs:
            self.ids.add(attrs["id"])
        if tag in {"a", "link", "script", "img"}:
            target = attrs.get("href") if tag in {"a", "link"} else attrs.get("src")
            if target:
                self.links.append(target)
        if tag == "img":
            self.images.append(attrs)

    def handle_data(self, text):
        if self._header is not None:
            self._header.append(text)

    def handle_endtag(self, tag):
        if tag == 'th' and self._header is not None:
            self.empty_table_headers += not ''.join(self._header).strip()
            self._header = None
        if tag == 'table':
            self._table_is_dataframe = False


def main():
    global SITE
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--site', type=Path, default=SITE, help='Rendered site folder.')
    SITE = parser.parse_args().site.resolve()
    pages = {path.resolve(): Page(path.read_text(encoding="utf-8")) for path in SITE.rglob("*.html")}
    assert (SITE / "index.html").resolve() in pages, "No landing page."
    failures = []
    for path, page in pages.items():
        if page.empty_table_headers:
            failures.append(f'{path.relative_to(SITE)}: unnamed pandas table header')
        for image in page.images:
            if not image.get("alt", "").strip() and image.get("role") != "presentation":
                failures.append(f"{path.relative_to(SITE)}: missing image alt text")
        for href in page.links:
            parts = urlsplit(href)
            own_site = parts.netloc == 'ningzhanglab.github.io' and parts.path.startswith('/Python-for-Beginners/')
            if ((parts.scheme or parts.netloc) and not own_site) or href == "#":
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
    for source in notebook_sources(ROOT):
        download = SITE / notebook_download(source, ROOT)
        if not download.exists() or download.read_bytes() != source.read_bytes():
            failures.append(f"Missing or stale notebook download: {source.name}")
    declared_exports = {exported for source in notebook_sources(ROOT)
                        for exported in nbformat.read(source, as_version=4).metadata.get('course', {}).get('exports', [])}
    for page in (SITE / 'downloads').rglob('*.html'):
        if page.relative_to(SITE).as_posix() not in declared_exports:
            failures.append(f'Unexpected rendered download: {page.relative_to(SITE)}')
    assert json.loads((SITE / "search.json").read_text(encoding="utf-8")), "Search index is empty."
    assert not failures, "\n".join(failures)
    assert (SITE / 'downloads/requirements.txt').read_bytes() == (ROOT / 'requirements.txt').read_bytes(), 'Stale shared dependency download.'
    check_exports(SITE, [nbformat.read(path, as_version=4) for path in notebook_sources(ROOT)])
    print(f"PASS: {len(pages)} rendered pages; local links/fragments, assets, notebook downloads, image alt text and search index.")


if __name__ == "__main__":
    main()
