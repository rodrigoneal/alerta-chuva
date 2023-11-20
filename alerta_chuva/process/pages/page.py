from selenium_tools.page_objects import Page

from alerta_chuva.process.pages.elements import DowloandHistory


class GetHistory(Page):
    download_history = DowloandHistory()
