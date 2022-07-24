from django.core.files.storage import default_storage


def verify_image_exists(file):
    return default_storage.exists(file)
