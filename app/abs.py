from abc import ABC, abstractmethod


class InvalidUrlException(BaseException):
    pass


class BaseUrlScraper:
    @abstractmethod
    async def get_url_images(self, url):
        pass


class BaseDownloader(ABC):
    @abstractmethod
    async def download_image(self, url):
        pass


class BaseUploader(ABC):
    @abstractmethod
    async def upload_image(self, initial_url, image_url, face_index, face_image):
        pass


class BaseFaceDetector(ABC):
    @abstractmethod
    async def detect_faces(self, image_bytes):
        pass
