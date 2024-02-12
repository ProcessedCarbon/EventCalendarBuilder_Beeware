import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW

from eventcalendarbuilder.GUI.Cards.card import Card

class EventConfigureCard(Card):
    def __init__(self) -> None:
        super().__init__()
        # MAIN
        self.event_input = self.labeled_input(label='Event', input=toga.TextInput(placeholder='Name of event'))
        self.desc_input = self.labeled_input(label='Description', input=toga.TextInput(placeholder='Describe the event'))
        self.loc_input = self.labeled_input(label='Location', input=toga.TextInput(placeholder='Location at where event is held'))
        self.start_date_input = self.labeled_input(label='Start Date', input=toga.DateInput())
        self.end_date_input = self.labeled_input(label='End Date', input=toga.DateInput())
        self.start_time_input = self.labeled_input(label='Start Time', input=toga.TimeInput())
        self.end_time_input = self.labeled_input(label='End Time', input=toga.TimeInput())

        # MISC
        self.priority = toga.Label('Priority:"')
        self.calendar = toga.Label('Calendar:"')
        self.timezone = toga.Label('Timezone:"')
        self.repeated = toga.Label('Repeated:"')
    
        self.misc_label = toga.Label('Misc:')
        self.misc_container = toga.SplitContainer()
        self.left_split = toga.Box(children=[self.priority, self.calendar], style=Pack(direction=COLUMN, padding_top=10))
        self.right_split = toga.Box(children=[self.timezone, self.repeated], style=Pack(direction=COLUMN, padding_top=10))
        self.misc_container.content = [(self.left_split, 1), (self.right_split, 1)]

        # Add to card
        self.content.add(self.event_input)
        self.content.add(self.desc_input)
        self.content.add(self.loc_input)
        self.content.add(self.start_date_input)
        self.content.add(self.end_date_input)
        self.content.add(self.start_time_input)
        self.content.add(self.end_time_input)
        self.content.add(self.misc_container)

    def labeled_input(self, label, input):
        # Container
        labeled_input_split = toga.SplitContainer()

        # UI
        label = toga.Label(f'{label}: ')
        labeled_input_split.content = [(label, 1), (input, 5)]
        return labeled_input_split
