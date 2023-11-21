from datetime import date, datetime
from dateutil import parser


def to_datetime_or_date(data: str, hora: str = None) -> datetime | date:
    if hora:
        date = parser.parse(data + " " + hora, dayfirst=True)
    else:
        date = parser.parse(data, dayfirst=True).date()
    return date
