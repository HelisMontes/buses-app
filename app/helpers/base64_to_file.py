
import base64
from django.core.files.base import ContentFile


def base64_to_file(image):
    format, imgstr = image.split(';base64,')
    ext = format.split('/')[-1]
    return ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
