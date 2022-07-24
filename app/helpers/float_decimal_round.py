def float_decimal_round(value: float, decimal_places: int = 2) -> float:
    '''
    Redondea un valor float a una cantidad de decimales determinada

    Parameters
    ----------
    value : float
        valor a redondear
    decimal_places : int
        cantidad de decimales a redondear

    Returns
    -------
    float
        valor redondeado
    '''
    return "{:.{}f}".format(value, decimal_places)
