import logging
import sys

import aiohttp

from abs import BaseDownloader

logger = logging.getLogger(__name__)


class Downloader(BaseDownloader):
    def __init__(self):
        self._session = None

    async def download_image(self, url):
        if not self._session:
            self._session = aiohttp.ClientSession()

        try:
            logger.debug(f"Downloading image from {url}")
            async with self._session.get(url) as response:
                if response.status != 200:
                    raise ValueError(f'Error status {response.status}')
                logger.debug(f"Downloaded image from {url} fine.")
                return await response.read()
        except:
            logger.error(f"Something wrong with downloading image from {url}")
            logger.debug(sys.exc_info()[0])
            raise
