from urllib.parse import urlsplit, ParseResult

class Url:
    pr: ParseResult

    def __init__(self, host, url):
        self.pr = urlsplit(url)
        if self.pr.netloc == '':
            self.pr = self.pr._replace(netloc=host)

    def __str__(self) -> str:
        return self.pr.geturl()
