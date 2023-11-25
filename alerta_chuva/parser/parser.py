from datetime import date, datetime

import cv2
import numpy as np
from dateutil import parser  # type: ignore


def str_to_datetime_or_date(data: str, hora: str | None = None) -> datetime | date:
    """
    Transforma uma string em um objeto datetime ou date.
    Se não houver hora, assume-se que a string contém apenas a data.
    >>> str_to_datetime_or_date("01/01/2022")
    datetime.datetime(2022, 1, 1, 0, 0)

    Se houver hora, assume-se que a string contém a data e a hora.
    >>> str_to_datetime_or_date("01/01/2022 12:00:00")
    datetime.datetime(2022, 1, 1, 12, 0)

    Se não houver hora retorna um objeto date.

    Args:
        data (str): Data que sera transformada em objeto datetime ou date.
        hora (str, optional): Hora que sera transformada em objeto datetime. Defaults to None.

    Returns:
        datetime | date: Objeto datetime ou date.
    """
    if hora:
        return parser.parse(data + " " + hora, dayfirst=True)
    else:
        return parser.parse(data, dayfirst=True).date()


def img_bytes_to_ndarray(img_bytes: bytes) -> np.ndarray:
    """
    Transforma uma bytes em um ndarray.
    Para serem usados no opencv, deve-se transformar o ndarray em bytes

    Args:
        img_bytes (bytes): Bytes de uma imagem

    Returns:
        np.ndarray: Numpy array da imagem
    """
    nparr = np.frombuffer(img_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    return img
