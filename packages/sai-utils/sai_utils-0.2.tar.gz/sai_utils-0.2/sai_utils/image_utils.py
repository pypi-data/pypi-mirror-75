import base64
import os
import re

from PIL import Image
from io import BytesIO

valid_image_extensions = ["jpg", "jpeg", "png"]

def datauri_to_io(data_uri):
    image_data = re.sub('^data:image/.+;base64,', '', data_uri)
    image_raw = BytesIO(base64.b64decode(image_data))
    return image_raw


def get_exif_orientation(file_path):

    orientation = None

    image = Image.open(file_path)

    exif_orientation_tag = 0x0112
    if hasattr(image, '_getexif'):
        exif = image._getexif()
        if (exif != None and exif_orientation_tag in exif):
            orientation = exif.get(exif_orientation_tag, 1)
    return orientation




