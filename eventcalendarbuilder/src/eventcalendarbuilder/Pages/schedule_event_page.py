import toga
from toga.style import Pack
from eventcalendarbuilder.Pages.page import Page
from toga.style.pack import COLUMN, ROW
from eventcalendarbuilder.PythonFiles.NER.NERInterface import NERInterface
from eventcalendarbuilder.PythonFiles.Events.EventsManager import EventsManager

class ScheduleEventPage(Page):
    def __init__(self):
        self.page_box = toga.Box(style=Pack(direction=COLUMN, padding_top=10))
        self.title = toga.Label('Schedule Page')
        self.input = toga.MultilineTextInput()
        self.get_entities_btn = toga.Button('Click me', on_press=self.get_entities_from_input)
        self.result = toga.Label('Output:')

        self.page_box.add(self.title)
        self.page_box.add(self.input)
        self.page_box.add(self.get_entities_btn)
        self.page_box.add(self.result)

    def get_entities_from_input(self, widget):
        # Define the behavior when the button on Page 1 is pressed
        text = self.input.value
        if text == "" or text == " " or text == "\n":
            #print("No text found!")
            #popup_mgr.BasicPopup('No text found!\nPlease input text')
            return False
        
        text.strip("\n").strip()
        events = NERInterface.GetEntitiesFromText(text)
        p_events = EventsManager.ProcessEvents(events)
        added_events = EventsManager.AddEvents(events=p_events)
        self.result.text = f'Output: {added_events}'
        #pass

    