from datetime import date, datetime

import cv2
import numpy as np
from dateutil import parser


def str_to_datetime_or_date(data: str, hora: str = None) -> datetime | date:
    if hora:
        date = parser.parse(data + " " + hora, dayfirst=True)
    else:
        date = parser.parse(data, dayfirst=True).date()
    return date

def img_bytes_to_ndarray(img_bytes: bytes) -> np.ndarray:
    nparr = np.frombuffer(img_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    return img