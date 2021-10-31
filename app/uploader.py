import logging
import os
import re

import cv2
import unicodedata

logger = logging.getLogger(__name__)


class Uploader:
    def __init__(self, target_dir):
        self._target_dir = target_dir
        pass

    def slugify(self, value):
        """
        Convert spaces or repeated dashes to single dashes.
        Remove characters that aren't alphanumerics, underscores, or hyphens.
        Convert to lowercase.
        Also strip leading and trailing whitespace, dashes, and underscores.
        """
        value = str(value)
        value = unicodedata.normalize('NFKC', value)
        value = re.sub(r'[^\w\s-]', '', value.lower())
        return re.sub(r'[-\s]+', '-', value).strip('-_')

    async def upload_image(self, initial_url, image_url, face_index, face_image):
        safe_src_url = self.slugify(initial_url)
        url_dir = os.path.join(self._target_dir, safe_src_url)
        if not os.path.exists(url_dir):
            os.makedirs(url_dir)

        safe_image_url = self.slugify(image_url)
        face_filename = f'{safe_image_url}_face_{face_index}.png'
        image_path = os.path.join(url_dir, face_filename)
        cv2.imwrite(image_path, face_image)
        logger.debug(f"Saved face image {face_filename} for image {image_url}")
        return True
