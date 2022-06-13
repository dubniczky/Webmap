import requests
import sys

import extract
from url import Url

from config import config

def get(url : str) -> str:
    req = requests.get(url, allow_redirects=True)
    if req:
        return str(req.content)
    else:
        return None

def parse_site(url : str) -> list[Url]:
    u = Url(url)
    host = u.host()
    page = get(url)

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

def crawl(url : str, searched = []) -> list[Url]:
    searched += [url]
    current = parse_site(url)
    print('Mapping:', url)
    targets = []
    for u in current:
        if u.type in ['page', 'unknown']:
            targets.append(u)
            current += crawl(str(u), searched)
    return current


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: webmap [URL]')
    url = sys.argv[1]

    print('Url:', url)

    urls = [url] + [str(i) for i in crawl(url)]
    print( urls )
