import re

def hrefs(html : str) -> list[str]:
    return re.findall(r'href="(.*?)"', html) or []

def srcs(html : str) -> list[str]:
    return re.findall(r'src="(.*?)"', html) or []

def raw_urls(html : str) -> list[str]:
    return re.findall(r'(https?://.*?)[^A-Za-z0-9-_./?#:@!$&%*+,;=~]', html) or []