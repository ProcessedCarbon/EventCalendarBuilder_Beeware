import subprocess
from eventcalendarbuilder.PythonFiles.Managers.TextProcessing import TextProcessingManager

mac_calendar_events = []

def getMacCalendarEvents():
        retrieve_applescript = """
                    tell application "Calendar"
                        set theCalendars to calendars
                        set output to ""
                        repeat with aCalendar in theCalendars
                            set theseEvents to (every event of aCalendar whose start date ≥ (current date))
                            repeat with anEvent in theseEvents
                                set output to output & "Title: " & (summary of anEvent) & ", Date: " & (start date of anEvent) & linefeed
                            end repeat
                        end repeat
                    end tell
                    return output
                    """
        osa_command = ['osascript', '-e', retrieve_applescript]
        events = subprocess.check_output(osa_command).decode('utf-8').strip()

        # Need to split events up as it comes in one entire long string
        events = events.split('\n')

        mac_events = []
        for e in events:
            # Splits into the this format
            #['Title: Hari Raya Puasa', 'Date: Friday', '20 March 2026 at 12:00:00 AM']
            attributes = e.split(", ")

            # Get event attributes
            name = attributes[0].split(':')[1]
            datetime = attributes[2].split('at')
            processed_date = TextProcessingManager.ProcessDate(datetime[0])

            # Add to list of events on mac
            mac_events.append({
                "name" : name,
                "date" : processed_date,
                "time" : datetime[1],

            })

        return mac_events    

def RemoveMacCalendarEvents(event_summary)->bool:
        applescript = f"""
            tell application "Calendar"
                set theCalendars to calendars
                repeat with aCalendar in theCalendars
                    tell aCalendar
                        set theEvents to every event whose summary is "{event_summary}"
                        repeat with anEvent in theEvents
                            delete anEvent
                        end repeat
                    end tell
                end repeat
            end tell
            """
        
        process = subprocess.Popen(['osascript', '-'], 
                                   stdin=subprocess.PIPE, 
                                   stdout=subprocess.PIPE, 
                                   stderr=subprocess.PIPE, 
                                   text=True)
        
        stdout, stderr = process.communicate(applescript)

        # if stderr: print(f"Error: {stderr}")
        # else: print(f"Result: {stdout}")
