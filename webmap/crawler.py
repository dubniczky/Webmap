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
    except:
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

def crawl(start: Url, url: Url = None, searched = []) -> list[Url]:
    if url is None:
        url = start
    url_s = str(url)
    print('Mapping:', url_s)
    searched += [url_s]
    current = parse_site(url_s)
    for u in current:
        # Not a page
        if u.type not in ['page', 'unknown']:
            continue
        # Already searched
        if str(u) in searched:
            continue
        # Different website
        if start.pr.netloc != url.pr.netloc:
            continue

        current += crawl(start, u, searched)
    return current


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: webmap [URL]')
    url = sys.argv[1]

    print('Url:', url)

    urls = [url] + [str(i) for i in crawl(Url(url))]
    print( urls )
