import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW

class Card():
    def __init__(self) -> None:
        self.card = toga.Box(style=Pack(direction=COLUMN, padding_top=10))
        pass

    def get_card(self):
        return self.card
    
    def on_remove(self):
        pass
    
def OutlineStyle():
    return {
        'padding': 10,
        'border_color': 'black',
        'border_width': 1,
    }
