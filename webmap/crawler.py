from time import perf_counter
import requests
import sys

import extract
from url import Url
from config import config
from modutils import trimf, unique_list

def get(url : str) -> str | None:
    try:
        req = requests.get(url, allow_redirects=True)
        if req:
            return (req.content.decode('utf-8'), req.status_code)
        else:
            return (None, req.status_code)
    except Exception:
        return (None, 0)

def parse_site(url : str) -> tuple[list[Url], int, int] | None:
    u = Url(url)
    host = u.host()
    content, status = get(url)

    if content is None:
        return (None, 0, status)

    urls = []
    urls += Url.from_list(host, extract.raw_urls(content))
    urls += Url.from_list(host, extract.hrefs(content))
    urls += Url.from_list(host, extract.srcs(content))

    return (remove_ignored(urls), len(content), status)

def remove_ignored(urls : list[Url]) -> list[Url]:
    for i in reversed(range(0, len(urls))):
        if str(urls[i]) in config['ignorelist']:
            del urls[i]
    return urls

def crawl(start: Url, url: Url = None, searched = []) -> tuple[list[str], int]:
    if url is None:
        url = start

    url_s = str(url)
    searched += [url_s]
    map_count = 1
    start_time = perf_counter()
    sub_urls = []

    # Search the site
    print(f'Scanning: ( ... ) {url_s}', end=' ', flush=True)
    curr_urls, content_length, status_code = parse_site(url_s)

    # Log results
    if curr_urls is None:
        print(f'\rScanning: ( {status_code} ) [ FAILED ] {url_s}', flush=True)
        return ([], 1)
    content_size = trimf(content_length / 1024)
    delta_time = trimf( perf_counter() - start_time )
    print(f'\rScanning: ( {status_code} ) [ {content_size}kb, {delta_time}s ] {url_s}', flush=True)

    # Search detected sites
    for u in curr_urls:
        # Not a page
        if u.type not in config['search']:
            continue
        # Already searched
        if str(u) in searched:
            continue
        # Different website
        if start.pr.netloc != u.pr.netloc:
            continue

        c_urls, maps = crawl(start, u, searched)
        sub_urls += c_urls
        map_count += maps

    return (curr_urls + sub_urls, map_count)

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('Usage: webmap [URL] [OUTPUT_FILE]')
    url = sys.argv[1]
    file = sys.argv[2]

    start_time = perf_counter()
    print('Url:', url)

    urls, map_count = crawl(Url(url))
    unique_urls = unique_list( [url] + [str(i) for i in urls] )

    delta_time = trimf( perf_counter() - start_time )
    print('========')
    print(f'Scanned completed in: {delta_time}s')
    print(f'Scanned sites: {map_count}')
    print(f'Mapped endpoints: {len(unique_urls)}')


    with open(file, 'w') as f:
        f.write( '\n'.join(unique_urls) )
