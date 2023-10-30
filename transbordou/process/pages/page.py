from selenium_tools.page_objects import Page

from transbordou.process.pages.elements import DowloandHistory


class GetHistory(Page):
    download_history = DowloandHistory()
