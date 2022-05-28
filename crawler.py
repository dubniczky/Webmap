import requests

import extract
from url import Url


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
    return urls

if __name__ == '__main__':
    print( [str(i) for i in parse_site('http://netpeak.hu')] )
