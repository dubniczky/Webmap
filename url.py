from urllib.parse import urlsplit, ParseResult

from config import config

def get_extensions(name):
    return tuple(config.extensions[name])

class Url:
    pr: ParseResult
    type: str

    def __init__(self, url, host = '', scheme = 'http'):
        self.pr = urlsplit(url)
        if self.pr.netloc == '':
            self.pr = self.pr._replace(netloc=host)
        if self.pr.scheme == '':
            self.pr = self.pr._replace(scheme=scheme)

        path = self.pr.path.lower()
        if path.endswith(get_extensions('page')):
            self.type = 'page'
        elif path.endswith(get_extensions('script')):
            self.type = 'script'
        elif path.endswith(get_extensions('style')):
            self.type = 'style'
        elif path.endswith(get_extensions('media')):
            self.type = 'media'

    def __str__(self) -> str:
        url = self.pr.geturl()
        # clean
        url = url.replace('/./', '/')
        return url

    def host(self) -> str:
        return self.pr.netloc

    @staticmethod
    def from_list(host, urls):
        url = []
        for u in urls:
            url.append(Url(u, host))
        return url
