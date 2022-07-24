from app.helpers.base64_to_file import base64_to_file
from django.core.files.storage import default_storage
from app.helpers.get_file_path_uuid import get_file_path_uuid


def save_image(image: str, instance: object) -> str:
    '''
    Guarda una imagen en el storage

    Parameters
    ----------
    image : str
        Imagen en base64
    instance : object
        Instancia del modelo

    Returns
    -------
    str
        Path del archivo
    '''
    image = base64_to_file(image)
    file_name = get_file_path_uuid(instance, image.name)
    return default_storage.save(file_name, image)
