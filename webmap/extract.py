import re

## General Extractors

def raw_urls(html : str) -> list[str]:
    return re.findall(r'(https?://.*?)[^A-Za-z0-9-_./?#:@!$&%*+,;=~]', html) or []

## HTML Extractors

def html_hrefs(html : str) -> list[str]:
    return re.findall(r'href="(.*?)"', html) or []

def html_srcs(html : str) -> list[str]:
    return re.findall(r'src="(.*?)"', html) or []

## CSS Extractors

def css_import(css : str) -> list[str]:
    return re.findall(r'@import\\s[\'"]?(.*?)[\'"]?;', css) or []

def css_urls(css : str) -> list[str]:
    return re.findall(r'url\([\'"]?(.*?)[\'"]?\)', css) or []
