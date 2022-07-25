from datetime import datetime


def validate_datetime(string: str) -> bool or datetime:
    '''
    Valida que un string sea una fecha y hora válida en formato '%Y-%m-%d %H:%M'

    Parameters
    ----------
    string : str
        Fecha a validar

    Returns
    -------
    bool
        False si no es una fecha válida
        datetime si es una fecha válida
    '''
    try:
        return datetime.strptime(string, '%Y-%m-%d %H:%M')
    except ValueError:
        return False
