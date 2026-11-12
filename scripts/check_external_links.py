"""Check public HTTP links in a rendered site; service refusals need manual review."""

import argparse
from concurrent.futures import ThreadPoolExecutor
import json
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urldefrag, urlsplit
from urllib.request import Request, urlopen

from check_site import Page


def check(url):
    request = Request(url, headers={'User-Agent': 'Python-for-Beginners-link-review/1.0'})
    try:
        with urlopen(request, timeout=25) as response:
            response.read(1024)  # GET avoids servers that reject HEAD; do not download whole files.
            return {'url': url, 'status': response.status, 'result': 'reachable', 'final_url': response.url}
    except HTTPError as error:
        result = 'broken' if error.code in {404, 410} else 'needs review'
        return {'url': url, 'status': error.code, 'result': result}
    except (URLError, TimeoutError, OSError) as error:
        return {'url': url, 'status': None, 'result': 'needs review', 'detail': str(error)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--site', type=Path, default=Path('_site'))
    parser.add_argument('--report', type=Path, default=Path('scratch/external-links.json'))
    args = parser.parse_args()
    assert (args.site / 'index.html').is_file(), 'Build the site first.'
    urls = set()
    for path in args.site.rglob('*.html'):
        for href in Page(path.read_text(encoding='utf-8')).links:
            url = urldefrag(href)[0]
            if urlsplit(url).scheme in {'http', 'https'}:
                urls.add(url)
    with ThreadPoolExecutor(max_workers=6) as executor:
        results = list(executor.map(check, sorted(urls)))
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(results, indent=2) + '\n', encoding='utf-8')
    for result in results:
        if result['result'] != 'reachable':
            print(f"{result['result']}: {result['status']} {result['url']}")
    counts = {label: sum(r['result'] == label for r in results)
              for label in ['reachable', 'broken', 'needs review']}
    print(f'HTTP review: {len(results)} links; {counts}. Details: {args.report}')
    raise SystemExit(1 if counts['broken'] else 0)


if __name__ == '__main__':
    main()
