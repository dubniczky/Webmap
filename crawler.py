import requests

def get(url : str) -> str:
    req = requests.get(url, allow_redirects=True)
    if req:
        return str(req.content)
    else:
        return None
