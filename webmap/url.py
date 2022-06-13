from urllib.parse import urlsplit, ParseResult

from config import config

def get_extensions(name):
    return tuple(config['extensions'][name])

class Url:
    pr: ParseResult
    type: str

    def __init__(self, url, host = '', scheme = 'http'):
        self.pr = urlsplit(url)
        if self.pr.netloc == '':
            self.pr = self.pr._replace(netloc=host)
        if self.pr.scheme == '':
            self.pr = self.pr._replace(scheme=scheme)

        self.type = self.get_content_type()

    def __str__(self) -> str:
        url = self.pr.geturl()
        # clean
        url = url.replace('/./', '/')

        frag_index = url.find('#')
        if frag_index != -1:
            url = url[0:frag_index]

        return url

    def host(self) -> str:
        return self.pr.netloc

    def get_content_type(self):
        path: str = self.pr.path.lower()
        if path.endswith(get_extensions('page')):
            return 'page'
        elif path.endswith(get_extensions('script')):
            return 'script'
        elif path.endswith(get_extensions('style')):
            return 'style'
        elif path.endswith(get_extensions('media')):
            return 'media'
        elif path.endswith(get_extensions('document')):
            return 'document'
        elif path.endswith(get_extensions('special')):
            return 'special'
        elif '.' not in path.split('/')[-1]:
            # Last segment contains no dot -> probably a page
            return 'page'
        else:
            return 'unknown'

    @staticmethod
    def from_list(host, urls):
        url = []
        for u in urls:
            url.append(Url(u, host))
        return url
