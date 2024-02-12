import requests
from flask import Flask, request, jsonify
import uuid
import webbrowser
from eventcalendarbuilder.PythonFiles.Calendar.CalendarInterface import CalendarInterface
import eventcalendarbuilder.PythonFiles.Managers.DirectoryManager as directory_manager
import threading
import logging
from werkzeug.middleware.proxy_fix import ProxyFix

app = Flask(__name__)
app.secret_key = 'EventCalendarBuilder'  # Change this
local_host = 8000

CLIENT_ID = "99b8766f-5d52-490c-8237-187338d09615"
CLIENT_SECRET = "_xm8Q~VKXbbgvNF8mT5BUAMr5I_XyE3Q18aRNczT"
REDIRECT_URI=f'http://localhost:{local_host}/callback'
AUTHORITY_URL = 'https://login.microsoftonline.com/common'
SCOPES = "openid User.Read Calendars.ReadWrite MailboxSettings.Read"

token_path = directory_manager.getCurrentFileDirectory(__file__)

# Format:
# https://learn.microsoft.com/en-us/graph/api/calendar-post-events?view=graph-rest-1.0&tabs=http
class OutlookEvent():
    def __init__(self, 
                 name:str, location:str,  dtstart:str, rrule:str,
                 dtend:str, tzstart:str, tzend:str, isonline=False) -> None:
        
        self.name = name
        self.location = location
        self.dtstart = dtstart
        self.dtend = dtend
        self.tzstart = tzstart
        self.tzend = tzend
        self.isonline = isonline
        self.rrule = rrule
        
        self.event = {
            "subject": name,
            "body": {
                "contentType": "HTML",
                "content": ""
            },
            "start": {
                "dateTime": dtstart,
                "timeZone": tzstart
            },
            "end": {
                "dateTime": dtend,
                "timeZone": tzend
            },
            "location":{
                "displayName":location
            },
            "isOnlineMeeting": isonline,
            # "attendees": [
            #     {
            #     "emailAddress": {
            #         "address":"adelev@contoso.onmicrosoft.com",
            #         "name": "Adele Vance"
            #     },
            #     "type": "required"
            #     }
            # ],
            # "transactionId":"7E163156-7762-4BEB-A1C6-729EA81755A7"
            }
        self.reccurence_pattern = self.getRecurrencePatternFromRRULE(rrule=self.rrule)
        if self.reccurence_pattern != {}: self.event['recurrence'] = self.reccurence_pattern

    
    def get_name(self):
        return self.name
    
    def get_location(self):
        return self.location
    
    def get_dtstart(self):
        return self.dtstart
    
    def get_dtend(self):
        return self.dtend
    
    def get_tzstart(self):
        return self.tzstart
    
    def get_tzend(self):
        return self.tzend
    
    def get_isonline(self):
        return self.isonline
    
    def get_rrule(self):
        return self.rrule

    # Assuming RRULES come in the following format
    # FREQ=DAILY;INTERVAL=10;COUNT=5 
    def getRecurrencePatternFromRRULE(self, rrule:str):
        if rrule == '': return {}
        split = rrule.split(';')
        rule_dict = {}
        # Convert each split into a single dictionary
        for s in split:
            split_s = s.split('=')
            key = split_s[0]
            val = split_s[1]
            rule_dict[key] = val
        
        freq = rule_dict['FREQ'].lower() if 'FREQ' in rule_dict else ''
        end_y = rule_dict['UNTIL'][:4]
        end_m = rule_dict['UNTIL'][4:6] 
        end_d = rule_dict['UNTIL'][6:8] 
        end_date = f'{end_y}-{end_m}-{end_d}'

        s_date = self.dtstart.split('T')[0]
        return {
            "pattern": {
                "type": freq,
                "interval": 1
            },
            "range": {
                "type": "endDate",
                "startDate": s_date,
                "endDate": end_date
            }
        }

@app.route('/')
def login():
    # Generate the full authorization endpoint on Microsoft's identity platform
    authorization_url = f"{AUTHORITY_URL}/oauth2/v2.0/authorize?client_id={CLIENT_ID}&response_type=code&redirect_uri={REDIRECT_URI}&response_mode=query&scope={SCOPES}&state={uuid.uuid4()}"

    # Open the browser for authentication
    webbrowser.open(authorization_url)

    return "Authentication started. Please check your browser."

@app.route('/callback')
def callback():
    code = request.args.get('code')
    if not code:
        directory_manager.WriteJSON(token_path, 'api_token_access.json', '')
        return "Failed Authentication."

    token_url = f"{AUTHORITY_URL}/oauth2/v2.0/token"
    token_data = {
        'grant_type': 'authorization_code',
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'scope': SCOPES,
        'code': code,
        'redirect_uri': REDIRECT_URI
    }
    token_r = requests.post(token_url, data=token_data)
    directory_manager.WriteJSON(token_path, 'api_token_access.json', token_r.json())
    return 'Authentication Successful can close browser'

@app.route('/create_event')
def create_event():   
    token_access = directory_manager.ReadJSON(token_path, 'api_token_access.json')
    token = token_access['access_token']

    if not token: return jsonify(status="error", message="Not authenticated!"), 401
    
    event = request.json['event']
    
    headers = {
        'Authorization': f'{token_access["token_type"]} {token}',
        'Content-Type': 'application/json'
    }
    #print(f'Event param: {event}')
    response = requests.post("https://graph.microsoft.com/v1.0/me/events", headers=headers, json=event)
    return response.json()

@app.route('/delete_event')
def delete_event():   
    token_access = directory_manager.ReadJSON(token_path, 'api_token_access.json')
    token = token_access['access_token']

    if not token:
        return jsonify(status="error", message="Not authenticated!"), 401
    
    event_id = request.json['event_id']

    headers = {
        'Authorization': f'{token_access["token_type"]} {token}',
        'Content-Type': 'application/json'
    }

    response = requests.delete(f"https://graph.microsoft.com/v1.0/me/events/{event_id}", headers=headers)
    #print(f'DELETE RESPONSE STATUS CODE: {response.status_code}')
    logging.info(f'DELETE RESPONSE STATUS CODE: {response.status_code}')
    return {}

@app.route('/get_events')
def get_events():   
    token_access = directory_manager.ReadJSON(token_path, 'api_token_access.json')
    token = token_access['access_token']

    if not token:
        return jsonify(status="error", message="Not authenticated!"), 401
    
    headers = {
        'Authorization': f'{token_access["token_type"]} {token}',
        'Content-Type': 'application/json'
    }

    response = requests.get(f"https://graph.microsoft.com/v1.0/me/events", headers=headers)
    #print(f'GET EVENTS RESPONSE STATUS CODE: {response.status_code}')
    logging.info(f'GET EVENTS RESPONSE STATUS CODE: {response.status_code}')
    return response.json()

@app.route('/get_mail_settings')
def get_mail_settings():
    token_access = directory_manager.ReadJSON(token_path, 'api_token_access.json')
    token = token_access['access_token']
    headers = {
        'Authorization': f'{token_access["token_type"]} {token}',
        'Content-Type': 'application/json'
    }
    response = requests.get('https://graph.microsoft.com/v1.0/me/mailboxsettings', headers=headers)
    #print(f'GET MAIL-SETTINGS RESPONSE STATUS CODE: {response.status_code}')
    logging.info(f'GET MAIL-SETTINGS RESPONSE STATUS CODE: {response.status_code}')
    return response.json()

# @app.route('/get_timezones')
# def get_timezones():
#     token_access = directory_manager.ReadJSON(token_path, 'api_token_access.json')
#     token = token_access['access_token']
#     headers = { 
#         'Authorization': f'{token_access["token_type"]} {token}',
#         'Content-Type': 'application/json'
#     }
#     response = requests.get('https://graph.microsoft.com/v1.0/me/outlook/supportedTimeZones', headers=headers)
#     print(f'GET TIMEZONE RESPONSE STATUS CODE: {response.status_code}')
#     return response.json()

# Only expecting 1 event per .ics file
def parse_ics(ics)->OutlookEvent:
    ics_file = CalendarInterface.ReadICSFile(ics)
    #res = send_flask_req(req='get_mail_settings')
    #user_profile = res[1]
    # Extract the time zone information
    #time_zone = user_profile.get('mailboxSettings', {}).get('timeZone')
    #tz = time_zone if time_zone is not None else 'Asia/Singapore'

    for component in ics_file.walk():
        if component.name == "VEVENT":
            rule=component.get('rrule').to_ical().decode(errors="ignore") if component.get('rrule') is not None else ''
            s_dt = component.get('dtstart').dt
            e_dt = component.get('dtend').dt
            return OutlookEvent(name=component.get('name'),
                                location=component.get("location"),
                                dtstart=s_dt.isoformat(),
                                dtend=e_dt.isoformat(),
                                tzstart='UTC',
                                tzend='UTC',
                                rrule=rule
                                )
    return None

# Require this to go from Flask -> Outlook
# send_flask_req will always return true if any sort of response is received
def send_flask_req(req, json_data={}, param_data={})->[bool, dict]:
    response = requests.get(f"http://localhost:{local_host}/{req}", json=json_data, params=param_data)
    #print(f'Response Content:\n{response.json()}')
    '''
    HTTP status codes in the 200-299 range indicate success, with 200 being the standard response for a successful HTTP request.

    HTTP status codes in the 400-499 range indicate client errors. For instance, a 404 status code means "Not Found", and a 400 means "Bad Request".

    HTTP status codes in the 500-599 range indicate server errors.
    '''
    if 200 <= response.status_code < 300: return True, response.json()
    else: return False, {}

def run():
    login()
    app.wsgi_app = ProxyFix(app.wsgi_app)
    app.run(host='localhost', port=local_host, use_reloader = False)

def start_flask():
    logging.info('ESTABLISHING CONNECTION TO OUTLOOK API THROUGH FLASK')
    flask_thread = threading.Thread(target=run)
    flask_thread.start()