import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW

class NavBar():
    def __init__(self, nav_bar_buttons = {}) -> None:
        self.content = toga.Box(style=Pack(direction=COLUMN, padding_top=10))
        self.add_buttons(nav_bar_buttons)
    
    def add_buttons(self, buttons = {}):
        if len(buttons) == 0:
            return
        
        for b in buttons:
            self.content.add(toga.Button(b, on_press=buttons[b], style=Pack(padding_top=10)))
    
    def get_navbar(self):
        return self.content