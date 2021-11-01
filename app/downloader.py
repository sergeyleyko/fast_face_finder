import logging
import sys

import aiohttp

from abs import BaseDownloader

logger = logging.getLogger(__name__)


class Downloader(BaseDownloader):
    """
    Downloads data from url
    """
    def __init__(self):
        self._session = None

    async def download(self, url: str):
        if not self._session:
            self._session = aiohttp.ClientSession()

        try:
            logger.debug(f"Getting content from {url}")
            async with self._session.get(url) as response:
                if response.status != 200:
                    raise ValueError(f'Error status {response.status}')
                logger.debug(f"Successfully received content from {url}.")
                return await response.read()
        except:
            # For debugging..
            logger.error(f"Something wrong with getting data from {url}")
            logger.debug(sys.exc_info()[0])
            raise
