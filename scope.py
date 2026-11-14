from urllib.parse import urlsplit


def origin(url):
    parts = urlsplit(url)
    if parts.scheme not in {'http', 'https'} or parts.username or parts.password:
        raise ValueError('非网页来源')
    return parts.scheme + '://' + parts.netloc


def permits(url, origins):
    try:
        return origin(url) in origins
    except ValueError:
        return False
