import uuid
import os


def get_file_path_uuid(instance, filename):
    '''
    Genera un path para un archivo

    Parameters
    ----------
    instance : object
        Instancia del modelo
    filename : str
        Nombre del archivo

    Returns
    -------
    str
        Path del archivo
    '''
    folder = instance.__name__.lower()
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join(f'{folder}/', filename)
