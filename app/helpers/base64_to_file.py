
import base64
from django.core.files.base import ContentFile


def base64_to_file(image: str) -> ContentFile:
    '''
    Convierte una imagen en base64 a un archivo

    Parameters
    ----------
    image : str
        Imagen en base64

    Returns
    -------
    django.core.files.base.ContentFile
        Archivo de imagen
    '''
    format, img_str = image.split(';base64,')
    ext = format.split('/')[-1]
    return ContentFile(base64.b64decode(img_str), name='temp.' + ext)
