import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW, CENTER
from toga.constants import Direction

from eventcalendarbuilder.GUI.Cards.card import Card
from eventcalendarbuilder.PythonFiles.Calendar.calendar_constants import GOOGLE_CALENDAR, OUTLOOK_CALENDAR, DEFAULT_CALENDAR, RecurrenceTypes, ScheduleStatus
from eventcalendarbuilder.PythonFiles.Managers.TextProcessing import TextProcessingManager
from eventcalendarbuilder.PythonFiles.Events.EventsManager import EventsManager, Event
import pytz

class EventConfigureCard(Card):
    def __init__(self, event: Event, remove_cb=None) -> None:
        super().__init__()
        self.event = event
        self.remove_cb = remove_cb

        # MAIN
        self.event_container, self.event_input, self.event_label = self.labeled_input(label='Event', input=toga.MultilineTextInput(placeholder='Name of event', style=Pack(flex=1)))
        self.desc_container, self.desc_input, self.desc_label = self.labeled_input(label='Description', input=toga.MultilineTextInput(placeholder='Describe the event', style=Pack(flex=1)))
        self.loc_container, self.loc_input, self.loc_label = self.labeled_input(label='Location', input=toga.MultilineTextInput(placeholder='Location at where event is held', style=Pack(flex=1)))
        self.start_date_container, self.start_date_input, self.start_date_label = self.labeled_input(label='Start Date', input=toga.DateInput(style=Pack(flex=1)))
        self.end_date_container, self.end_date_input, self.end_date_label = self.labeled_input(label='End Date', input=toga.DateInput(style=Pack(flex=1)))
        self.start_time_container, self.start_time_input, self.start_time_label = self.labeled_input(label='Start Time', input=toga.TimeInput(style=Pack(flex=1)))
        self.end_time_container, self.end_time_input, self.end_time_label = self.labeled_input(label='End Time', input=toga.TimeInput(style=Pack(flex=1)))

        # Insert known values
        self.event_input.value = self.event.getName()
        self.loc_input.value = self.event.getLocation()
        self.start_date_input.value = self.event.get_S_Date()
        self.end_date_input.value = self.event.get_E_Date()
        self.start_time_input.value = self.event.getStart_Time()
        self.end_time_input.value = self.event.getEnd_Time()

        # MISC
        self.priority = toga.Selection(items=['1', '2', '3', '4', '5'], style=Pack(padding=5))
        self.calendar = toga.Selection(items=[DEFAULT_CALENDAR, GOOGLE_CALENDAR, OUTLOOK_CALENDAR], style=Pack(padding=5))
        self.timezone = toga.Selection(items=pytz.all_timezones, style=Pack(padding=5))
        self.timezone.value = "Asia/Singapore"
        self.repeated = toga.Selection(items=[RecurrenceTypes.NONE.value, RecurrenceTypes.DAILY.value, RecurrenceTypes.WEEKLY.value, RecurrenceTypes.MONTHLY.value], style=Pack(padding=5))
    
        self.misc_label = toga.Label('Misc:')
        self.misc_container = toga.SplitContainer()
        self.left_split = toga.Box(children=[self.priority, self.calendar], style=Pack(direction=COLUMN, padding_top=10))
        self.right_split = toga.Box(children=[self.timezone, self.repeated], style=Pack(direction=COLUMN, padding_top=10))
        self.misc_container.content = [(self.left_split, 1), (self.right_split, 1)]

        # SUBMIT BTN
        self.submit_btn = toga.Button(text='Schedule', on_press=self.submit_event)

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
        ics_s_date = TextProcessingManager.ProcessDateToICSFormat(str(self.start_date_input.value))
        ics_e_date = TextProcessingManager.ProcessDateToICSFormat(str(self.end_date_input.value))
        ics_time = TextProcessingManager.ProcessTimeToICSFormat([str(self.start_time_input.value), str(self.end_time_input.value)])
        ics_s, ics_e = TextProcessingManager.ProcessICS(ics_s_date, ics_e_date, ics_time)

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
            'Calendar' : self.calendar.value,
            'Priority' : self.priority.value,
            'Timezone' : self.timezone.value,
            'Repeated' : self.repeated.value
        }
    
    async def submit_event(self, widget):
        input = self.get_all_values()
        clash = None
        cb = None
        clash_text = ''

        if self.calendar.value == DEFAULT_CALENDAR: 
            self.default_confirm = await toga.Window().confirm_dialog(title='Warning!', message='You will not be able to manage default scheduled events, do you wish to proceed?')
            if self.default_confirm:
                clash, cb = EventsManager.ScheduleDefault(input, schedule_cb=self.schedule_actions)# No clash checking done for default yet
        elif self.calendar.value == GOOGLE_CALENDAR: 
            clash, cb = EventsManager.ScheduleGoogleCalendar(input, schedule_cb=self.schedule_actions)
        elif self.calendar.value == OUTLOOK_CALENDAR: 
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
            EventsManager.WriteEventDBToJSON()
            toga.Window().info_dialog(title='Success!', message="Successfully scheduled the event!")
        self.remove_cb(card=self.card)