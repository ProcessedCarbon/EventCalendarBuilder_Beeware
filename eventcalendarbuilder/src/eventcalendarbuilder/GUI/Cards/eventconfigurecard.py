import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW, CENTER
from toga.constants import Direction

from eventcalendarbuilder.GUI.Cards.card import Card
from eventcalendarbuilder.PythonFiles.Calendar.calendar_constants import GOOGLE_CALENDAR, OUTLOOK_CALENDAR, DEFAULT_CALENDAR, RecurrenceTypes, ScheduleStatus
from eventcalendarbuilder.PythonFiles.Managers.TextProcessing import TextProcessingManager
from eventcalendarbuilder.PythonFiles.Events.EventsManager import EventsManager, Event

import pytz
from sys import platform
import re

DATE_PATTERN = re.compile(r'^\d{4}-\d{2}-\d{2}$')
TIME_PATTERN = re.compile(r'^([01]\d|2[0-3]):([0-5]\d):([0-5]\d)$')

class EventConfigureCard(Card):
    def __init__(self, event: Event, remove_cb=None) -> None:
        color = (platform=='win32') and 'grey' or 'transparent'
        super().__init__(color=color)
        self.event = event
        self.remove_cb = remove_cb

        # MAIN
        self.event_container, self.event_input, self.event_label = self.labeled_input(label='Event', input=toga.MultilineTextInput(placeholder='Name of event', style=Pack(flex=1)))
        self.desc_container, self.desc_input, self.desc_label = self.labeled_input(label='Description', input=toga.MultilineTextInput(placeholder='Describe the event', style=Pack(flex=1)))
        self.loc_container, self.loc_input, self.loc_label = self.labeled_input(label='Location', input=toga.MultilineTextInput(placeholder='Location at where event is held', style=Pack(flex=1)))
        
        # temp: Only display datetime for windows
        if platform == 'win32':
            self.start_date_container, self.start_date_input, self.start_date_label = self.labeled_input(label='Start Date', input=toga.DateInput(style=Pack(flex=1)))
            self.end_date_container, self.end_date_input, self.end_date_label = self.labeled_input(label='End Date', input=toga.DateInput(style=Pack(flex=1)))
            self.start_time_container, self.start_time_input, self.start_time_label = self.labeled_input(label='Start Time', input=toga.TimeInput(style=Pack(flex=1)))
            self.end_time_container, self.end_time_input, self.end_time_label = self.labeled_input(label='End Time', input=toga.TimeInput(style=Pack(flex=1)))
        else:
            self.start_date_container, self.start_date_input, self.start_date_label = self.labeled_input(label='Start Date', input=toga.TextInput(placeholder='YYYY-MM-DD',style=Pack(flex=1)))
            self.end_date_container, self.end_date_input, self.end_date_label = self.labeled_input(label='End Date', input=toga.TextInput(placeholder='YYYY-MM-DD', style=Pack(flex=1)))
            self.start_time_container, self.start_time_input, self.start_time_label = self.labeled_input(label='Start Time', input=toga.TextInput(placeholder='HH:MM:SS', style=Pack(flex=1)))
            self.end_time_container, self.end_time_input, self.end_time_label = self.labeled_input(label='End Time', input=toga.TextInput(placeholder='HH:MM:SS', style=Pack(flex=1)))

        # Insert known values
        self.event_input.value = self.event.getName()
        self.loc_input.value = self.event.getLocation()
        self.start_date_input.value = self.event.get_S_Date()
        self.end_date_input.value = self.event.get_E_Date()
        self.start_time_input.value = self.event.getStart_Time()
        self.end_time_input.value = self.event.getEnd_Time()

        # MISC
        self.calendar_input = toga.Selection(items=[DEFAULT_CALENDAR, GOOGLE_CALENDAR, OUTLOOK_CALENDAR], style=Pack(padding=5))
        self.timezone_input = toga.Selection(items=pytz.all_timezones, style=Pack(padding=5))
        self.timezone_input.value = "Asia/Singapore"
        self.repeated_input = toga.Selection(items=[RecurrenceTypes.NONE.value, RecurrenceTypes.DAILY.value, RecurrenceTypes.WEEKLY.value, RecurrenceTypes.MONTHLY.value], style=Pack(padding=5))

        self.calendar_container = toga.Box(children=[toga.Label('Calendar:'), toga.Divider(direction=Direction.VERTICAL), self.calendar_input], style=Pack(padding=5, alignment=CENTER))
        self.timezone_container = toga.Box(children=[toga.Label('Timezone:'), toga.Divider(direction=Direction.VERTICAL), self.timezone_input], style=Pack(padding=5, alignment=CENTER))
        self.repeated_container = toga.Box(children=[toga.Label('Repeated:'), toga.Divider(direction=Direction.VERTICAL), self.repeated_input], style=Pack(padding=5, alignment=CENTER))

        self.misc_label = toga.Label('Misc:')
        self.misc_container = toga.SplitContainer()
        self.left_split = toga.Box(children=[self.calendar_container], style=Pack(direction=COLUMN, padding_top=10))
        self.right_split = toga.Box(children=[self.timezone_container, self.repeated_container], style=Pack(direction=COLUMN, padding_top=10))
        self.misc_container.content = [(self.left_split, 1), (self.right_split, 1)]

        # SUBMIT BTN
        self.submit_btn = toga.Button(text='Schedule', on_press=self.submit_event, style=Pack(padding_top=10))

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
        self.content.add(self.submit_btn)

    def labeled_input(self, label, input):
        # Container
        labeled_input_container = toga.SplitContainer()

        # UI
        label = toga.Label(f'{label}: ')
        
        #labeled_input_container = toga.Box(children=[label, toga.Divider(direction=Direction.VERTICAL), input], style=Pack(padding=10))
        labeled_input_container.content = [(label, 1), (input, 5)]
        return labeled_input_container, input, label
    
    def get_all_values(self):
        # Check format
        start_date = str(self.start_date_input.value)
        end_date = str(self.end_date_input.value)
        start_time = str(self.start_time_input.value)
        end_time = str(self.end_time_input.value)

        if bool(DATE_PATTERN.match(start_date)) == False: return {}, 'Invalid Start Date!'
        elif bool(DATE_PATTERN.match(end_date)) == False: return {}, 'Invalid End Date!'
        elif bool(TIME_PATTERN.match(start_time)) == False: return {}, 'Invalid Start Time!'
        elif bool(TIME_PATTERN.match(end_time)) == False: return {}, 'Invalid End Time!'
        elif self.event_input.value == '' or self.event_input.value == ' ' or self.event_input.value == '\n': return {}, 'Missing Event Name!'

        ics_s_date = TextProcessingManager.ProcessDateToICSFormat(start_date)
        ics_e_date = TextProcessingManager.ProcessDateToICSFormat(end_date)
        ics_time = TextProcessingManager.ProcessTimeToICSFormat([start_time, end_time])
        ics_s, ics_e = TextProcessingManager.ProcessICS(ics_s_date, ics_e_date, ics_time)

        # Update event details only attainable from input
        self.event.setName(self.event_input.value)
        self.event.setDescription(self.desc_input.value)
        self.event.setLocation(self.loc_input.value)
        self.event.set_S_Date(self.start_date_input.value)
        self.event.set_E_Date(self.end_date_input.value)
        self.event.setStart_Time(self.start_time_input.value)
        self.event.setEnd_Time(self.end_time_input.value)
        self.event.setPlatform(self.calendar_input.value)
        self.event.setTimezone(self.timezone_input.value)
        self.event.setRecurring(self.repeated_input.value)

        return {
            'Event' : self.event_input.value,
            'Location' : self.loc_input.value,
            'Description' : self.desc_input.value,
            'Start_Date' : self.start_date_input.value,
            'End_Date' : self.end_date_input.value,
            'Start_Time' : self.start_time_input.value,
            'End_Time' : self.end_time_input.value,
            'Start_Time_ICS': ics_s,
            'End_Time_ICS' : ics_e,
            'Calendar' : self.calendar_input.value,
            'Timezone' : self.timezone_input.value,
            'Repeated' : self.repeated_input.value
        }, ''
    
    async def submit_event(self, widget):
        input, res = self.get_all_values()

        if res != '':
            toga.Window().error_dialog(title='Warning!', message=res)
            return

        clash = None
        cb = None
        clash_text = ''

        if self.calendar_input.value == DEFAULT_CALENDAR: 
            self.default_confirm = await toga.Window().confirm_dialog(title='Warning!', message='You will not be able to manage default scheduled events, do you wish to proceed?')
            if self.default_confirm:
                clash, cb = EventsManager.ScheduleDefault(input, schedule_cb=self.schedule_actions)# No clash checking done for default yet
            else: return
        elif self.calendar_input.value == GOOGLE_CALENDAR: 
            clash, cb = EventsManager.ScheduleGoogleCalendar(input, schedule_cb=self.schedule_actions)
        elif self.calendar_input.value == OUTLOOK_CALENDAR: 
            clash, cb = EventsManager.ScheduleOutlookCalendar(input, schedule_cb=self.schedule_actions)
        
        if len(clash) > 0:
            for t in clash: clash_text += (t + '\n')
            self.clash_confirm = await toga.Window().confirm_dialog(title='Clash!', message=f'There is a clash with the following events:\n{clash_text}\nDo you still wish to schedule?')
            if self.clash_confirm:
                cb()
        else: cb()

    def schedule_actions(self, id, platform=DEFAULT_CALENDAR):
        if platform != '':
            self.event.setPlatform(platform)
            self.event.setId(id)
            EventsManager.AddEventToEventDB(self.event, EventsManager.events_db)
            toga.Window().info_dialog(title='Success!', message="Successfully scheduled the event!")
        self.remove_cb(card=self.card)