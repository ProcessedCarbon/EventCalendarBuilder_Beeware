import toga
from toga.style import Pack
from eventcalendarbuilder.GUI.Pages.page import Page

class ManageEventPage(Page):
    def __init__(self):
        super().__init__()
        self.title = toga.Label('Manage Events')
        self.page_box.add(self.title)
