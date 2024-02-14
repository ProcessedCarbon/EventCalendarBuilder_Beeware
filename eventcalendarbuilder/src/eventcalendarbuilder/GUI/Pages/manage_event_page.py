import toga
from toga.style import Pack
from toga.style.pack import COLUMN, CENTER

from eventcalendarbuilder.GUI.Pages.page import Page
from eventcalendarbuilder.GUI.Cards.eventdisplaycard import EventDisplayCard

from eventcalendarbuilder.PythonFiles.Events.EventsManager import EventsManager

class ManageEventPage(Page):
    def __init__(self):
        super().__init__()
        self.title = toga.Label('Manage Events', style=Pack(alignment=CENTER))
        self.page_box.add(self.title)

        self.event_container = toga.ScrollContainer(horizontal=False, style=Pack(flex=1))
        self.event_content = toga.Box(style=Pack(direction=COLUMN, padding_top=10))
        self.event_container.content = self.event_content

        self.page_box.add(self.event_container)
    
    def on_enter(self):
        super().on_enter()
        EventsManager.UpdateEventsDB()

        # Get events from events db
        events = EventsManager.events_db
        print(events)
        if len(events) > 0:
            for index, data in enumerate(EventsManager.events_db):
                card = EventDisplayCard(event=data) # json read as a string for each value
                self.event_content.add(card.get_card())
                self.event_content.add(toga.Divider())
                pass