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
from eventcalendarbuilder.GUI.Pages.schedule_event_page import ScheduleEventPage
from eventcalendarbuilder.GUI.Pages.manage_event_page import ManageEventPage

# GUI
from eventcalendarbuilder.GUI.navbar import NavBar

ENABLE_GOOGLE = True
ENABLE_OUTLOOK = False

class EventCalendarBuilder(toga.App):
    def startup(self):
        """Construct and show the Toga application.

        Usually, you would add your application to a main content box.
        We then create a main window (with a name matching the app), and
        show the main window.
        """
        # APIs
        if ENABLE_GOOGLE: GoogleCalendarInterface.ConnectToGoogleCalendar()
        if ENABLE_OUTLOOK: outlook_interface.start_flask()
        
        self.pages = []
        self.main_window = toga.MainWindow(title=self.formal_name)
        
        # Pages
        schedule_event_page = ScheduleEventPage()
        manage_event_page = ManageEventPage()
        self.pages.append(schedule_event_page)
        self.pages.append(manage_event_page)

        # Right Side Container (Pages)
        self.current_page = schedule_event_page
        self.right_container = toga.ScrollContainer(horizontal=False)
        self.right_container.content = toga.Box(children=[self.current_page.getPage()], style=Pack(direction=COLUMN))

        # Left Side Container (NavBar)
        nav_bar = NavBar(nav_bar_buttons={
            "Schedule Events" : lambda widget:self.show_page(0),
            "Manage Events" : lambda widget:self.show_page(1)
        })
        left_container = toga.ScrollContainer(horizontal=False)
        left_container.content = nav_bar.get_navbar()

        # Add the button box and content box to the main window
        split = toga.SplitContainer()
        split.content = [(left_container, 1), (self.right_container, 5)]
        self.main_window.content = split

        self.main_window.show()

    def show_page(self, page_number):
        self.current_page.on_remove()
        self.right_container.content.remove(self.current_page.getPage())
        self.current_page = self.pages[page_number]
        self.right_container.content.add(self.current_page.getPage())

def main():
    return EventCalendarBuilder()
