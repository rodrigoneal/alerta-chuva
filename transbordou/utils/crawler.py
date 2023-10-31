from transbordou.locais import Local
from transbordou.process.pages.page import GetHistory


def download_rainfall_history_one_station(driver, estacao: str, year: int) -> None:
    station = Local[estacao.upper()].value
    get_history = GetHistory(driver)
    get_history.download_history.download_specific_station(year, station)


def download_rainfall_history_all_stations(driver, year: int) -> None:
    get_history = GetHistory(driver)
    get_history.download_history.download_history_all_stations(year)
