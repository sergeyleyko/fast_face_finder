import logging
import os

import anyconfig
import uvicorn
from fastapi import FastAPI, HTTPException

from abs import InvalidUrlException
from dlib_face_detector import DlibFaceDetector
from downloader import Downloader
from service import FaceService
from uploader import Uploader
from url_scraper import UrlScraper
from url_utils import fix_url_scheme, is_valid_url

logging.basicConfig(level=logging.INFO)


def create_service():
    """
    The main objects fabric of the app. Instantiates concrete implementations,
    passing parameter from the configuration.yml file.
    :return: face server object
    """
    config = anyconfig.load("config.yml", ac_parser="yaml")

    url_parser = UrlScraper()
    downloader = Downloader()
    uploader = Uploader(config["uploader"]["dir"])

    # face_detector = FaceDetector()
    face_detector = DlibFaceDetector(os.path.join("models",
                                                  config["face_detector"]["model"]),
                                     config["face_detector"]["final_size"])

    face_service = FaceService(url_parser, downloader, uploader, face_detector)
    return face_service


def get_app():
    """
    Creates FastAPI application object
    :return:
    """
    fastapi_app = FastAPI()
    return fastapi_app


service = create_service()
app = get_app()


@app.get("/faces")
async def get_faces(url: str):
    """
    find faces endpoint
    :param url: url to find faces on images at
    :return: faces count
    """
    fixed_url = fix_url_scheme(url)
    if not is_valid_url(fixed_url):
        raise HTTPException(status_code=400, detail="Invalid url passed. Check if there is a typo in {url}.")

    try:
        faces_count = await service.get_faces(fixed_url)
    except InvalidUrlException:
        raise HTTPException(status_code=400, detail=f"This URL can’t be reached. Check if there is a typo in {url}.")

    return faces_count


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
