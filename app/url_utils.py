from urllib.parse import urlparse


def is_valid_url(url):
    """
    Checks whether `url` is a valid URL.
    """
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)


def clean_url(url):
    try:
        pos = url.index("?")
        url = url[:pos]
    except ValueError:
        pass
    return url


def fix_url_scheme(url, scheme='http'):
    parsed_url = urlparse(url)
    if not bool(parsed_url.scheme):
        parsed_url = parsed_url._replace(**{"scheme": scheme})
    if not bool(parsed_url.netloc):
        parsed_url = parsed_url._replace(**{"netloc": parsed_url.path, "path": ''})
    fixed_url = parsed_url.geturl()
    return fixed_url
