from app.helpers.base64_to_file import base64_to_file
from django.core.files.storage import default_storage
from app.helpers.get_file_path_uuid import get_file_path_uuid


def save_image(image, instance):
    image = base64_to_file(image)
    file_name = get_file_path_uuid(instance, image.name)
    return default_storage.save(file_name, image)
