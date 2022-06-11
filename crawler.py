import requests

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

def crawl(url : str):
    searched = [url]
    urls = []

if __name__ == '__main__':
    print( [str(i) for i in parse_site('http://netpeak.hu')] )
