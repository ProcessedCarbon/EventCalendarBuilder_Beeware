from enum import Enum
# Calendar Types
DEFAULT_CALENDAR = 'Default'
GOOGLE_CALENDAR = 'Google'
OUTLOOK_CALENDAR = 'Outlook'

# Recurrence
class RecurrenceTypes(Enum):
    NONE = 'None'
    DAILY = 'Daily'
    WEEKLY = 'Weekly'
    MONTHLY = 'Monthly'

# Status
class ScheduleStatus(Enum):
    SUCCESS = 'Success'
    FAILED = 'Failed'
    CLASH = 'Clash'