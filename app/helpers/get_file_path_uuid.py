import uuid
import os


def get_file_path_uuid(instance, filename):
    folder = instance.__name__.lower()
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join(f'{folder}/', filename)
