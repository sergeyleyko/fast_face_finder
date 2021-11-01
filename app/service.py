import asyncio
import logging
from typing import List, Tuple

from numpy import ndarray

from abs import BaseDownloader, BaseUrlScraper, BaseUploader, BaseFaceDetector

logger = logging.getLogger(__name__)


class FaceService:
    """
    The main service logic.
    Combines all pieces together.
    """

    def __init__(self,
                 url_parser: BaseUrlScraper,
                 downloader: BaseDownloader,
                 uploader: BaseUploader,
                 face_detector: BaseFaceDetector):
        self._url_parser = url_parser
        self._downloader = downloader
        self._uploader = uploader
        self._face_detector = face_detector
        logger.info("Started face service.")

    async def _process_image_url(self, image_url: str) -> List[ndarray]:
        """
        Process a single image: download and extract faces
        :param image_url: image url
        :return: list of face images
        """
        image_bytes = await self._downloader.download(image_url)
        faces = await self._face_detector.detect_faces(image_bytes)
        return faces

    async def _process_image_urls(self, image_urls: List[str]) -> List[Tuple[str, List[ndarray]]]:
        """
        Wait for all images to be processed and return all faces found
        :param image_urls: list of images urls
        :return: image url to faces tuples
        """
        per_image_faces = await asyncio.gather(*[self._process_image_url(url) for url in image_urls],
                                               return_exceptions=True)

        # get rid of exceptions and make url->faces tuples
        url_and_faces = [(url, faces) if isinstance(faces, list) else (url, [])
                         for url, faces in zip(image_urls, per_image_faces)]
        return url_and_faces

    async def _upload_faces(self, initial_url: str, image_url_and_faces: List[Tuple[str, List[ndarray]]]):
        tasks = []
        for image_url, image_faces in image_url_and_faces:
            for face_index, face_image in enumerate(image_faces):
                tasks.append(self._uploader.upload_image(initial_url, image_url, face_index, face_image))

        uploaded_flags = await asyncio.gather(*tasks, return_exceptions=True)
        faces_processed = sum(1 if isinstance(flag, bool) else 0 for flag in uploaded_flags)
        return faces_processed

    async def get_faces(self, url: str):
        """
        - Downloads images attached url
        - Finds all faces on the each image
        - Saves aligned faces by using 'uploader'
        - Returns count of faces
        :param url:
        :return:
        """
        image_urls = await self._url_parser.get_url_images(url)
        url_and_faces = await self._process_image_urls(image_urls)
        faces_processed = await self._upload_faces(url, url_and_faces)
        return faces_processed
