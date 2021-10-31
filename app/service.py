import asyncio
import logging

logger = logging.getLogger(__name__)


class FaceService:
    def __init__(self, url_parser, downloader, uploader, face_detector):
        self._url_parser = url_parser
        self._downloader = downloader
        self._uploader = uploader
        self._face_detector = face_detector
        logger.info("Started face service.")

    async def process_image_url(self, image_url):
        image_bytes = await self._downloader.download_image(image_url)
        faces = await self._face_detector.detect_faces(image_bytes)
        return faces

    async def process_image_urls(self, image_urls):
        """
        Wait for all images to be processed and return all faces found
        :param image_urls: images urls
        :return: faces
        """
        per_image_faces = await asyncio.gather(*[self.process_image_url(url) for url in image_urls],
                                               return_exceptions=True)

        # get rid of exceptions and make url->faces tuples
        url_and_faces = [(url, faces) if isinstance(faces, list) else (url, [])
                         for url, faces in zip(image_urls, per_image_faces)]
        return url_and_faces

    async def upload_faces(self, initial_url, image_url_and_faces):
        tasks = []
        for image_url, image_faces in image_url_and_faces:
            for face_index, face_image in enumerate(image_faces):
                tasks.append(self._uploader.upload_image(initial_url, image_url, face_index, face_image))

        uploaded_flags = await asyncio.gather(*tasks, return_exceptions=True)
        faces_processed = sum(1 if isinstance(flag, bool) else 0 for flag in uploaded_flags)
        return faces_processed

    async def get_faces(self, url):
        image_urls = await self._url_parser.get_url_images(url)
        url_and_faces = await self.process_image_urls(image_urls)
        faces_processed = await self.upload_faces(url, url_and_faces)
        return faces_processed
