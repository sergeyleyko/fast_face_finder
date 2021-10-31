import logging
import os

import uvicorn
from fastapi import FastAPI
import anyconfig

from dlib_face_detector import DlibFaceDetector
from downloader import Downloader
from face_detector import FaceDetector
from uploader import Uploader
from url_parser import UrlParser

logging.basicConfig(level=logging.DEBUG)

from service import FaceService


def create_service():
    config = anyconfig.load("config.yml", ac_parser="yaml")

    url_parser = UrlParser()
    downloader = Downloader()
    uploader = Uploader(config["uploader"]["dir"])

    # face_detector = FaceDetector()
    face_detector = DlibFaceDetector(os.path.join("models",
                                                  config["face_detector"]["model"]),
                                     config["face_detector"]["final_size"])

    service = FaceService(url_parser, downloader, uploader, face_detector)
    return service


def get_app():
    fastapi_app = FastAPI()
    return fastapi_app


service = create_service()
app = get_app()


@app.get("/faces")
async def get_faces(url):
    return await service.get_faces(url)


if __name__ == "__main__":
    fastapi_app = get_app()
    uvicorn.run(fastapi_app, host="0.0.0.0", port=8000)
