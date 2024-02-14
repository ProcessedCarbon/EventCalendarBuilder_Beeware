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

        self.page_box.add(self.title)
        self.page_box.add(toga.Divider(style=Pack(padding_top=10, padding_bottom=10)))
        self.page_box.add(self.event_container)
    
    def on_enter(self):
        super().on_enter()
        EventsManager.UpdateEventsDB()

        # Get events from events db
        events = EventsManager.events_db
        print(events)
        if len(events) > 0:
            for data in EventsManager.events_db:
                card = EventDisplayCard(event=data, remove_cb=self.remove_card) # json read as a string for each value
                self.event_content.add(card.get_card())
                self.event_content.add(toga.Divider())
    
    def remove_card(self, card=None):
        if card == None: return
        self.event_content.remove(card)        