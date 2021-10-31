import logging
import sys
from urllib.parse import urljoin, urlparse

import aiohttp
from aiohttp import InvalidURL
from bs4 import BeautifulSoup as bs

logger = logging.getLogger(__name__)


class UrlParser:
    def __init__(self):
        self._session = aiohttp.ClientSession()

    def is_valid(self, url):
        """
        Checks whether `url` is a valid URL.
        """
        parsed = urlparse(url)
        return bool(parsed.netloc) and bool(parsed.scheme)

    def clean_url(self, url):
        try:
            pos = url.index("?")
            url = url[:pos]
        except ValueError:
            pass
        return url

    def find_urls(self, url, body):
        urls = set()
        soup = bs(body, "html.parser")

        for img in soup.find_all("img"):
            img_url = img.attrs.get("src")
            if not img_url:
                # if img does not contain src attribute, just skip
                continue

            img_url = urljoin(url, img_url)
            img_url = self.clean_url(img_url)
            if self.is_valid(img_url):
                urls.add(img_url)
        return list(urls)

    async def get_url_images(self, url):
        if not url.startswith("http"):
            url = f"https://{url}"
        try:
            async with self._session.get(url) as response:
                if response.status == 200:
                    if response.content_type.startswith('image'):
                        return [url]
                    else:
                        html = await response.text()
                        image_urls = self.find_urls(url, html)
                        return image_urls
                else:
                    raise ValueError(f'Error status {response.status} while downloading an image')
        except (ValueError, InvalidURL) as err:
            logger.error(err)
        except:
            # I know, I know..
            logger.error(f"Something wrong with getting data from {url}")
            logger.debug(sys.exc_info()[0])
            raise
        return []
