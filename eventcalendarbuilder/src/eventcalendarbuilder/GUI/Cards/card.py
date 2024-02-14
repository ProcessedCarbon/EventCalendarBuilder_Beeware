import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
from sys import platform

class Card():
    def __init__(self) -> None:
        color = (platform == 'win32') and 'grey' or 'transparent'
        self.card = toga.Box(style=Pack(background_color = color))
        self.content = toga.Box(style=Pack(direction=COLUMN, padding=10, flex=1))
        self.card.add(self.content)

    def get_card(self):
        return self.card
    
    def get_content(self):
        return self.content
    
    def on_remove(self):
        pass
