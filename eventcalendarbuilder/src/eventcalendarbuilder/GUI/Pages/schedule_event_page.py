import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW, CENTER

from eventcalendarbuilder.GUI.Pages.page import Page
from eventcalendarbuilder.PythonFiles.NER.NERInterface import NERInterface
from eventcalendarbuilder.PythonFiles.Events.EventsManager import EventsManager
from eventcalendarbuilder.GUI.Cards.eventconfigurecard import EventConfigureCard

DEFAULT_RESULT_TEXT = 'Output: '

class ScheduleEventPage(Page):
    def __init__(self):
        super().__init__()
        self.title = toga.Label('Schedule Page', style=Pack(text_align=CENTER))
        self.input = toga.MultilineTextInput(style=Pack(padding_top=10, height=200))
        self.get_entities_btn = toga.Button('Click me', on_press=self.get_entities_from_input, style=Pack(padding_top=10))
        self.result_container = toga.ScrollContainer(horizontal=False, style=Pack(flex=1))
        self.result_content = toga.Box(style=Pack(direction=COLUMN, padding_top=10))
        self.result_container.content = self.result_content

        self.page_box.add(self.title)
        self.page_box.add(self.input)
        self.page_box.add(self.get_entities_btn)
        self.page_box.add(self.result_container)

    def get_entities_from_input(self, widget):
        # Clear local events list
        EventsManager.events = []
        for c in list(self.result_content.children):
            self.result_content.remove(c)

        text = self.input.value
        if text == "" or text == " " or text == "\n":
            # Popup used for now 
            toga.Window().error_dialog(title='Warning!', message='No text detected. Please input text!')
            return
        
        text.strip("\n").strip()
        events = NERInterface.GetEntitiesFromText(text)
        p_events = EventsManager.ProcessEvents(events)
        added_events = EventsManager.AddEvents(events=p_events)
        
        for e in added_events:
            card = EventConfigureCard(event=e['object'], remove_cb=self.remove_card)
            self.result_content.add(card.get_card())
            self.result_content.add(toga.Divider())

    def on_remove(self):
        super().on_remove()
        self.input.value = ''
    
    def remove_card(self, card=None):
        if card == None: return
        self.result_content.remove(card)