from alerta_chuva.enums.locais import LocalChuva

def local_str_to_int(station: str | int) -> int:
    """
    Converte o nome do local para o id da estação.

    Args:
        station (str): Estação. Ex: 'Vidigal'

    Returns:
        int: Id da estação.
    """
    if isinstance(station, int):
        return station
    _local = station.upper()
    return LocalChuva[_local].value
