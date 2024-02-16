import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW

class Page():
    def __init__(self) -> None:
        self.page_box = toga.Box(style=Pack(flex=1))
        self.content = toga.Box(style=Pack(direction=COLUMN, padding=10, flex=1))
        self.page_box.add(self.content)
    
    def getPage(self):
        return self.page_box

    def get_content(self):
        return self.content
    
    def on_exit(self):
        pass

    def on_enter(self):
        pass
