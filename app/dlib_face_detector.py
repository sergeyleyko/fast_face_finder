import logging

import cv2
import dlib
import numpy as np

from abs import BaseFaceDetector

logger = logging.getLogger(__name__)


class DlibFaceDetector(BaseFaceDetector):
    def __init__(self, predictor_model_file, final_image_size=320):
        self._detector = dlib.get_frontal_face_detector()
        self._shape_predictor = dlib.shape_predictor(predictor_model_file)
        self._final_image_size = final_image_size

    async def detect_faces(self, image_bytes):
        np_arr = np.asarray(bytearray(image_bytes), dtype="uint8")
        cv_image = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

        # Ask the detector to find the bounding boxes of each face. The 1 in the
        # second argument indicates that we should upsample the image 1 time. This
        # will make everything bigger and allow us to detect more faces.
        detections = self._detector(cv_image, 1)

        # Find the 5 face landmarks we need to do the alignment.
        face_landmarks = dlib.full_object_detections()
        for index, detection in enumerate(detections):
            face_landmarks.append(self._shape_predictor(cv_image, detection))

        # Extract face
        faces = dlib.get_face_chips(cv_image, face_landmarks, size=self._final_image_size)
        logger.debug(f"Detected {len(faces)} faces.")
        return faces
