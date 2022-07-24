from django.core.files.storage import default_storage


def verify_image_exists(file_path: str) -> bool:
    '''
    Verifica que un archivo exista en el storage

    Parameters
    ----------
    file_path : str
        Path del archivo

    Returns
    -------
    bool
        True si el archivo existe, False si no
    '''
    return default_storage.exists(file_path)
