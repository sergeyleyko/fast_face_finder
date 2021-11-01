"""
Base classes for(Interfaces) used by the service
"""

from abc import ABC, abstractmethod

from numpy import ndarray


class InvalidUrlException(BaseException):
    pass


class BaseUrlScraper:
    @abstractmethod
    async def get_url_images(self, url: str):
        pass


class BaseDownloader(ABC):
    @abstractmethod
    async def download(self, url: str):
        pass


class BaseUploader(ABC):
    @abstractmethod
    async def upload_image(self, initial_url: str, image_url: str, face_index: int, face_image: ndarray):
        pass


class BaseFaceDetector(ABC):
    @abstractmethod
    async def detect_faces(self, image_bytes: bytes):
        pass
