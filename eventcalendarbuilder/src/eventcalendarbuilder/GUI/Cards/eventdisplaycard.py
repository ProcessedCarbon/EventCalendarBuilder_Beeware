import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW, CENTER
from toga.constants import Direction

from eventcalendarbuilder.GUI.Cards.card import Card

class EventDisplayCard(Card):
    def __init__(self) -> None:
        super().__init__()
        # MAIN
        self.event_container, self.event_input, self.event_label = self.labeled_input(label='Event', input=toga.MultilineTextInput(placeholder='Name of event', style=Pack(flex=1), readonly=True))
        self.desc_container, self.desc_input, self.desc_label = self.labeled_input(label='Description', input=toga.MultilineTextInput(placeholder='Describe the event', style=Pack(flex=1), readonly=True))
        self.loc_container, self.loc_input, self.loc_label = self.labeled_input(label='Location', input=toga.MultilineTextInput(placeholder='Location at where event is held', style=Pack(flex=1), readonly=True))
        self.start_date_container, self.start_date_input, self.start_date_label = self.labeled_input(label='Start Date', input=toga.Label(text='', style=Pack(flex=1)))
        self.end_date_container, self.end_date_input, self.end_date_label = self.labeled_input(label='End Date', input=toga.Label(text='', style=Pack(flex=1)))
        self.start_time_container, self.start_time_input, self.start_time_label = self.labeled_input(label='Start Time', input=toga.Label(text='', style=Pack(flex=1)))
        self.end_time_container, self.end_time_input, self.end_time_label = self.labeled_input(label='End Time', input=toga.Label(text='', style=Pack(flex=1)))

        # MISC
        self.priority_container = toga.Box(children=[toga.Label('Priority:'), toga.Divider(direction=Direction.VERTICAL), toga.Label('')], style=Pack(padding=5, alignment=CENTER))
        self.calendar_container = toga.Box(children=[toga.Label('Calendar:'), toga.Divider(direction=Direction.VERTICAL), toga.Label('')], style=Pack(padding=5, alignment=CENTER))
        self.timezone_container = toga.Box(children=[toga.Label('Timezone:'), toga.Divider(direction=Direction.VERTICAL), toga.Label('')], style=Pack(padding=5, alignment=CENTER))
        self.repeated_container = toga.Box(children=[toga.Label('Repeated:'), toga.Divider(direction=Direction.VERTICAL), toga.Label('')], style=Pack(padding=5, alignment=CENTER))

        self.misc_label = toga.Label('Misc:')
        self.misc_container = toga.SplitContainer()
        self.left_split = toga.Box(children=[self.priority_container, self.calendar_container], style=Pack(direction=COLUMN, padding_top=10))
        self.right_split = toga.Box(children=[self.timezone_container, self.repeated_container], style=Pack(direction=COLUMN, padding_top=10))
        self.misc_container.content = [(self.left_split, 1), (self.right_split, 1)]

        # Add to card
        self.content.add(self.event_container)
        self.content.add(self.desc_container)
        self.content.add(self.loc_container)
        self.content.add(self.start_date_container)
        self.content.add(self.end_date_container)
        self.content.add(self.start_time_container)
        self.content.add(self.end_time_container)
        self.content.add(self.misc_label)
        self.content.add(self.misc_container)

    def labeled_input(self, label, input):
        # Container
        labeled_input_container = toga.SplitContainer()

        # UI
        label = toga.Label(f'{label}: ')
        
        #labeled_input_container = toga.Box(children=[label, toga.Divider(direction=Direction.VERTICAL), input], style=Pack(padding=10))
        labeled_input_container.content = [(label, 1), (input, 5)]
        return labeled_input_container, input, label