import io
import logging
from typing import Dict

from PIL import Image

from app.settings import settings

logger = logging.getLogger(__name__)


def resize_image(image_file: io.BytesIO) -> Dict[str, io.BytesIO]:
    # Convert file to PIL Image
    image = Image.open(image_file)
    image_file.seek(0)

    # Result stored in job
    result = {'original': image}

    # Convert to required sizes and store in result
    for size in settings.IMAGE_SIZES:
        image_thumbnail = image.copy()
        image_thumbnail.thumbnail((size, size))
        result[str(size)] = image_thumbnail

    # Convert images to file-like objects
    for key in result:
        bytes_file = io.BytesIO()
        result[key].save(bytes_file, format=image.format)
        bytes_file.seek(0)
        result[key] = bytes_file

    return result
