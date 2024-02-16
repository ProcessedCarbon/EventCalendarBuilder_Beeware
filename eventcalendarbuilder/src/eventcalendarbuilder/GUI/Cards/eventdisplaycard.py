import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW, CENTER
from toga.constants import Direction

from eventcalendarbuilder.GUI.Cards.card import Card

from eventcalendarbuilder.PythonFiles.Calendar.calendar_constants import DEFAULT_CALENDAR, GOOGLE_CALENDAR, OUTLOOK_CALENDAR
from eventcalendarbuilder.PythonFiles.Calendar.GoogleCalendar.GoogleCalendarInterface import GoogleCalendarInterface
import eventcalendarbuilder.PythonFiles.Calendar.Outlook.OutlookInterface as outlook_interface
import eventcalendarbuilder.PythonFiles.Calendar.CalendarMacInterface as calendarmac_interface
from eventcalendarbuilder.PythonFiles.Events.EventsManager import EventsManager

from sys import platform

class EventDisplayCard(Card):
    def __init__(self, event:dict, remove_cb) -> None:
        super().__init__(color='grey')
        self.platform = event['platform']
        self.id = event['id']
        self.name = event['name']
        self.remove_cb = remove_cb

        # MAIN
        self.event_container, self.event_input, self.event_label = self.labeled_input(label='Event', input=toga.MultilineTextInput(value=self.name, style=Pack(flex=1), readonly=True))
        self.desc_container, self.desc_input, self.desc_label = self.labeled_input(label='Description', input=toga.MultilineTextInput(value=event['description'], style=Pack(flex=1), readonly=True))
        self.loc_container, self.loc_input, self.loc_label = self.labeled_input(label='Location', input=toga.MultilineTextInput(value=event['location'], style=Pack(flex=1), readonly=True))
        self.start_date_container, self.start_date_input, self.start_date_label = self.labeled_input(label='Start Date', input=toga.Label(text=event['s_date'], style=Pack(flex=1)))
        self.end_date_container, self.end_date_input, self.end_date_label = self.labeled_input(label='End Date', input=toga.Label(text=event['e_date'], style=Pack(flex=1)))
        self.start_time_container, self.start_time_input, self.start_time_label = self.labeled_input(label='Start Time', input=toga.Label(text=event['start_time'], style=Pack(flex=1)))
        self.end_time_container, self.end_time_input, self.end_time_label = self.labeled_input(label='End Time', input=toga.Label(text=event['end_time'], style=Pack(flex=1)))

        # MISC
        self.calendar_container = toga.Box(children=[toga.Label('Calendar:'), toga.Divider(direction=Direction.VERTICAL), toga.Label(self.platform)], style=Pack(padding=5, alignment=CENTER))
        self.timezone_container = toga.Box(children=[toga.Label('Timezone:'), toga.Divider(direction=Direction.VERTICAL), toga.Label(event['timezone'])], style=Pack(padding=5, alignment=CENTER))
        self.repeated_container = toga.Box(children=[toga.Label('Repeated:'), toga.Divider(direction=Direction.VERTICAL), toga.Label(event['recurring'])], style=Pack(padding=5, alignment=CENTER))

        self.misc_label = toga.Label('Misc:')
        self.misc_container = toga.SplitContainer()
        self.left_split = toga.Box(children=[self.calendar_container], style=Pack(direction=COLUMN, padding_top=10))
        self.right_split = toga.Box(children=[self.timezone_container, self.repeated_container], style=Pack(direction=COLUMN, padding_top=10))
        self.misc_container.content = [(self.left_split, 1), (self.right_split, 1)]

        # Remove btn
        self.remove_btn = toga.Button('Remove', on_press=self.remove_event_trigger)

        # Add to card
        self.content.add(self.event_container)
        self.content.add(self.desc_container)
        self.content.add(self.loc_container)
        self.content.add(self.start_date_container)
        self.content.add(self.end_date_container)
        self.content.add(self.start_time_container)
        self.content.add(self.end_time_container)
        self.content.add(self.misc_label)
        self.content.add(self.misc_container)
        self.content.add(self.remove_btn)

    def labeled_input(self, label, input):
        # Container
        labeled_input_container = toga.SplitContainer()

        # UI
        label = toga.Label(f'{label}: ')
        
        #labeled_input_container = toga.Box(children=[label, toga.Divider(direction=Direction.VERTICAL), input], style=Pack(padding=10))
        labeled_input_container.content = [(label, 1), (input, 5)]
        return labeled_input_container, input, label
    
    async def remove_event_trigger(self, widget):
        self.delete_confirm = await toga.Window().confirm_dialog(title='Warning!', message=f'Are you sure you wish to remove {self.name} from {self.platform} calendar')

        if self.delete_confirm:
            res = self.remove_event(calendar=self.platform)
            EventsManager.RemoveFromEventDB(id=self.id, target=EventsManager.events_db)

            if res != '': toga.Window().error_dialog(title='Warning!', message=res) # There is an error show error
            else : toga.Window().info_dialog(title='Done!', message=f'Successful deletion of {self.name} event on {self.platform} calendar')

            self.remove_cb(card=self.card)
        else: return

    def remove_event(self, calendar):
        if calendar == DEFAULT_CALENDAR: # not supported for now
            try:
                if platform == 'darwin': calendarmac_interface.RemoveMacCalendarEvents(self.name)
                else: self.remove_outlook()
                return ''
            except: return f'Cannot find {self.name} on {DEFAULT_CALENDAR} calendar, removing instance.'
        elif calendar == GOOGLE_CALENDAR:
            remove, res = GoogleCalendarInterface.DeleteEvent(self.id)
            return res
        elif calendar == OUTLOOK_CALENDAR:
            remove, res = self.remove_outlook()
            return res
        else:
            return f'Could not find calendar of {calendar} calendar. No removal executed.'
    
    def remove_outlook(self)->bool:
        removed, response = outlook_interface.send_flask_req('delete_event', json_data={'event_id':self.id})
        return removed, response