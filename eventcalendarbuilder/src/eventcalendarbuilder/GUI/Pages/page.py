import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW

class Page():
    def __init__(self) -> None:
        self.page_box = toga.Box(style=Pack(direction=COLUMN, padding_top=10, flex=1))
    
    def getPage(self):
        return self.page_box
    
    def on_remove(self):
        pass
