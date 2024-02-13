import toga
from toga.style import Pack
from toga.style.pack import COLUMN
from eventcalendarbuilder.GUI.Pages.page import Page
from eventcalendarbuilder.PythonFiles.Events.EventsManager import EventsManager

class ManageEventPage(Page):
    def __init__(self):
        super().__init__()
        self.title = toga.Label('Manage Events')
        self.page_box.add(self.title)

        self.event_container = toga.ScrollContainer(horizontal=False, style=Pack(flex=1))
        self.event_content = toga.Box(style=Pack(direction=COLUMN, padding_top=10))
        self.event_container.content = self.event_content

        # Get events from events db
        events = EventsManager.events_db
        if len(events) > 0:
            for index, data in enumerate(EventsManager.events_db):
                pass