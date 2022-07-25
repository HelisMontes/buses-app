import re


def validate_base64_image(string: str) -> bool:
    '''
    Valida que un string sea una imagen en base64

    Parameters
    ----------
    string : str
        String a validar

    Returns
    -------
    bool
        True si es una imagen en base64, False si no
    '''
    return re.match(r'data:image\/([a-zA-Z]*);base64,([^\"]*)', string)
