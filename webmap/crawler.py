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
            return req.content.decode('utf-8')
        else:
            return None
    except Exception:
        return None

def parse_site(url : str) -> list[Url]:
    u = Url(url)
    host = u.host()
    page = get(url)

    if page is None:
        return []

    urls = []
    urls += Url.from_list(host, extract.raw_urls(page))
    urls += Url.from_list(host, extract.hrefs(page))
    urls += Url.from_list(host, extract.srcs(page))

    return remove_ignored(urls)

def remove_ignored(urls : list[Url]) -> list[Url]:
    for i in reversed(range(0, len(urls))):
        if str(urls[i]) in config['ignorelist']:
            del urls[i]
    return urls

def crawl(start: Url, url: Url = None, searched = []) -> tuple[list[str], int]:
    if url is None:
        url = start
    url_s = str(url)
    print('Mapping:', url_s)
    searched += [url_s]
    map_count = 1
    current = parse_site(url_s)
    for u in current:
        # Not a page
        if u.type not in ['page', 'unknown']:
            continue
        # Already searched
        if str(u) in searched:
            continue
        # Different website
        if start.pr.netloc != u.pr.netloc:
            continue

        urls, maps = crawl(start, u, searched)
        current += urls
        map_count += maps
    return (current, map_count)

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
