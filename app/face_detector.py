import logging

import cv2
import mediapipe as mp
import numpy as np
from mediapipe.framework.formats import detection_pb2, location_data_pb2
from mediapipe.python.solutions.drawing_utils import _normalized_to_pixel_coordinates

logger = logging.getLogger(__name__)

class FaceDetector:
    def __init__(self):
        self._mp_face_detection = mp.solutions.face_detection
        self._mp_drawing = mp.solutions.drawing_utils

    def get_detection_abs_rect(self, image: np.ndarray, detection: detection_pb2.Detection):
        """Get the detection bounding box in absolute images coordinates.

        Args:
          image: A three channel RGB image represented as numpy ndarray.
          detection: A detection proto message.
        """
        image_rows, image_cols, _ = image.shape

        location = detection.location_data
        relative_bounding_box = location.relative_bounding_box
        rect_start_point = _normalized_to_pixel_coordinates(
            relative_bounding_box.xmin, relative_bounding_box.ymin, image_cols,
            image_rows)
        rect_end_point = _normalized_to_pixel_coordinates(
            relative_bounding_box.xmin + relative_bounding_box.width,
            relative_bounding_box.ymin + relative_bounding_box.height, image_cols,
            image_rows)
        return rect_start_point, rect_end_point

    async def detect_faces(self, image_bytes):
        # For static images:
        with self._mp_face_detection.FaceDetection(
                model_selection=1, min_detection_confidence=0.5) as face_detection:
            np_arr = np.asarray(bytearray(image_bytes), dtype="uint8")
            cv_image = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

            # Convert the BGR image to RGB and process it with MediaPipe Face Detection.
            results = face_detection.process(cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB))

            detections = results.detections or []
            faces = []
            for index, detection in enumerate(detections):
                # Draw face detection.
                self._mp_drawing.draw_detection(cv_image, detection)

                # Extract face
                left_top, right_bottom = self.get_detection_abs_rect(cv_image, detection)
                face_image = cv_image[left_top[1]:right_bottom[1], left_top[0]:right_bottom[0]]
                faces.append(face_image)

            logger.debug(f"Detected {len(faces)} faces.")
            return faces
