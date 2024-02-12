import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW

class Card():
    def __init__(self) -> None:
        self.card = toga.Box(style=Pack(background_color = 'blue'))
        self.content = toga.Box(style=Pack(direction=COLUMN, padding=10, flex=1))
        self.card.add(self.content)

    def get_card(self):
        return self.card
    
    def get_content(self):
        return self.content
    
    def on_remove(self):
        pass
