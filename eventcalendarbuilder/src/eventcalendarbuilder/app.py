"""
My FYP
"""
import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW

# Custom modules
from eventcalendarbuilder.PythonFiles.Calendar.GoogleCalendar.GoogleCalendarInterface import GoogleCalendarInterface
import eventcalendarbuilder.PythonFiles.Calendar.Outlook.OutlookInterface as outlook_interface

# Pages
from eventcalendarbuilder.Pages.schedule_event_page import ScheduleEventPage

class EventCalendarBuilder(toga.App):
    def startup(self):
        """Construct and show the Toga application.

        Usually, you would add your application to a main content box.
        We then create a main window (with a name matching the app), and
        show the main window.
        """
        # GoogleCalendarInterface.ConnectToGoogleCalendar()
        # outlook_interface.start_flask()
        self.pages = []

        # App nav bar
        left_content = toga.Box(style=Pack(direction=COLUMN, padding_top=10))
        left_content.add(toga.Button('Schedule Events', on_press=lambda widget:self.show_page(0)))
        left_content.add(toga.Button('Manage Events', on_press=lambda widget:self.show_page(1)))
        left_container = toga.ScrollContainer(horizontal=False)
        left_container.content = left_content

        self.right_container = toga.ScrollContainer(horizontal=False)

        self.main_window = toga.MainWindow(title=self.formal_name)
        
        # Pages
        schedule_event_page = ScheduleEventPage()

        # Create content for Page 2
        self.page2_box = toga.Box()
        self.page2_label = toga.Label('This is Page 2')
        self.page2_textinput = toga.TextInput()
        self.page2_box.add(self.page2_label)
        self.page2_box.add(self.page2_textinput)

        # Append pages to list
        self.pages.append(schedule_event_page.getPage())
        self.pages.append(self.page2_box)

        # Create a box container for the content
        self.current_page = schedule_event_page.getPage()
        self.right_container = toga.Box(children=[self.current_page], style=Pack(direction=COLUMN))

        # Add the button box and content box to the main window
        split = toga.SplitContainer()
        split.content = [(left_container, 1), (self.right_container, 2)]
        self.main_window.content = split

        self.main_window.show()

    def show_page(self, page_number):
        self.right_container.remove(self.current_page)
        self.current_page = self.pages[page_number]
        self.right_container.add(self.current_page)

def main():
    return EventCalendarBuilder()
