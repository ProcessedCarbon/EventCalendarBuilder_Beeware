import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW

REMOVE_CARD_MSG = 'Are you sure you wish to remove this card?'

class Card():
    def __init__(self, parent, color='transparent') -> None:
        self.parent = parent
        self.card = toga.Box(style=Pack(background_color = color))
        self.content = toga.Box(style=Pack(direction=COLUMN, padding=10, flex=1))
        self.card.add(self.content)

    def get_card(self):
        return self.card
    
    def get_content(self):
        return self.content
    
    def on_remove(self):
        pass

    async def ask_before_remove(self, widget):
        confirm_window = await toga.Window().confirm_dialog(title='Are you sure?', message=REMOVE_CARD_MSG)
        if confirm_window:
            self.remove_from()
        else: return

    def remove_from(self):
        self.parent.remove(self.card)