import logging
import sys
from urllib.parse import urljoin

import aiohttp
from aiohttp import InvalidURL, ClientConnectorError
from bs4 import BeautifulSoup as bs

from abs import BaseUrlScraper, InvalidUrlException
from url_utils import clean_url, is_valid_url

logger = logging.getLogger(__name__)


class UrlScraper(BaseUrlScraper):
    """

    """

    def __init__(self):
        self._session = None

    def find_img_urls(self, url: str, body: str):
        """
        Find all urls in the body of the URL
        :param url: url body from
        :param body: the body string
        :return: list of images urls
        """
        urls = set()
        soup = bs(body, "html.parser")

        for img in soup.find_all("img"):
            img_url = img.attrs.get("src")
            if not img_url:
                # if img does not contain src attribute, just skip
                continue

            img_url = urljoin(url, img_url)
            img_url = clean_url(img_url)
            if is_valid_url(img_url):
                urls.add(img_url)
        return list(urls)

    async def get_url_images(self, url):
        """
        Download page at url and find all the images links there
        :param url: url
        :return: list of images urls
        """
        if not self._session:
            self._session = aiohttp.ClientSession()

        try:
            async with self._session.get(url) as response:
                if response.status == 200:
                    if response.content_type.startswith('image'):
                        return [url]
                    else:
                        html = await response.text()
                        image_urls = self.find_img_urls(url, html)
                        return image_urls
                else:
                    raise ValueError(f'Error status {response.status} while downloading an image')
        except (ValueError, InvalidURL, RuntimeError, ClientConnectorError) as err:
            logger.error(f"Error when with getting data from {url}")
            logger.error(err)
            raise InvalidUrlException() from err
        except:
            # Used for debugging
            logger.error(f"Something wrong with getting data from {url}")
            logger.debug(sys.exc_info()[0])
            raise
        return []
