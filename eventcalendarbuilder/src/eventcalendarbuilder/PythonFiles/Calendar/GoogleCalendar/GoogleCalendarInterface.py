import os.path
import datetime as dt
from eventcalendarbuilder.PythonFiles.Calendar.GoogleCalendar.GoogleEvent import GoogleEvent
from eventcalendarbuilder.PythonFiles.Calendar.CalendarInterface import CalendarInterface
from eventcalendarbuilder.PythonFiles.Managers.DateTimeManager import DateTimeManager
import eventcalendarbuilder.PythonFiles.Managers.DirectoryManager as directory_manager

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import logging

SCOPES = ['https://www.googleapis.com/auth/calendar']
# GoogleCalendarAPI_path = "./GoogleCalendarAPI/"
# token_path = GoogleCalendarAPI_path + "token.json"
# credentials_path = GoogleCalendarAPI_path + "credentials.json"

main_path = directory_manager.getCurrentFileDirectory(__file__)
misc_path = directory_manager.getFilePath(main_path, 'GoogleCalendarAPI')
token_path = directory_manager.getFilePath(misc_path, 'token.json')
credentials_path = directory_manager.getFilePath(misc_path, 'credentials.json')

class GoogleCalendarInterface:
    creds = None
    service = None
    # Tries to establish connection with Google Calendar API
    def ConnectToGoogleCalendar():
        #print("ESTABLISHING CONNECTION TO GOOGLE CALENDARS......")
        logging.info("ESTABLISHING CONNECTION TO GOOGLE CALENDARS......")
        if os.path.exists(r'token_path'):
            GoogleCalendarInterface.creds = Credentials.from_authorized_user_file(token_path)
        
        if not GoogleCalendarInterface.creds or not GoogleCalendarInterface.creds.valid:
            if GoogleCalendarInterface.creds and GoogleCalendarInterface.creds.expired and GoogleCalendarInterface.creds.refresh_token:
                GoogleCalendarInterface.creds.refresh(Request())

            else:
                flow = InstalledAppFlow.from_client_secrets_file(credentials_path, SCOPES)
                GoogleCalendarInterface.creds = flow.run_local_server(port = 0)

            with open(token_path, "w") as token:
                token.write(GoogleCalendarInterface.creds.to_json())
        
        try:
            GoogleCalendarInterface.service = build("calendar", 'v3', credentials = GoogleCalendarInterface.creds)
            logging.info(f"[{__name__}] CONNECTION SUCCESSFUL")
        except HttpError as error:
            logging.error(f"[{__name__}] CONNECTION FAILURE WITH {error}")

    # Calendar event query
    def GetUpcomingCalendarEvent(count: int):
        """
        Obtains a list of upcoming count calendar events gotten from google calendar. 
        
        :param count (int): Number of events to get
        return: list of upcoming events from calendar
        """

        if GoogleCalendarInterface.service == None:
            print(f"[{__name__}] MISSING CONNECTION TO GOOGLE CALENDARS, PLEASE CONNECT TO GOOGLE CALENDARS FIRST")
            return

        now = dt.datetime.now().isoformat() + "Z"

        events_result = GoogleCalendarInterface.service.events().list(calendarId='primary', 
                                                                        timeMin=now,
                                                                        maxResults=count, 
                                                                        singleEvents=True,
                                                                        orderBy='startTime').execute()
            
        events = events_result.get('items', [])

        if not events:
            print("NO UPCOMING EVENTS FOUND")
            return
            
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            #print(start, event['summary'])

        return events

    # Event creation
    def ScheduleCalendarEvent(googleEvent: GoogleEvent)->str:
        """
        Creates the google event on the google calendar

        :param googleEvent (GoogleEvent): Google event to be created on calendar
        """
        
        if GoogleCalendarInterface.service == None:
            #print(f"[{__name__}] MISSING CONNECTION TO GOOGLE CALENDARS, PLEASE CONNECT TO GOOGLE CALENDARS FIRST")
            logging.error(f"[{__name__}] MISSING CONNECTION TO GOOGLE CALENDARS, PLEASE CONNECT TO GOOGLE CALENDARS FIRST")
            return '', []
        
        if type(googleEvent) is not GoogleEvent:
            #print(f"[{__name__}] INVALID EVENT OF GIVEN {type(googleEvent)}, LOOKING FOR - {GoogleEvent}")
            logging.error(f"[{__name__}] INVALID EVENT OF GIVEN {type(googleEvent)}, LOOKING FOR - {GoogleEvent}")
            return '', []
    
        new_event = GoogleCalendarInterface.service.events().insert(calendarId = "primary", body=googleEvent.event).execute()
        #print(f'{new_event}\n')
        #print(f"Event created {new_event.get('htmlLink')}")
        return new_event['id']

    # Creates event datatype
    def CreateGoogleEvent(title:str, location:str,  dtstart:str, dtend:str, tzstart:str, tzend:str, rrule:str, description:str ,colorId=1):
        """
        Returns the google calendar event format with the given entities in placed to be used to parsed to create a new event on google calendars
        https://developers.google.com/calendar/api/v3/reference/events
        
        :param str event: Name of event
        :param str location: Place where the event is to be
        :param str date_start: Start date of event
        :param str date_end: End date of event
        :param str time_start: Start timing of the event
        :param str time_end: End timing of the event
        :return: Event format using google calendars
        """
        return GoogleEvent(event=title, 
                            location=str(location), 
                            start_datetime=dtstart,
                            end_datetime=dtend,
                            colorId=colorId,
                            tzstart=tzstart,
                            tzend=tzend,
                            description=description,
                            rrule=rrule
                        )

    # Only expecting 1 event per ics
    def Parse_ICS(ics:str):
        if GoogleCalendarInterface.service == None:
            logging.warning(f"[{__name__}] MISSING CONNECTION TO GOOGLE CALENDARS, PLEASE CONNECT TO GOOGLE CALENDARS FIRST")
            return
        
        ics_file = CalendarInterface.ReadICSFile(ics)
        for component in ics_file.walk():
            if component.name == "VEVENT":
                start_datetime = component.get('dtstart').dt.isoformat()
                end_datetime = component.get('dtend').dt.isoformat()
                tzstart = str(component.get('dtstart').dt.tzinfo)
                tzend = str(component.get('dtstart').dt.tzinfo)
                rule='RRULE:' + component.get('rrule').to_ical().decode(errors="ignore")+'Z' if component.get('rrule') is not None else ''

                return GoogleCalendarInterface.CreateGoogleEvent(title=component.get('name'),
                                                                location=component.get("location"),
                                                                dtstart=start_datetime,
                                                                dtend=end_datetime,
                                                                tzstart=tzstart,
                                                                tzend=tzend,
                                                                description=component.get('description'),
                                                                rrule=str(rule) if rule != '' else [],
                                                                )
        return None
    
    def getEvents(calendar_id='primary', time_min=None, time_max=None)->list[GoogleEvent]:
        """Get events from a specific calendar within a time range."""
        existing = GoogleCalendarInterface.service.events().list(calendarId=calendar_id, timeMin=time_min, timeMax=time_max).execute().get('items', [])
        existing_google_events = [GoogleCalendarInterface.CreateGoogleEvent(
                                                                            title=x['summary'],
                                                                            location=x['location'] if "location" in x else "", # Done this way as might be empty
                                                                            dtstart=x['start']['dateTime'],
                                                                            tzstart=x['start']['timeZone'],
                                                                            dtend=x['end']['dateTime'],
                                                                            tzend=x['end']['timeZone'],
                                                                            description=x['description'],
                                                                            rrule=x['recurrence'] if 'recurrence' in x else ''
                                                                        ) for x in existing]
        return existing_google_events  

    def EventOverlaps(new_event:GoogleEvent, existing_events:list[GoogleEvent])->bool:
        """Check if the new event overlaps with any existing events."""
        overlapped_events = []
        # 2023-01-31 18:00:00+08:00
        new_event_start = new_event.getStartDate().replace("T", " ") 
        new_event_end = new_event.getUNTILDate().replace("T", " ")

        for event in existing_events:
            event_start = event.getStartDate().replace("T", " ")
            event_end = event.getEndDate().replace("T", " ")

            if DateTimeManager.hasDateTimeClash(new_event_start, new_event_end, event_start, event_end):
                #print(f'Event to schedule {new_event.getEvent().upper()} has clash with {event.getEvent().upper()}!')
                overlapped_events.append(event)
        return overlapped_events #False
    
    def DeleteEvent(id:str)->[bool,str]:
        if GoogleCalendarInterface.service == None:
            logging.warning(f"[{__name__}] MISSING CONNECTION TO GOOGLE CALENDARS, PLEASE CONNECT TO GOOGLE CALENDARS FIRST")
            return False,''
        
        try:
            GoogleCalendarInterface.service.events().delete(calendarId='primary', eventId=id).execute()
            #print(f"[{__name__}] EVENT DELETED SUCCESSFULLY")
            logging.info(f"[{__name__}] EVENT DELETED SUCCESSFULLY")
            return True,''
        except HttpError as e:
            #print(f"Error: {e.error_details[0]['reason']}")
            error_details = e.error_details[0]
            if 'reason' in error_details['reason'] and error_details['reason'] != '':
                return False, error_details['reason']
            else: return False, 'Unknown Reason, Proceeding to Deletion'
