import toga
from toga.style import Pack
from toga.style.pack import COLUMN, CENTER

from eventcalendarbuilder.GUI.Pages.page import Page
from eventcalendarbuilder.GUI.Cards.eventdisplaycard import EventDisplayCard

from eventcalendarbuilder.PythonFiles.Events.EventsManager import EventsManager

class ManageEventPage(Page):
    def __init__(self):
        super().__init__()
        self.title = toga.Label('Manage Events', style=Pack(text_align=CENTER))

        self.event_container = toga.ScrollContainer(horizontal=False, style=Pack(flex=1))
        self.event_content = toga.Box(style=Pack(direction=COLUMN, padding=10))
        self.event_container.content = self.event_content

        self.content.add(self.title)
        self.content.add(toga.Divider(style=Pack(padding_top=10, padding_bottom=10)))
        self.content.add(self.event_container)
    
    def on_enter(self):
        super().on_enter()
        EventsManager.UpdateEventsDB()

        # Get events from events db
        events = EventsManager.events_db
        if len(events) > 0:
            for data in EventsManager.events_db:
                card = EventDisplayCard(event=data, parent=self.event_content) # json read as a string for each value
                self.event_content.add(card.get_card())
                self.event_content.add(toga.Divider())
    
    def on_exit(self):
        super().on_exit()
        for c in list(self.event_content.children):
            self.event_content.remove(c)