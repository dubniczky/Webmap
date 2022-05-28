from urllib.parse import urlsplit, ParseResult

class Url:
    pr: ParseResult
    type: str

    def __init__(self, host, url):
        self.pr = urlsplit(url)
        if self.pr.netloc == '':
            self.pr = self.pr._replace(netloc=host)

        path = self.pr.path.lower()
        if path.endswith('.html'):
            self.type = 'page'
        elif path.endswith(('.js', '.mjs')):
            self.type = 'script'
        elif path.endswith('.css'):
            self.type = 'style'
        elif path.endswith(('.png', '.jpg', '.svg')):
            self.type = 'style'

    def __str__(self) -> str:
        return self.pr.geturl()
