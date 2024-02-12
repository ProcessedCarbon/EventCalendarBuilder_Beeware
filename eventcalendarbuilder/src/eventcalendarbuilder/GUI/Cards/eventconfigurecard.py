import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW

from eventcalendarbuilder.GUI.Cards.card import Card

class EventConfigureCard(Card):
    def __init__(self) -> None:
        super().__init__()
        # MAIN
        self.event = toga.Label('Event:"')
        self.description = toga.Label('Description:"')
        self.location = toga.Label('Location:"')
        self.start_date = toga.Label('Start Date:"')
        self.end_date = toga.Label('End Date:"')
        self.start_time = toga.Label('Start Time:"')
        self.end_time = toga.Label('End Time:"')

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

        self.card.add(self.event)
        self.card.add(self.description)
        self.card.add(self.location)
        self.card.add(self.start_date)
        self.card.add(self.end_date)
        self.card.add(self.start_time)
        self.card.add(self.end_time)
        self.card.add(self.misc_container)

