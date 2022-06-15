from time import perf_counter
import requests
import sys

import extract
from url import Url

from config import config

def get(url : str) -> str | None:
    try:
        req = requests.get(url, allow_redirects=True)
        if req:
            return (req.content.decode('utf-8'), req.status_code)
        else:
            return None
    except Exception:
        return None

def parse_site(url : str) -> tuple[list[Url], int, int] | None:
    u = Url(url)
    host = u.host()
    page = get(url)

    if page is None:
        return None

    content, status = page

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
    print(f'Mapping: ( ... ) {url_s}', end=' ', flush=True)
    searched += [url_s]
    map_count = 1
    start_time = perf_counter()
    current = parse_site(url_s)
    delta_time = trimf( perf_counter() - start_time )
    if current is None:
        return ([], 1)

    curr_urls, content_length, status_code = current
    sub_urls = []

    print('\r', end='')
    content_size = trimf(content_length / 1024)
    print(f'Mapping: ( {status_code} ) [ {content_size}kb, {delta_time}s ] {url_s}', flush=True)

    for u in curr_urls:
        # Not a page
        if u.type not in ['page', 'unknown']:
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

def unique_list(l):
    return list(set(l))

def trimf(f: float) -> str:
    return str( round(f, 2) )

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
    print(f'Mapping completed in: {delta_time}s')
    print(f'Mapped sites: {map_count}')
    print(f'Detected endpoints: {len(unique_urls)}')


    with open(file, 'w') as f:
        f.write( '\n'.join(unique_urls) )
