import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW

class Page():
    def __init__(self) -> None:
        self.page_box = toga.Box()
    
    def getPage(self):
        return self.page_box
